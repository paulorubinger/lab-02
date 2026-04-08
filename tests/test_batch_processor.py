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


def create_test_repositories_csv():
    """Create a test repositories.csv file if it doesn't exist."""
    os.makedirs("data/raw", exist_ok=True)
    
    test_repos = [
        {
            "owner": "Snailclimb",
            "repository": "JavaGuide",
            "stars": 150000,
            "releases": 50,
            "created_at": "2018-01-01",
            "url": "https://github.com/Snailclimb/JavaGuide"
        },
        {
            "owner": "krahets",
            "repository": "hello-algo",
            "stars": 100000,
            "releases": 30,
            "created_at": "2020-06-15",
            "url": "https://github.com/krahets/hello-algo"
        },
        {
            "owner": "GrowingGit",
            "repository": "GitHub-Chinese-Top-Charts",
            "stars": 80000,
            "releases": 20,
            "created_at": "2019-03-01",
            "url": "https://github.com/GrowingGit/GitHub-Chinese-Top-Charts"
        }
    ]
    
    with open("data/raw/repositories.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "owner", "repository", "stars", "releases", "created_at", "url"
        ])
        writer.writeheader()
        writer.writerows(test_repos)
    
    print("✓ Created test repositories.csv with 3 sample repositories\n")


def test_batch_processor(num_repos: int = 1):
    print("\n" + "="*80)
    print(f"TESTING BATCH PROCESSOR WITH {num_repos} REPOSITORY(IES)")
    print("="*80 + "\n")
    
    processor = BatchProcessor(
        consolidated_csv="data/processed/test_consolidated_metrics.csv",
        progress_file="data/processed/test_progress.txt",
        keep_repos=True,      # KEEP cloned repos
        keep_metrics=True,    # KEEP CK metrics folder
        verbose=True          # SHOW detailed errors
    )
    
    # Check if repositories.csv exists
    if not os.path.exists(processor.repositories_csv):
        print(f"❌ Repository list not found: {processor.repositories_csv}\n")
        print("Options:")
        print("  1. Run 'python src/main.py' first to fetch repositories from GitHub")
        print("  2. Create a test CSV file\n")
        
        response = input("Create test repositories.csv? (y/n): ").strip().lower()
        if response == 'y':
            create_test_repositories_csv()
        else:
            print("\n❌ Cannot proceed without repository list")
            print("   Run: python src/main.py")
            return
    
    # Load first N repositories
    print(f"Loading {num_repos} test repositories...\n")
    try:
        with open(processor.repositories_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            test_repos = []
            for i, row in enumerate(reader):
                if i >= num_repos:
                    break
                test_repos.append(row)
                print(f"  [{i+1}] {row['owner']}/{row['repository']}")
    except Exception as e:
        print(f"❌ Error reading repository list: {e}")
        return
    
    if not test_repos:
        print("\n❌ No repositories found in CSV file")
        return
    
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
        print("  run: python tests/cleanup_test_data.py")
        print("\nThen run the full pipeline:")
        print("  run: python src/main.py")
    else:
        print("\n✗ All repositories failed - check errors above")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    test_batch_processor(num_repos=num)
