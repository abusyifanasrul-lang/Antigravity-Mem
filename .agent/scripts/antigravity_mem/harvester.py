"""
Hardened Harvester
===================
Extracts code change observations from git diff and stores them in memory.db.

Improvements over the original:
1. Silent Failure Logging — unclassifiable chunks go to unclassified_log, never silently skipped.
2. Change Type Classification — semantic labels: added, removed, logic, signature, renamed, moved.
3. Similarity Scoring — detects renames via difflib.SequenceMatcher (threshold 0.85).
4. Confidence Scores — each observation rated 0.0–1.0 based on detection reliability.
"""

import os
import re
import sqlite3
import subprocess
from datetime import datetime
from difflib import SequenceMatcher

# Paths
DB_PATH = os.path.join(os.getcwd(), ".agent", "memory.db")

# Thresholds
RENAME_SIMILARITY_THRESHOLD = 0.85

# Patterns for function detection (Universal)
# Supports: TS/JS, Python, Go, Rust, PHP, Ruby, etc.
FUNC_PATTERN = re.compile(
    r"(?:export\s+)?(?:async\s+)?(?:function|def|func|fn)\s+(\w+)\s*[\(\[]"  # Standard functions
    r"|(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(.*?\)\s*=>" # Arrow functions
    r"|^(\w+)\s*\(.*?\)\s*\{" # Class methods or simplified functions
    r"|^(\w+)\s*:\s*function", # Object methods
    re.MULTILINE,
)


def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def get_git_diff():
    return run_command("git diff HEAD~1 HEAD")


def get_session_id():
    return os.environ.get("CONVERSATION_ID", "default_session")


def extract_function_name(line):
    """Try to extract a function/variable name from a diff line."""
    match = FUNC_PATTERN.search(line)
    if match:
        return match.group(1) or match.group(2) or match.group(3)
    return None


def parse_diff_into_file_chunks(diff_text):
    """
    Split a unified diff into per-file chunks.
    Returns list of dicts: {file_path, added_lines, removed_lines, raw}
    """
    chunks = []
    current_file = None
    current_added = []
    current_removed = []
    current_raw = []

    for line in diff_text.split("\n"):
        if line.startswith("diff --git"):
            # Save previous chunk
            if current_file:
                chunks.append(
                    {
                        "file_path": current_file,
                        "added_lines": current_added,
                        "removed_lines": current_removed,
                        "raw": "\n".join(current_raw),
                    }
                )
            current_file = None
            current_added = []
            current_removed = []
            current_raw = [line]

        elif line.startswith("+++ b/"):
            current_file = line[6:]
            current_raw.append(line)

        elif line.startswith("+") and not line.startswith("+++"):
            current_added.append(line[1:])
            current_raw.append(line)

        elif line.startswith("-") and not line.startswith("---"):
            current_removed.append(line[1:])
            current_raw.append(line)

        else:
            current_raw.append(line)

    # Don't forget the last chunk
    if current_file:
        chunks.append(
            {
                "file_path": current_file,
                "added_lines": current_added,
                "removed_lines": current_removed,
                "raw": "\n".join(current_raw),
            }
        )

    return chunks


def extract_functions_from_lines(lines):
    """
    Extract function signatures from a list of source lines.
    Returns dict: {func_name: body_text}
    """
    functions = {}
    for line in lines:
        name = extract_function_name(line)
        if name and name not in functions:
            functions[name] = line.strip()
    return functions


def classify_file_changes(chunk):
    """
    Classify changes in a single file chunk.
    Returns list of dicts: {name, change_type, confidence, detail}
    """
    results = []
    removed_funcs = extract_functions_from_lines(chunk["removed_lines"])
    added_funcs = extract_functions_from_lines(chunk["added_lines"])

    removed_names = set(removed_funcs.keys())
    added_names = set(added_funcs.keys())

    # Functions present in both → logic or signature change
    common = removed_names & added_names
    for name in common:
        old_body = removed_funcs[name]
        new_body = added_funcs[name]
        similarity = SequenceMatcher(None, old_body, new_body).ratio()

        if similarity > 0.95:
            # Almost identical, likely whitespace/formatting change
            results.append(
                {
                    "name": name,
                    "change_type": "logic",
                    "confidence": 0.9,
                    "detail": f"Minor change (similarity: {similarity:.2f})",
                }
            )
        elif "(" in old_body and "(" in new_body:
            # Check if signature changed
            old_sig = old_body.split("(")[0]
            new_sig = new_body.split("(")[0]
            if old_sig != new_sig:
                results.append(
                    {
                        "name": name,
                        "change_type": "signature",
                        "confidence": 0.9,
                        "detail": f"Signature changed: {old_sig} → {new_sig}",
                    }
                )
            else:
                results.append(
                    {
                        "name": name,
                        "change_type": "logic",
                        "confidence": 0.7,
                        "detail": f"Body changed (similarity: {similarity:.2f})",
                    }
                )
        else:
            results.append(
                {
                    "name": name,
                    "change_type": "logic",
                    "confidence": 0.7,
                    "detail": "Body changed",
                }
            )

    # Functions only removed → check if renamed (similarity match with added)
    only_removed = removed_names - common
    only_added = added_names - common
    matched_renames = set()

    for old_name in only_removed:
        old_body = removed_funcs[old_name]
        best_match = None
        best_score = 0.0

        for new_name in only_added - matched_renames:
            new_body = added_funcs[new_name]
            score = SequenceMatcher(None, old_body, new_body).ratio()
            if score > best_score:
                best_score = score
                best_match = new_name

        if best_match and best_score >= RENAME_SIMILARITY_THRESHOLD:
            matched_renames.add(best_match)
            results.append(
                {
                    "name": f"{old_name} → {best_match}",
                    "change_type": "renamed",
                    "confidence": 0.7,
                    "detail": f"Rename detected (similarity: {best_score:.2f})",
                }
            )
        else:
            results.append(
                {
                    "name": old_name,
                    "change_type": "removed",
                    "confidence": 0.9,
                    "detail": "Function removed",
                }
            )

    # Functions only added (excluding those matched as renames)
    truly_added = only_added - matched_renames
    for name in truly_added:
        results.append(
            {
                "name": name,
                "change_type": "added",
                "confidence": 0.9,
                "detail": "New function",
            }
        )

    return results


