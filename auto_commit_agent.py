#!/usr/bin/env python3
"""
auto_commit_agent.py

Runs continuously and makes CONFIGURED commits per day to its own repo.
"""

import os
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from git import Repo, GitCommandError

# ─── CONFIG ────────────────────────────────────────────────────────────────
# Number of commits per day (5–10 is reasonable)
COMMIT_COUNT = int(os.environ.get("COMMIT_COUNT", 7))

# Window during which commits may happen (24-hour clock)
START_HOUR = int(os.environ.get("START_HOUR", 9))   # earliest commit at 09:00
END_HOUR   = int(os.environ.get("END_HOUR", 17))  # latest commit by 17:00

# Path to this script / repo root
SCRIPT_PATH = Path(__file__).resolve()
REPO_PATH   = SCRIPT_PATH.parent

# Git settings
REMOTE_NAME   = "origin"
BRANCH        = os.environ.get("BRANCH", "main")
# ─────────────────────────────────────────────────────────────────────────────

def schedule_times(count, start_h, end_h):
    """Return sorted list of 'HH:MM' strings for today's run."""
    start = start_h * 60
    end   = end_h * 60
    if count > (end - start):
        raise ValueError("Too many commits for given time window")
    minutes = random.sample(range(start, end), count)
    hhmm = sorted(f"{m//60:02d}:{m%60:02d}" for m in minutes)
    return hhmm

def do_commit(repo, file_path):
    """Append timestamp to own script, commit & push."""
    ts = datetime.utcnow().isoformat() + "Z"
    with open(file_path, "a") as f:
        f.write(f"\n# Auto-updated at {ts}")
    repo.index.add([str(file_path)])
    msg = f"Auto-commit at {ts}"
    repo.index.commit(msg)
    try:
        repo.remote(REMOTE_NAME).push(refspec=f"HEAD:{BRANCH}")
        print(f"[{ts}] Pushed commit.")
    except GitCommandError as e:
        print(f"[{ts}] Push failed:", e)

def main():
    random.seed()  # system time seed
    repo = Repo(REPO_PATH)
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    # Compute today's commit schedule once at startup
    today_times = schedule_times(COMMIT_COUNT, START_HOUR, END_HOUR)
    print("Today's commit schedule:", ", ".join(today_times))

    while True:
        now = datetime.now()
        # If we've rolled into a new day, recompute schedule
        if now.date() >= tomorrow:
            tomorrow = (now + timedelta(days=1)).date()
            today_times = schedule_times(COMMIT_COUNT, START_HOUR, END_HOUR)
            print("\nNew schedule for", now.date(), ":", ", ".join(today_times))

        current_hm = now.strftime("%H:%M")
        if current_hm in today_times:
            try:
                do_commit(repo, SCRIPT_PATH)
            except Exception as ex:
                print(f"[{current_hm}] Error during commit:", ex)
            # ensure we only run once per scheduled time
            today_times.remove(current_hm)

        time.sleep(30)  # check twice a minute

if __name__ == "__main__":
    main()