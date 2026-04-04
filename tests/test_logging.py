#!/usr/bin/env python3
"""
Test script to demonstrate the logging system.
This creates a sample log file to show how the logger works.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.processing_logger import ProcessingLogger


def main():
    print("Creating a sample processing log...\n")
    
    # Create logger
    logger = ProcessingLogger()
    
    # Simulate some processing
    repos = [
        ("java-repo-1", True, None),
        ("kotlin-repo-1", True, None),
        ("java-repo-2", False, "fatal: unable to access repository: Connection timed out"),
        ("java-repo-3", True, None),
        ("java-repo-4", False, "fatal: Repository not found"),
    ]
    
    print(f"Simulating clone of {len(repos)} repositories...\n")
    
    for repo_name, success, error in repos:
        logger.increment_attempted()
        if success:
            logger.log_clone_success(repo_name)
            print(f"✓ {repo_name} cloned successfully")
        else:
            logger.log_clone_failure(repo_name, error)
            print(f"✗ {repo_name} failed: {error[:60]}")
    
    print("\nSimulating analysis of 3 repositories...\n")
    
    analysis_repos = [
        ("java-repo-1", True, None, None),
        ("kotlin-repo-1", False, "ck_analysis", "Java memory error: OutOfMemoryException"),
        ("java-repo-3", True, None, None),
    ]
    
    for repo_name, success, stage, error in analysis_repos:
        if success:
            logger.log_analysis_success(repo_name)
            print(f"✓ {repo_name} analyzed successfully")
        else:
            logger.log_analysis_failure(repo_name, stage, error)
            print(f"✗ {repo_name} failed at {stage}: {error[:50]}")
    
    # Display summary
    print("\n" + "=" * 80)
    logger.print_summary()
    
    print(f"\nSample log created at: {logger.log_file}")
    print("You can view this log with: python src/utils/view_logs.py")


if __name__ == "__main__":
    main()
