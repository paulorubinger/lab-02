#!/usr/bin/env python3
"""
Inspect generated test files - check repos, metrics, CSV contents.
"""

import os
import pandas as pd

# Change to parent directory so relative paths work
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def inspect_repos():
    """List cloned repositories."""
    repos_dir = "repos"
    if not os.path.exists(repos_dir):
        print(f"  (none)")
        return
    
    repos = [d for d in os.listdir(repos_dir) if os.path.isdir(os.path.join(repos_dir, d))]
    if not repos:
        print(f"  (empty)")
        return
    
    for repo in sorted(repos):
        repo_path = os.path.join(repos_dir, repo)
        size_mb = sum(os.path.getsize(os.path.join(dirpath, filename))
                     for dirpath, dirnames, filenames in os.walk(repo_path)
                     for filename in filenames) / (1024 * 1024)
        print(f"  • {repo} ({size_mb:.1f} MB)")


def inspect_ck_metrics():
    """List CK metrics output."""
    metrics_dir = "data/raw/ck_metrics"
    if not os.path.exists(metrics_dir):
        print(f"  (none)")
        return
    
    repos = [d for d in os.listdir(metrics_dir) if os.path.isdir(os.path.join(metrics_dir, d))]
    if not repos:
        print(f"  (empty)")
        return
    
    for repo in sorted(repos):
        repo_path = os.path.join(metrics_dir, repo)
        files = os.listdir(repo_path)
        print(f"  • {repo}/")
        for f in sorted(files):
            file_path = os.path.join(repo_path, f)
            if os.path.isfile(file_path):
                size_kb = os.path.getsize(file_path) / 1024
                print(f"      - {f} ({size_kb:.1f} KB)")


def inspect_metrics_csv():
    """Show consolidated metrics CSV contents."""
    csv_file = "data/processed/test_consolidated_metrics.csv"
    if not os.path.exists(csv_file):
        print(f"  (not found)")
        return
    
    try:
        df = pd.read_csv(csv_file)
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"  Columns: {', '.join(df.columns.tolist())}")
        print(f"\n  Preview:")
        print(df.to_string(max_rows=5, max_colwidth=20))
    except Exception as e:
        print(f"  Error reading CSV: {e}")


def inspect_progress():
    """Show progress file."""
    prog_file = "data/processed/test_progress.txt"
    if not os.path.exists(prog_file):
        print(f"  (not found)")
        return
    
    try:
        with open(prog_file, 'r') as f:
            lines = f.readlines()
        print(f"  Processed repositories: {len(lines)}")
        for line in lines:
            print(f"    • {line.strip()}")
    except Exception as e:
        print(f"  Error reading file: {e}")


def main():
    print("\n" + "="*80)
    print("TEST DATA INSPECTION")
    print("="*80 + "\n")
    
    print("📁 Cloned Repositories (repos/):")
    inspect_repos()
    
    print("\n📊 CK Metrics Output (data/raw/ck_metrics/):")
    inspect_ck_metrics()
    
    print("\n📈 Consolidated Metrics (data/processed/test_consolidated_metrics.csv):")
    inspect_metrics_csv()
    
    print("\n✓ Progress Tracking (data/processed/test_progress.txt):")
    inspect_progress()
    
    print("\n" + "="*80)
    print("To cleanup: python cleanup_test_data.py --confirm")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
