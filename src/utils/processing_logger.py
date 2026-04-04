"""
Processing logger for tracking clone and analysis failures.
Logs failures to JSON for easy parsing and reporting.
"""

import os
import json
from datetime import datetime
from typing import List


class ProcessingLogger:
    def __init__(self, log_dir: str = "logs"):
        """Initialize the logger."""
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Current execution log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"processing_{timestamp}.json")
        
        self.data = {
            "execution_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_attempted": 0,
                "clone_successful": 0,
                "clone_failed": 0,
                "analysis_successful": 0,
                "analysis_failed": 0
            },
            "clone_failures": [],
            "analysis_failures": []
        }
    
    def log_clone_failure(self, repo_name: str, error: str):
        """Log a clone failure."""
        failure = {
            "repo": repo_name,
            "timestamp": datetime.now().isoformat(),
            "error": error[:500]  # Limit error message length
        }
        self.data["clone_failures"].append(failure)
        self.data["summary"]["clone_failed"] += 1
        self.save()
    
    def log_clone_success(self, repo_name: str):
        """Log a successful clone."""
        self.data["summary"]["clone_successful"] += 1
        self.save()
    
    def log_analysis_failure(self, repo_name: str, stage: str, error: str):
        """Log an analysis failure.
        
        Args:
            repo_name: Name of the repository
            stage: Stage where failure occurred (e.g., 'ck_analysis', 'metrics_extraction', 'data_save')
            error: Error message
        """
        failure = {
            "repo": repo_name,
            "stage": stage,
            "timestamp": datetime.now().isoformat(),
            "error": error[:500]  # Limit error message length
        }
        self.data["analysis_failures"].append(failure)
        self.data["summary"]["analysis_failed"] += 1
        self.save()
    
    def log_analysis_success(self, repo_name: str):
        """Log a successful analysis."""
        self.data["summary"]["analysis_successful"] += 1
        self.save()
    
    def increment_attempted(self):
        """Increment total attempted counter."""
        self.data["summary"]["total_attempted"] += 1
        self.save()
    
    def save(self):
        """Save log to JSON file."""
        with open(self.log_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_summary(self) -> dict:
        """Get the current summary."""
        return self.data["summary"]
    
    def print_summary(self):
        """Print a formatted summary of the execution."""
        summary = self.data["summary"]
        
        print("\n" + "=" * 80)
        print("PROCESSING SUMMARY")
        print("=" * 80)
        print(f"\nTotal attempted: {summary['total_attempted']}")
        print(f"  Clone successful: {summary['clone_successful']}")
        print(f"  Clone failures:   {summary['clone_failed']}")
        print(f"  Analysis successful: {summary['analysis_successful']}")
        print(f"  Analysis failures:   {summary['analysis_failed']}")
        
        clone_success_rate = (
            100 * summary['clone_successful'] / (summary['clone_successful'] + summary['clone_failed'])
            if (summary['clone_successful'] + summary['clone_failed']) > 0 else 0
        )
        analysis_success_rate = (
            100 * summary['analysis_successful'] / (summary['analysis_successful'] + summary['analysis_failed'])
            if (summary['analysis_successful'] + summary['analysis_failed']) > 0 else 0
        )
        
        print(f"\nSuccess rates:")
        print(f"  Clone success rate:    {clone_success_rate:.1f}%")
        print(f"  Analysis success rate: {analysis_success_rate:.1f}%")
        
        if self.data["clone_failures"]:
            print(f"\n❌ Clone failures ({len(self.data['clone_failures'])}):")
            for failure in self.data["clone_failures"][:10]:  # Show first 10
                print(f"  • {failure['repo']}: {failure['error'][:60]}")
            if len(self.data["clone_failures"]) > 10:
                print(f"  ... and {len(self.data['clone_failures']) - 10} more")
        
        if self.data["analysis_failures"]:
            print(f"\n❌ Analysis failures ({len(self.data['analysis_failures'])}):")
            for failure in self.data["analysis_failures"][:10]:  # Show first 10
                print(f"  • {failure['repo']} ({failure['stage']}): {failure['error'][:50]}")
            if len(self.data["analysis_failures"]) > 10:
                print(f"  ... and {len(self.data['analysis_failures']) - 10} more")
        
        print(f"\nLog file: {self.log_file}")
        print("=" * 80 + "\n")
    
    @staticmethod
    def list_logs(log_dir: str = "logs") -> List[str]:
        """List all log files."""
        if not os.path.exists(log_dir):
            return []
        return sorted([f for f in os.listdir(log_dir) if f.startswith("processing_") and f.endswith(".json")])
    
    @staticmethod
    def load_log(log_file: str) -> dict:
        """Load a specific log file."""
        with open(log_file, 'r') as f:
            return json.load(f)