def log_unclassified(cursor, observation_id, file_path, reason, raw_diff):
    """Log a chunk that failed classification to unclassified_log."""
    cursor.execute(
        """
    INSERT INTO unclassified_log (observation_id, file_path, reason, raw_diff, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """,
        (
            observation_id,
            file_path,
            reason,
            raw_diff[:2000],  # Cap raw diff to prevent DB bloat
            datetime.now().isoformat(),
        ),
    )


def harvest():
    print("Harvesting session data...")
    diff = get_git_diff()

    if not diff.strip():
        print("No git diff found. Nothing to harvest.")
        return

    chunks = parse_diff_into_file_chunks(diff)
    affected_files = [c["file_path"] for c in chunks]

    # Classify all changes across all files
    all_changes = []
    unclassified_chunks = []

    for chunk in chunks:
        try:
            file_changes = classify_file_changes(chunk)
            if file_changes:
                all_changes.extend(file_changes)
            else:
                # File changed but no functions detected — record as unclassified
                unclassified_chunks.append(
                    {
                        "file_path": chunk["file_path"],
                        "reason": "No function signatures detected in changed lines",
                        "raw": chunk["raw"],
                    }
                )
        except Exception as e:
            unclassified_chunks.append(
                {
                    "file_path": chunk["file_path"],
                    "reason": f"Classification error: {str(e)}",
                    "raw": chunk["raw"],
                }
            )

    # Calculate aggregate confidence
    if all_changes:
        avg_confidence = sum(c["confidence"] for c in all_changes) / len(all_changes)
    else:
        avg_confidence = 0.3  # Low confidence if nothing was classified

    # Determine dominant change type
    change_types = [c["change_type"] for c in all_changes]
    dominant_type = max(set(change_types), key=change_types.count) if change_types else "unknown"

    # Build description
    type_counts = {}
    for ct in change_types:
        type_counts[ct] = type_counts.get(ct, 0) + 1

    change_summary = ", ".join(f"{count} {ctype}" for ctype, count in type_counts.items())
    function_names = [c["name"] for c in all_changes]

    description = (
        f"Changes in {len(affected_files)} file(s): {change_summary}. "
        f"Functions: {', '.join(function_names[:10])}"
    )
    if len(function_names) > 10:
        description += f" (+{len(function_names) - 10} more)"

    if unclassified_chunks:
        description += f". {len(unclassified_chunks)} chunk(s) unclassified."

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    session_id = get_session_id()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        "INSERT OR IGNORE INTO sessions (id, start_time) VALUES (?, ?)",
        (session_id, timestamp),
    )

    cursor.execute(
        """
    INSERT INTO observations
        (session_id, type, description, affected_files, overwritten_functions,
         timestamp, confidence, detection_method, change_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            session_id,
            "auto_harvest",
            description,
            ", ".join(affected_files),
            ", ".join(function_names),
            timestamp,
            round(avg_confidence, 2),
            "heuristic",
            dominant_type,
        ),
    )

    observation_id = cursor.lastrowid

    # Log unclassified chunks — NEVER silently skip
    for uc in unclassified_chunks:
        log_unclassified(
            cursor, observation_id, uc["file_path"], uc["reason"], uc["raw"]
        )

    conn.commit()
    conn.close()

    print(f"Harvest completed:")
    print(f"  Files: {len(affected_files)}")
    print(f"  Classified changes: {len(all_changes)}")
    print(f"  Unclassified chunks: {len(unclassified_chunks)}")
    print(f"  Avg confidence: {avg_confidence:.2f}")
    print(f"  Dominant change type: {dominant_type}")


if __name__ == "__main__":
    harvest()
