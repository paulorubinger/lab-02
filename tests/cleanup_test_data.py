#!/usr/bin/env python3
"""
Cleanup script - remove test data (repos, CK metrics, progress tracking).
Use after inspecting test results.
"""

import os
import sys
import shutil

# Change to parent directory so relative paths work
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def cleanup_test_data():
    print("\n" + "="*80)
    print("CLEANING UP TEST DATA")
    print("="*80 + "\n")
    
    items_to_delete = [
        ("repos/", "Cloned repositories"),
        ("data/raw/ck_metrics/", "CK metrics output"),
        ("data/processed/progress.txt", "Progress tracking file"),
        ("data/processed/consolidated_metrics.csv", "Consolidated metrics CSV")
    ]
    
    deleted_count = 0
    
    for path, description in items_to_delete:
        full_path = os.path.abspath(path)
        
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    def handle_remove_readonly(func, path, exc):
                        import stat
                        os.chmod(path, stat.S_IWRITE)
                        func(path)
                    
                    shutil.rmtree(path, onerror=handle_remove_readonly)
                else:
                    os.remove(path)
                
                print(f"✓ Deleted: {path}")
                print(f"  ({description})")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Failed to delete: {path}")
                print(f"  Error: {e}")
        else:
            print(f"• Skipped: {path} (not found)")
    
    print("\n" + "="*80)
    print(f"Cleaned {deleted_count} items")
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm":
        cleanup_test_data()
    else:
        print("\n" + "="*80)
        print("CLEANUP PREVIEW")
        print("="*80 + "\n")
        
        items_to_delete = [
            ("repos/", "Cloned repositories"),
            ("data/raw/ck_metrics/", "CK metrics output"),
            ("data/processed/progress.txt", "Progress tracking file"),
            ("data/processed/consolidated_metrics.csv", "Consolidated metrics CSV")
        ]
        
        print("This will delete:")
        for path, description in items_to_delete:
            if os.path.exists(path):
                print(f"  • {path} ({description})")
        
        print("\nTo confirm cleanup, run:")
        print("  python tests/cleanup_test_data.py --confirm")
        print("\n")
