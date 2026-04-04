#!/usr/bin/env python3
"""
Utility to view and analyze processing logs.
Usage: python view_logs.py [log_file]
"""

import os
import sys
import json
from processing_logger import ProcessingLogger


def view_logs(log_dir: str = "logs"):
    """View available logs."""
    logs = ProcessingLogger.list_logs(log_dir)
    
    if not logs:
        print("No log files found.")
        return
    
    print("\nAvailable logs:")
    for i, log_file in enumerate(logs, 1):
        print(f"{i}. {log_file}")
    
    return logs


def display_log(log_file: str):
    """Display a specific log file."""
    try:
        data = ProcessingLogger.load_log(log_file)
        
        print(f"\n{'='*80}")
        print(f"Log: {log_file}")
        print(f"{'='*80}")
        print(f"Execution: {data['execution_timestamp']}")
        print()
        
        # Summary
        summary = data['summary']
        print("SUMMARY")
        print("-" * 40)
        print(f"Total attempted:        {summary['total_attempted']}")
        print(f"Clone successful:       {summary['clone_successful']}")
        print(f"Clone failures:         {summary['clone_failed']}")
        print(f"Analysis successful:    {summary['analysis_successful']}")
        print(f"Analysis failures:      {summary['analysis_failed']}")
        
        clone_total = summary['clone_successful'] + summary['clone_failed']
        analysis_total = summary['analysis_successful'] + summary['analysis_failed']
        
        if clone_total > 0:
            print(f"Clone success rate:     {100*summary['clone_successful']/clone_total:.1f}%")
        if analysis_total > 0:
            print(f"Analysis success rate:  {100*summary['analysis_successful']/analysis_total:.1f}%")
        
        # Clone failures
        if data['clone_failures']:
            print(f"\nCLONE FAILURES ({len(data['clone_failures'])})")
            print("-" * 40)
            for failure in data['clone_failures']:
                print(f"  • {failure['repo']}")
                print(f"    Error: {failure['error'][:100]}")
                print(f"    Time: {failure['timestamp']}\n")
        
        # Analysis failures
        if data['analysis_failures']:
            print(f"\nANALYSIS FAILURES ({len(data['analysis_failures'])})")
            print("-" * 40)
            for failure in data['analysis_failures']:
                print(f"  • {failure['repo']} (Stage: {failure['stage']})")
                print(f"    Error: {failure['error'][:100]}")
                print(f"    Time: {failure['timestamp']}\n")
        
        print(f"{'='*80}\n")
        
    except FileNotFoundError:
        print(f"Error: Log file not found: {log_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in log file: {log_file}")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        # List and select a log
        logs = view_logs()
        if not logs:
            return
        
        choice = input("\nSelect a log to view (number): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(logs):
                log_file = os.path.join("logs", logs[idx])
            else:
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input.")
            return
    
    display_log(log_file)


if __name__ == "__main__":
    main()
