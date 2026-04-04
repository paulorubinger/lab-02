#!/usr/bin/env python3
"""
Main pipeline for collecting and analyzing CK metrics from 1000 GitHub Java repositories.
Uses batch processing to minimize disk usage: clone -> analyze -> delete -> repeat.
"""

import os
import sys
import io

# Configure UTF-8 encoding for Windows console output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from github_api.repositories import fetch_repositories
from utils.save_csv import save_to_csv
from utils.load_query import load_query
from utils.processing_logger import ProcessingLogger
from processing.batch_processor import BatchProcessor

def main():
    # 1. Fetch repositories (if not already fetched)
    print("\n" + "="*80)
    print("STEP 1: FETCHING TOP 1000 JAVA REPOSITORIES FROM GITHUB")
    print("="*80 + "\n")
    
    query_path = "src/github_api/queries/top_java_repositories.graphql"
    repositories_csv = "data/raw/repositories.csv"
    
    if not os.path.exists(repositories_csv):
        print("Repository list not found. Fetching from GitHub...\n")
        
        query = load_query(query_path)
        repositories = fetch_repositories(query, total=1000)
        
        save_to_csv(repositories, repositories_csv)
        
        print(f"\n✓ Fetched {len(repositories)} repositories")
    else:
        import csv
        with open(repositories_csv) as f:
            num_repos = sum(1 for _ in csv.DictReader(f))
        print(f"Using existing repository list: {num_repos} repositories")
        print(f"  Location: {os.path.abspath(repositories_csv)}\n")
    
    # 2. Batch process repositories
    print("\n" + "="*80)
    print("STEP 2: BATCH PROCESSING (Clone -> CK -> Save -> Delete)")
    print("="*80 + "\n")
    print("Processing strategy: 1 repository at a time to minimize disk usage")
    
    # Create logger
    logger = ProcessingLogger()
    
    processor = BatchProcessor(
        repositories_csv=repositories_csv,
        ck_jar="ck.jar",
        ck_metrics_folder="data/raw/ck_metrics",
        consolidated_csv="data/processed/consolidated_metrics.csv",
        progress_file="data/processed/progress.txt",
        logger=logger
    )
    
    processor.process_all_repositories(resume=True)
    
    print("\n" + "="*80)
    print("PIPELINE COMPLETE")
    print("="*80 + "\n")
    print("Next steps:")
    print("  1. Run final analysis on consolidated_metrics.csv")
    print("  2. Generate visualizations")
    print("  3. Create final report\n")


if __name__ == "__main__":
    main()