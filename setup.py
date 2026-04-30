
import os
import shutil
import subprocess
import sys

def print_step(msg):
    print(f"\n[🚀] {msg}")

def run_command(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing: {cmd}")
        return False

def setup():
    print("==========================================")
    print("   Antigravity Memory Protocol Installer  ")
    print("==========================================")

    # 1. Check Python Version
    if sys.version_info < (3, 10):
        print("❌ Error: Python 3.10+ is required.")
        return

    # 2. Install Graphify
    print_step("Installing Graphify dependency...")
    if run_command("pip install git+https://github.com/abusyifanasrul-lang/graphify.git"):
        print("✅ Graphify installed successfully.")
    else:
        print("⚠️ Failed to install Graphify. You might need to install it manually later.")

    # 3. Create Folder Structure
    print_step("Creating project structure...")
    folders = [
        ".agent/rules",
        ".agent/scripts/antigravity_mem",
        "scripts",
        "graphify-out"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"  - Created {folder}/")

    # 4. Copy Files (Assuming script is inside the distribution folder)
    print_step("Deploying protocol files...")
    # This script expects to be in the root of the temp folder or same level as the files
    # We will copy from current directory to the project directories
    
    mapping = {
        "scripts/sync_knowledge.py": "scripts/sync_knowledge.py",
        ".agent/rules/GEMINI.md": ".agent/rules/GEMINI.md",
        ".agent/scripts/antigravity_mem/harvester.py": ".agent/scripts/antigravity_mem/harvester.py",
        ".agent/scripts/antigravity_mem/init_db.py": ".agent/scripts/antigravity_mem/init_db.py",
        ".agent/scripts/antigravity_mem/migrate_memory_db.py": ".agent/scripts/antigravity_mem/migrate_memory_db.py",
        ".agent/scripts/antigravity_mem/sync_mem.py": ".agent/scripts/antigravity_mem/sync_mem.py",
        ".agent/scripts/antigravity_mem/review_unclassified.py": ".agent/scripts/antigravity_mem/review_unclassified.py",
        "KNOWLEDGE_MAP.md": "KNOWLEDGE_MAP.md",
        "STATE_OF_THE_UNION.md": "STATE_OF_THE_UNION.md"
    }

    for src, dest in mapping.items():
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"  - Deployed {dest}")
        else:
            print(f"  - ⚠️ Source {src} not found, skipping.")

    # 5. Initialize Database
    print_step("Initializing Memory Database...")
    if os.path.exists(".agent/scripts/antigravity_mem/init_db.py"):
        run_command("python .agent/scripts/antigravity_mem/init_db.py")
        print("✅ Database memory.db initialized.")

    # 6. Auto-Detection: New vs Existing Project
    print_step("Analyzing project state...")
    is_existing = False
    
    # Check for Git history
    git_check = run_command("git rev-parse --is-inside-work-tree")
    if git_check == "true":
        commit_count = run_command("git rev-list --count HEAD")
        if commit_count and int(commit_count) > 0:
            is_existing = True
            print(f"  - Detected Git repository with {commit_count} commits.")

    # Check for common folders if not git
    if not is_existing:
        common_indicators = ['src', 'lib', 'apps', 'package.json', 'main.py', 'go.mod']
        for indicator in common_indicators:
            if os.path.exists(indicator):
                is_existing = True
                print(f"  - Detected existing project via indicator: '{indicator}'")
                break

    if is_existing:
        print("\n🤖 [Sistem Mendeteksi Project Berjalan]")
        print("Sangat disarankan untuk menjalankan 'Initial Discovery Scan' agar AI memahami konteks project Anda saat ini.")
        choice = input("❓ Jalankan scan sekarang? (Y/n): ").lower()
        if choice != 'n':
            print_step("Running Initial Discovery Scan...")
            run_command("python .agent/scripts/antigravity_mem/backfill_legacy.py")
            print("✅ Project history and structure ingested.")
    else:
        print("\n🌱 [Sistem Mendeteksi Project Baru]")
        print("Selamat memulai! AI akan mulai mencatat memori sejak commit pertama Anda.")

    print("\n" + "="*42)
    print("🎉 INSTALLATION COMPLETE!")
    print("="*42)
    print("\nNext Steps:")
    print("1. Pastikan Agent Anda mengenali protokol ini.")
    print("2. Berikan instruksi: 'Aktifkan Automated Memory Protocol sesuai GEMINI.md'")
    print("3. Jalankan 'python scripts/sync_knowledge.py' untuk sinkronisasi pertama.")
    print("\nHappy Coding with Antigravity! 🤖")

if __name__ == "__main__":
    setup()
