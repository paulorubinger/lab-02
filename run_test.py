#!/usr/bin/env python3
"""
Quick access to test scripts from project root.
Use: python run_test.py [cleanup|inspect|test] [args]
"""

import sys
import subprocess
import os

if len(sys.argv) < 2:
    print("\n" + "="*80)
    print("TEST SCRIPT RUNNER")
    print("="*80 + "\n")
    print("Usage:")
    print("  python run_test.py test [N]              # Test N repos (default 1)")
    print("  python run_test.py inspect               # Inspect test data")
    print("  python run_test.py cleanup [--confirm]   # Cleanup test data\n")
    print("Examples:")
    print("  python run_test.py test 1                # Test with 1 repo")
    print("  python run_test.py test 5                # Test with 5 repos")
    print("  python run_test.py inspect               # See results")
    print("  python run_test.py cleanup --confirm     # Delete test files\n")
    sys.exit(0)

command = sys.argv[1]
args = sys.argv[2:] if len(sys.argv) > 2 else []

script_map = {
    "test": "tests/test_batch_processor.py",
    "inspect": "tests/inspect_test_data.py",
    "cleanup": "tests/cleanup_test_data.py"
}

if command not in script_map:
    print(f"\n❌ Unknown command: {command}")
    print(f"   Available: {', '.join(script_map.keys())}\n")
    sys.exit(1)

script_path = script_map[command]

# Run the script with args
result = subprocess.run([sys.executable, script_path] + args)
sys.exit(result.returncode)
