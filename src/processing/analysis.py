"""
Analysis module for CK metrics and GitHub repository data.
Aggregates CK metrics, combines with repository characteristics,
and performs correlation analysis to answer research questions.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats

class CKAnalysis:
    def __init__(
        self,
        ck_metrics_folder: str = "data/raw/ck_metrics",
        repositories_csv: str = "data/raw/repositories.csv",
        output_folder: str = "data/processed"
    ):
        self.ck_metrics_folder = ck_metrics_folder
        self.repositories_csv = repositories_csv
        self.output_folder = output_folder
        self.repos_data = None
        self.ck_aggregated = None
        self.combined_data = None
        
        os.makedirs(output_folder, exist_ok=True)
    
    def load_repositories(self) -> pd.DataFrame:
        """Load GitHub repository data."""
        print(f"Loading repositories from {self.repositories_csv}...")
        self.repos_data = pd.read_csv(self.repositories_csv)
        
        # Convert created_at to datetime and calculate age
        self.repos_data['created_at'] = pd.to_datetime(self.repos_data['created_at'], utc=True)
        # Remove timezone info for calculation
        self.repos_data['age_days'] = (pd.Timestamp.now(tz='UTC') - self.repos_data['created_at']).dt.days
        
        print(f"  Loaded {len(self.repos_data)} repositories")
        return self.repos_data
    
    def _read_ck_file(self, filepath: str) -> pd.DataFrame:
        """Read a single CK CSV file."""
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            print(f"  ERROR reading {filepath}: {e}")
            return None
    
    def _aggregate_repo_metrics(self, repo_name: str) -> dict:
        """Aggregate CK metrics for a single repository."""
        repo_path = os.path.join(self.ck_metrics_folder, repo_name)
        
        metrics = {
            'repository': repo_name,
            'classes_analyzed': 0,
            'methods_analyzed': 0,
        }
        
        # Read class metrics
        class_csv = os.path.join(repo_path, "class.csv")
        if os.path.exists(class_csv):
            class_df = self._read_ck_file(class_csv)
            if class_df is not None:
                metrics['classes_analyzed'] = len(class_df)
                
                # Key quality metrics averaged across classes
                quality_metrics = ['cbo', 'dit', 'lcom', 'wmc', 'rfc', 'loc', 'nosi']
                for metric in quality_metrics:
                    if metric in class_df.columns:
                        # Handle NaN values
                        valid_values = pd.to_numeric(class_df[metric], errors='coerce').dropna()
                        if len(valid_values) > 0:
                            metrics[f'{metric}_avg'] = valid_values.mean()
                            metrics[f'{metric}_max'] = valid_values.max()
                            metrics[f'{metric}_median'] = valid_values.median()
                            metrics[f'{metric}_std'] = valid_values.std()
                        else:
                            metrics[f'{metric}_avg'] = np.nan
                            metrics[f'{metric}_max'] = np.nan
                            metrics[f'{metric}_median'] = np.nan
                            metrics[f'{metric}_std'] = np.nan
                
                # Calculate total LOC
                if 'loc' in class_df.columns:
                    loc_values = pd.to_numeric(class_df['loc'], errors='coerce').dropna()
                    metrics['total_loc'] = loc_values.sum()
        
        # Read method metrics
        method_csv = os.path.join(repo_path, "method.csv")
        if os.path.exists(method_csv):
            method_df = self._read_ck_file(method_csv)
            if method_df is not None:
                metrics['methods_analyzed'] = len(method_df)
                
                # Method-level quality metrics
                if 'cbo' in method_df.columns:
                    cbo_values = pd.to_numeric(method_df['cbo'], errors='coerce').dropna()
                    if len(cbo_values) > 0:
                        metrics['method_cbo_avg'] = cbo_values.mean()
                if 'loc' in method_df.columns:
                    loc_values = pd.to_numeric(method_df['loc'], errors='coerce').dropna()
                    if len(loc_values) > 0:
                        metrics['method_loc_avg'] = loc_values.mean()
        
        return metrics
    
    def aggregate_ck_metrics(self) -> pd.DataFrame:
        """Aggregate all CK metrics by repository."""
        print(f"\nAggregating CK metrics from {self.ck_metrics_folder}...")
        
        repo_names = [
            d for d in os.listdir(self.ck_metrics_folder)
            if os.path.isdir(os.path.join(self.ck_metrics_folder, d))
        ]
        
        aggregated_data = []
        for repo_name in repo_names:
            print(f"  Processing {repo_name}...")
            metrics = self._aggregate_repo_metrics(repo_name)
            aggregated_data.append(metrics)
        
        self.ck_aggregated = pd.DataFrame(aggregated_data)
        print(f"  Aggregated metrics for {len(self.ck_aggregated)} repositories")
        return self.ck_aggregated
    
    def combine_data(self) -> pd.DataFrame:
        """Combine GitHub and CK metrics data."""
        print("\nCombining GitHub and CK metrics...")
        
        if self.repos_data is None:
            self.load_repositories()
        if self.ck_aggregated is None:
            self.aggregate_ck_metrics()
        
        # Create mapping from repository name in repos to folder name in ck_metrics
        # repositories.csv has format: "owner", "repository" = directory name in repos folder
        repo_folders = os.listdir(self.ck_metrics_folder)
        
        # Try to match repositories with CK metrics folders
        combined = []
        for _, repo_row in self.repos_data.iterrows():
            repo_name = repo_row['repository']
            owner = repo_row['owner']
            
            # Try exact match and fuzzy match
            ck_row = None
            for ck_folder in repo_folders:
                if repo_name.lower() in ck_folder.lower() or ck_folder.lower() in repo_name.lower():
                    ck_row = self.ck_aggregated[self.ck_aggregated['repository'] == ck_folder]
                    if len(ck_row) > 0:
                        ck_row = ck_row.iloc[0].to_dict()
                        break
            
            if ck_row is not None:
                row = repo_row.to_dict()
                row.update(ck_row)
                combined.append(row)
        
        self.combined_data = pd.DataFrame(combined)
        print(f"  Combined data for {len(self.combined_data)} repositories")
        return self.combined_data
    
    def calculate_correlations(self) -> dict:
        """Calculate correlations for each research question."""
        print("\nCalculating correlations...")
        
        if self.combined_data is None:
            self.combine_data()
        
        results = {}
        
        # Define quality metrics
        quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'wmc_avg', 'rfc_avg']
        
        # RQ01: Popularity (stars) vs Quality
        print("\n  RQ01: Popularity vs Quality")
        results['RQ01'] = self._calculate_rq_correlations(
            'stars', quality_metrics,
            "Relationship between repository popularity (stars) and code quality"
        )
        
        # RQ02: Maturity (age) vs Quality
        print("  RQ02: Maturity vs Quality")
        results['RQ02'] = self._calculate_rq_correlations(
            'age_days', quality_metrics,
            "Relationship between repository maturity (age) and code quality"
        )
        
        # RQ03: Activity (releases) vs Quality
        print("  RQ03: Activity vs Quality")
        results['RQ03'] = self._calculate_rq_correlations(
            'releases', quality_metrics,
            "Relationship between repository activity (releases) and code quality"
        )
        
        # RQ04: Size (LOC) vs Quality
        print("  RQ04: Size vs Quality")
        results['RQ04'] = self._calculate_rq_correlations(
            'total_loc', quality_metrics,
            "Relationship between repository size (LOC) and code quality"
        )
        
        return results
    
    def _calculate_rq_correlations(self, independent_var: str, dependent_vars: list, description: str) -> dict:
        """Calculate correlations for a specific research question."""
        result = {
            'description': description,
            'independent_var': independent_var,
            'correlations': {}
        }
        
        # Filter data with valid values
        data = self.combined_data[[independent_var] + dependent_vars].dropna()
        
        if len(data) < 3:
            print(f"    WARNING: Not enough data points ({len(data)}) for correlation")
            return result
        
        for var in dependent_vars:
            x = data[independent_var].values
            y = data[var].values
            
            # Pearson correlation
            pearson_r, pearson_p = stats.pearsonr(x, y)
            
            # Spearman correlation
            spearman_r, spearman_p = stats.spearmanr(x, y)
            
            result['correlations'][var] = {
                'pearson_r': pearson_r,
                'pearson_p': pearson_p,
                'spearman_r': spearman_r,
                'spearman_p': spearman_p,
                'n_samples': len(data)
            }
        
        return result
    
    def generate_descriptive_statistics(self) -> pd.DataFrame:
        """Generate descriptive statistics table."""
        print("\nGenerating descriptive statistics...")
        
        if self.combined_data is None:
            self.combine_data()
        
        # Select numeric columns for statistics
        numeric_cols = self.combined_data.select_dtypes(include=[np.number]).columns
        
        stats_df = self.combined_data[numeric_cols].describe().T
        stats_df['cv'] = self.combined_data[numeric_cols].std() / self.combined_data[numeric_cols].mean()
        
        return stats_df
    
    def save_results(self, correlation_results: dict, stats_df: pd.DataFrame):
        """Save all results to files."""
        print("\nSaving results...")
        
        # Save combined data
        combined_file = os.path.join(self.output_folder, "combined_metrics.csv")
        self.combined_data.to_csv(combined_file, index=False)
        print(f"  Saved combined data to {combined_file}")
        
        # Save descriptive statistics
        stats_file = os.path.join(self.output_folder, "descriptive_statistics.csv")
        stats_df.to_csv(stats_file)
        print(f"  Saved statistics to {stats_file}")
        
        # Save correlation results
        correlation_file = os.path.join(self.output_folder, "correlation_results.txt")
        with open(correlation_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CORRELATION ANALYSIS RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            for rq, results in correlation_results.items():
                f.write(f"\n{rq}: {results['description']}\n")
                f.write(f"Independent Variable: {results['independent_var']}\n")
                f.write("-" * 80 + "\n")
                
                for metric, corr_data in results['correlations'].items():
                    f.write(f"\n  {metric}:\n")
                    f.write(f"    Pearson:  r={corr_data['pearson_r']:.4f}, p={corr_data['pearson_p']:.4f}\n")
                    f.write(f"    Spearman: r={corr_data['spearman_r']:.4f}, p={corr_data['spearman_p']:.4f}\n")
                    f.write(f"    Samples: {corr_data['n_samples']}\n")
        
        print(f"  Saved correlation results to {correlation_file}")
    
    def generate_report(self, correlation_results: dict) -> str:
        """Generate a comprehensive analysis report."""
        print("\nGenerating analysis report...")
        
        report = []
        report.append("=" * 80)
        report.append("JAVA SOFTWARE QUALITY ANALYSIS - GITHUB REPOSITORIES")
        report.append("=" * 80)
        report.append(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Repositories Analyzed: {len(self.combined_data)}")
        report.append(f"Classes Analyzed: {self.combined_data['classes_analyzed'].sum():.0f}")
        report.append(f"Methods Analyzed: {self.combined_data['methods_analyzed'].sum():.0f}")
        
        report.append("\n" + "=" * 80)
        report.append("RESEARCH QUESTIONS RESULTS")
        report.append("=" * 80)
        
        for rq, results in correlation_results.items():
            report.append(f"\n{rq}: {results['description']}")
            report.append(f"Independent Variable: {results['independent_var']}")
            report.append("-" * 80)
            
            has_significant = False
            for metric, corr_data in results['correlations'].items():
                pearson_p = corr_data['pearson_p']
                pearson_r = corr_data['pearson_r']
                
                # Significance: p < 0.05
                if pearson_p < 0.05:
                    has_significant = True
                    report.append(f"\n  [OK] {metric}:")
                    report.append(f"    - Pearson Correlation: r = {pearson_r:.4f} (p = {pearson_p:.4f}) **SIGNIFICANT**")
                else:
                    report.append(f"\n  [--] {metric}:")
                    report.append(f"    - Pearson Correlation: r = {pearson_r:.4f} (p = {pearson_p:.4f})")
            
            if not has_significant:
                report.append("\n  No significant correlations found (α = 0.05)")
                
        return "\n".join(report)
    
    def run_full_analysis(self):
        """Run complete analysis pipeline."""
        print("\n" + "=" * 80)
        print("STARTING FULL ANALYSIS")
        print("=" * 80)
        
        # Load and process data
        self.load_repositories()
        self.aggregate_ck_metrics()
        self.combine_data()
        
        # Calculate correlations
        correlation_results = self.calculate_correlations()
        
        # Generate statistics
        stats_df = self.generate_descriptive_statistics()
        
        # Save results
        self.save_results(correlation_results, stats_df)
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETED")
        print("=" * 80)
        print("\nFiles generated in 'data/processed/':")
        print("  - combined_metrics.csv")
        print("  - descriptive_statistics.csv")
        print("  - correlation_results.txt")
        
        return {
            'combined_data': self.combined_data,
            'statistics': stats_df,
            'correlations': correlation_results
        }
    
    def save_report(self, correlation_results: dict):
        """Save analysis report to file."""
        print("\nGenerating analysis report...")
        report = self.generate_report(correlation_results)
        report_file = os.path.join(self.output_folder, "analysis_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"  Saved report to {report_file}")
        return report

if __name__ == "__main__":
    analysis = CKAnalysis()
    results = analysis.run_full_analysis()
