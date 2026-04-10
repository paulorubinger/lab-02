"""
Batch processor for repositories - processes one repo at a time to minimize disk usage.
Clones -> Analyzes with CK -> Saves metrics -> Deletes repo.
"""

import os
import csv
import sys
import shutil
import subprocess
import pandas as pd

# Add parent directory to path so we can import from utils/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.processing_logger import ProcessingLogger


class BatchProcessor:
    def __init__(
        self,
        repositories_csv: str = "data/raw/repositories.csv",
        ck_jar: str = "ck.jar",
        ck_metrics_folder: str = "data/raw/ck_metrics",
        consolidated_csv: str = "data/processed/consolidated_metrics.csv",
        progress_file: str = "data/processed/progress.txt",
        keep_repos: bool = False,
        keep_metrics: bool = False,
        verbose: bool = False,
        logger: ProcessingLogger = None
    ):
        self.repositories_csv = repositories_csv
        self.ck_jar = ck_jar
        self.ck_metrics_folder = ck_metrics_folder
        self.consolidated_csv = consolidated_csv
        self.progress_file = progress_file
        self.repos_folder = "repos"
        self.keep_repos = keep_repos
        self.keep_metrics = keep_metrics
        self.verbose = verbose
        self.logger = logger
        
        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("repos", exist_ok=True)
        
    def get_processed_repos(self) -> set:
        """Get list of already processed repositories."""
        if not os.path.exists(self.progress_file):
            return set()
        
        try:
            with open(self.progress_file, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        except:
            return set()
    
    def mark_repo_processed(self, repo_name: str):
        """Mark repository as processed."""
        with open(self.progress_file, 'a') as f:
            f.write(f"{repo_name}\n")
    
    def delete_repo_folder(self, repo_name: str):
        """Delete repository folder.
        
        On Windows, handles long paths and special characters by:
        - Retrying if file is temporarily locked
        - Using more aggressive permission removal
        - Using subprocess for robust deletion as fallback
        """
        if self.keep_repos:
            if self.verbose:
                print(f"  [KEEP] {repo_name} (keep_repos=True)")
            return
        
        repo_path = os.path.join(self.repos_folder, repo_name)
        if not os.path.exists(repo_path):
            return
        
        # Try shutil.rmtree first (standard approach)
        try:
            def handle_remove_readonly(func, path, exc):
                import stat
                try:
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                except:
                    pass
            
            shutil.rmtree(repo_path, onerror=handle_remove_readonly)
            if self.verbose:
                print(f"  Deleted {repo_name}")
            return
        except Exception as e:
            if self.verbose:
                print(f"  WARNING (shutil): Could not delete {repo_name}: {str(e)[:100]}")
        
        # Fallback: try subprocess rmdir for Windows
        if sys.platform == "win32":
            try:
                import subprocess
                result = subprocess.run(
                    ["rmdir", "/s", "/q", repo_path],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode == 0:
                    if self.verbose:
                        print(f"  Deleted {repo_name} (via rmdir)")
                    return
            except Exception as e:
                if self.verbose:
                    print(f"  WARNING (rmdir): {str(e)[:100]}")
        
        # If all else fails, just log it and continue
        print(f"  WARNING: Could not delete {repo_name} (will persist). Please remove manually: {repo_path}")
    
    def delete_ck_metrics_folder(self, repo_name: str):
        """Delete CK metrics folder for this repo.
        
        Same robust deletion as delete_repo_folder.
        """
        if self.keep_metrics:
            if self.verbose:
                print(f"  [KEEP] CK metrics for {repo_name} (keep_metrics=True)")
            return
        
        metrics_path = os.path.join(self.ck_metrics_folder, repo_name)
        if not os.path.exists(metrics_path):
            return
        
        # Try shutil.rmtree first
        try:
            def handle_remove_readonly(func, path, exc):
                import stat
                try:
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                except:
                    pass
            
            shutil.rmtree(metrics_path, onerror=handle_remove_readonly)
            if self.verbose:
                print(f"  Deleted CK metrics")
            return
        except Exception as e:
            if self.verbose:
                print(f"  WARNING (shutil): Could not delete CK metrics: {str(e)[:100]}")
        
        # Fallback: try subprocess rmdir for Windows
        if sys.platform == "win32":
            try:
                import subprocess
                result = subprocess.run(
                    ["rmdir", "/s", "/q", metrics_path],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode == 0:
                    if self.verbose:
                        print(f"  Deleted CK metrics (via rmdir)")
                    return
            except Exception as e:
                if self.verbose:
                    print(f"  WARNING (rmdir): {str(e)[:100]}")
        
        # If all else fails, log and continue
        if self.verbose:
            print(f"  WARNING: Could not delete CK metrics (will persist)")

    
    def extract_repo_metrics(self, repo_name: str) -> dict:
        """Extract aggregated metrics for a single repository."""
        repo_path = os.path.join(self.ck_metrics_folder, repo_name)
        
        metrics = {'repository': repo_name}
        
        # Read class metrics
        class_csv = os.path.join(repo_path, "class.csv")
        if os.path.exists(class_csv):
            try:
                class_df = pd.read_csv(class_csv)
                
                # Aggregate key metrics
                # Use lcom* (normalized 0-1) instead of lcom (unreliable first version)
                for metric in ['cbo', 'dit', 'lcom*', 'wmc', 'rfc', 'loc']:
                    if metric in class_df.columns:
                        valid_values = pd.to_numeric(class_df[metric], errors='coerce').dropna()
                        if len(valid_values) > 0:
                            col = 'lcom_star' if metric == 'lcom*' else metric
                            metrics[f'{col}_avg'] = valid_values.mean()
                            metrics[f'{col}_median'] = valid_values.median()
                            metrics[f'{col}_min'] = valid_values.min()
                            metrics[f'{col}_max'] = valid_values.max()
                            metrics[f'{col}_std'] = valid_values.std()
            except:
                pass
        
        return metrics
    
    def process_one_repo(self, owner: str, repo_name: str, current_index: int, total: int) -> bool:
        """Process a single repository: clone -> CK -> extract metrics -> delete."""
        repo_display_name = f"{owner}_{repo_name}"
        
        print(f"\n[{current_index}/{total}] Processing {repo_display_name}")
        
        if self.logger:
            self.logger.increment_attempted()
        
        try:
            # 1. Clone repository
            print(f"  Cloning... {repo_name}")
            repo_url = f"https://github.com/{owner}/{repo_name}"
            
            # Remove existing folder if it exists (from previous incomplete run)
            repo_destination = os.path.join(self.repos_folder, repo_display_name)
            if os.path.exists(repo_destination):
                try:
                    def handle_remove_readonly(func, path, exc):
                        import stat
                        os.chmod(path, stat.S_IWRITE)
                        func(path)
                    
                    shutil.rmtree(repo_destination, onerror=handle_remove_readonly)
                    if self.verbose:
                        print(f"    (removed existing incomplete clone)")
                except:
                    pass
            
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, repo_destination],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                print(f"  ERROR: Clone failed")
                if self.verbose or result.stderr:
                    print(f"    stderr: {error_msg[:300]}")
                if self.logger:
                    self.logger.log_clone_failure(repo_display_name, error_msg)
                return False
            
            if self.logger:
                self.logger.log_clone_success(repo_display_name)
            
            # 2. Run CK analysis
            print(f"  Running CK analysis...")
            repo_path = os.path.join(self.repos_folder, repo_display_name)
            ck_output = os.path.join(self.ck_metrics_folder, repo_display_name)
            
            # Create output folder for CK
            os.makedirs(ck_output, exist_ok=True)
            
            result = subprocess.run([
                "java", "-jar", self.ck_jar, repo_path, "false", "0", "false", ck_output            
            ], capture_output=True, text=True, timeout=1200)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                print(f"  ERROR: CK analysis failed")
                if self.verbose or result.stderr:
                    print(f"    stderr: {error_msg[:300]}")
                if self.logger:
                    self.logger.log_analysis_failure(repo_display_name, "ck_analysis", error_msg)
                self.delete_repo_folder(repo_display_name)
                return False
            
            # 3. Extract and save metrics
            print(f"  Extracting metrics...")
            try:
                metrics = self.extract_repo_metrics(repo_display_name)
                
                if not metrics or len(metrics) < 2:
                    raise Exception("No metrics extracted")
                
                # Append to consolidated CSV
                df_new = pd.DataFrame([metrics])
                if os.path.exists(self.consolidated_csv):
                    df_existing = pd.read_csv(self.consolidated_csv)
                    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                else:
                    df_combined = df_new
                
                df_combined.to_csv(self.consolidated_csv, index=False)
                print(f"  ✓ Metrics saved")
            except Exception as e:
                error_msg = str(e)
                print(f"  WARNING: {error_msg}")
                if self.logger:
                    self.logger.log_analysis_failure(repo_display_name, "metrics_extraction", error_msg)
                self.delete_repo_folder(repo_display_name)
                self.delete_ck_metrics_folder(repo_display_name)
                return False
            
            # 4. Clean up
            print(f"  Cleaning up...")
            self.delete_repo_folder(repo_display_name)
            self.delete_ck_metrics_folder(repo_display_name)
            
            # Mark as processed
            self.mark_repo_processed(repo_display_name)
            
            if self.logger:
                self.logger.log_analysis_success(repo_display_name)
            
            print(f"  ✓ Completed")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"  ERROR: {error_msg}")
            if self.logger:
                self.logger.log_analysis_failure(repo_display_name, "process_repo", error_msg)
            self.delete_repo_folder(repo_display_name)
            self.delete_ck_metrics_folder(repo_display_name)
            return False
    
    def process_all_repositories(self, resume: bool = True):
        """Process all repositories one by one."""
        # Initialize logger if not provided
        if not self.logger:
            self.logger = ProcessingLogger()
        
        print("\n" + "=" * 80)
        print("BATCH PROCESSING REPOSITORIES (One at a time)")
        print("=" * 80)
        
        # Load repositories
        print("\nLoading repository list...")
        repositories = []
        with open(self.repositories_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                repositories.append(row)
        
        print(f"  Found {len(repositories)} repositories")
        
        # Get already processed
        processed = self.get_processed_repos() if resume else set()
        remaining = [r for r in repositories if f"{r['owner']}_{r['repository']}" not in processed]
        
        print(f"  Already processed: {len(processed)}")
        print(f"  Remaining: {len(remaining)}")
        
        if not remaining:
            print("\nAll repositories already processed!")
            return
        
        # Process remaining repositories
        total_to_process = len(remaining)
        for idx, repo in enumerate(remaining, start=1):
            owner = repo['owner']
            repo_name = repo['repository']
            
            success = self.process_one_repo(owner, repo_name, idx, total_to_process)
            
            if not success:
                print(f"  Continuing to next repository...")

        print("\n" + "=" * 80)
        print("BATCH PROCESSING COMPLETED")
        print("=" * 80)
        # Print final summary
        self.logger.print_summary()
        
        print("\nConsolidated metrics saved to: {}\n".format(self.consolidated_csv))


if __name__ == "__main__":
    import subprocess
    
    processor = BatchProcessor()
    processor.process_all_repositories(resume=True)
