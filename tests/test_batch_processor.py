#!/usr/bin/env python3
"""
Quick test script - process few repositories to validate batch processor works correctly.
Keeps repos and metrics for inspection.
"""

import csv
import sys
import os

# Add parent directory to path so we can import from src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processing.batch_processor import BatchProcessor


def test_batch_processor(num_repos: int = 1):
    print("\n" + "="*80)
    print(f"TESTING BATCH PROCESSOR WITH {num_repos} REPOSITORY(IES)")
    print("="*80 + "\n")
    
    processor = BatchProcessor(
        keep_repos=True,      # KEEP cloned repos
        keep_metrics=True,    # KEEP CK metrics folder
        verbose=True          # SHOW detailed errors
    )
    
    # Load first N repositories
    print(f"Loading {num_repos} test repositories...\n")
    with open(processor.repositories_csv, 'r') as f:
        reader = csv.DictReader(f)
        test_repos = []
        for i, row in enumerate(reader):
            if i >= num_repos:
                break
            test_repos.append(row)
            print(f"  [{i+1}] {row['owner']}/{row['repository']}")
    
    print("\nProcessing steps:")
    print("  1. Clone with --depth 1")
    print("  2. Run CK analysis")
    print("  3. Extract metrics")
    print("  4. Save to CSV")
    print("  5. Keep repos and metrics for inspection\n")
    
    success_count = 0
    for idx, repo in enumerate(test_repos, start=1):
        owner = repo['owner']
        repo_name = repo['repository']
        success = processor.process_one_repo(owner, repo_name, idx, len(test_repos))
        if success:
            success_count += 1
    
    print("\n" + "="*80)
    print(f"TEST RESULTS: {success_count}/{len(test_repos)} repositories processed successfully")
    print("="*80)
    
    if success_count > 0:
        print("\n✓ Batch processor working!")
        print("\nGenerated files:")
        print(f"  - Cloned repos: repos/")
        print(f"  - CK metrics: data/raw/ck_metrics/")
        print(f"  - Consolidated CSV: {processor.consolidated_csv}")
        print(f"  - Progress file: {processor.progress_file}")
        print("\nTo cleanup test files:")
        print("  - Remove: repos/")
        print("  - Remove: data/raw/ck_metrics/")
        print("  - Remove: data/processed/progress.txt")
        print("  - Remove: data/processed/consolidated_metrics.csv")
        print("\nThen run: python src/main.py")
    else:
        print("\n✗ All repositories failed - check errors above")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    test_batch_processor(num_repos=num)
