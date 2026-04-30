import subprocess
import os
import sys

# Get the absolute path to the root directory
# Assuming this script is at .agent/scripts/antigravity_mem/sync_mem.py
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SYNC_SCRIPT = os.path.join(ROOT_DIR, "scripts", "sync_knowledge.py")

def main():
    if not os.path.exists(SYNC_SCRIPT):
        print(f"Error: Sync script not found at {SYNC_SCRIPT}")
        sys.exit(1)
    
    print(f"Executing Antigravity Sync: {SYNC_SCRIPT}")
    result = subprocess.run([sys.executable, SYNC_SCRIPT], cwd=ROOT_DIR)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
