
import os
import sqlite3
import glob
import subprocess
from datetime import datetime

# Path database lokal
DB_PATH = os.path.join(os.getcwd(), ".agent", "memory.db")

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return ""

def get_brain_base():
    """Mencoba menemukan folder brain Antigravity secara dinamis."""
    # Cari di AppData (Windows)
    appdata = os.environ.get("APPDATA")
    if appdata:
        path = os.path.join(appdata, "gemini", "antigravity", "brain")
        if os.path.exists(path):
            return path
            
    # Cari di Home (Linux/macOS)
    home = os.path.expanduser("~")
    path = os.path.join(home, ".gemini", "antigravity", "brain")
    if os.path.exists(path):
        return path
    
    return None

def scan_current_codebase():
    """Memindai struktur proyek saat ini untuk membangun memori awal."""
    print("🔍 Scanning current codebase structure...")
    summary = "# Initial Project Discovery\n\n"
    
    # List top level directories
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    summary += f"### Project Structure:\n- Folders: {', '.join(dirs)}\n\n"
    
    # Look for main files
    main_files = glob.glob("*.json") + glob.glob("*.md") + glob.glob("package.json")
    summary += f"### Configuration & Docs:\n- Files: {', '.join(main_files)}\n\n"
    
    # Get last 5 git commits if available
    git_log = run_command("git log -n 5 --oneline")
    if git_log:
        summary += f"### Recent Git History:\n```\n{git_log}\n```\n"
        
    return summary

def backfill():
    print("==========================================")
    print("   Antigravity Legacy Backfill System     ")
    print("==========================================")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Ingest from Antigravity Brain (if exists)
    brain_base = get_brain_base()
    if brain_base:
        print(f"📂 Found Antigravity Brain at: {brain_base}")
        session_folders = glob.glob(os.path.join(brain_base, "*"))
        for folder in session_folders:
            if not os.path.isdir(folder): continue
            session_id = os.path.basename(folder)
            
            plan_file = os.path.join(folder, "implementation_plan.md")
            walk_file = os.path.join(folder, "walkthrough.md")
            
            content = ""
            if os.path.exists(walk_file):
                with open(walk_file, "r", encoding="utf-8", errors="ignore") as f:
                    content += f"--- WALKTHROUGH ---\n{f.read()}\n"
            if os.path.exists(plan_file):
                with open(plan_file, "r", encoding="utf-8", errors="ignore") as f:
                    content += f"--- PLAN ---\n{f.read()}\n"
            
            if content:
                ts = datetime.fromtimestamp(os.path.getmtime(folder)).isoformat()
                cursor.execute("INSERT OR IGNORE INTO sessions (id, start_time) VALUES (?, ?)", (session_id, ts))
                cursor.execute("INSERT INTO observations (session_id, type, description, timestamp, confidence, detection_method) VALUES (?, ?, ?, ?, ?, ?)", 
                               (session_id, "legacy_backfill", content[:3000], ts, 0.8, "import"))
    
    # 2. Ingest from current Codebase (Universal)
    codebase_summary = scan_current_codebase()
    ts_now = datetime.now().isoformat()
    session_id = "initial_discovery"
    
    cursor.execute("INSERT OR IGNORE INTO sessions (id, start_time) VALUES (?, ?)", (session_id, ts_now))
    cursor.execute("INSERT INTO observations (session_id, type, description, timestamp, confidence, detection_method) VALUES (?, ?, ?, ?, ?, ?)", 
                   (session_id, "discovery", codebase_summary, ts_now, 0.9, "scan"))
    
    conn.commit()
    conn.close()
    print("\n✅ Backfill complete. Knowledge Base has been initialized.")

if __name__ == "__main__":
    backfill()
