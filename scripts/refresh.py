#!/usr/bin/env python3
"""
Soundvault — 1-Click Apple Music Data Refresh Script
Syncs fresh play counts, skips, and track additions from macOS Music.app ('English' playlist)
and regenerates the frontend dataset (src/lib/data/artists-data.js).
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

def run_step(description, script_name):
    print(f"\n[STEP] {description}...")
    script_path = SCRIPTS_DIR / script_name
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"[ERROR] Error during {script_name}:")
        print(result.stderr)
        sys.exit(1)
    
    print(result.stdout.strip())

def main():
    print("=" * 60)
    print("SOUNDVAULT — SYNCING WITH APPLE MUSIC ('English' Playlist)")
    print("=" * 60)
    
    # 1. Extract fresh metrics from macOS Music.app
    run_step("1/4: Extracting real-time playback metrics from Apple Music", "extract_extended_data.py")
    
    # 2. Fetch any missing high-res artist artwork
    run_step("2/4: Fetching high-res Apple Music artwork for artists", "fetch_artist_images.py")

    # 3. Fetch authentic editorial artist biographies
    run_step("3/4: Fetching authentic artist descriptions & bios", "fetch_artist_bios.py")
    
    # 4. Recompute catalog stats, Fibonacci galaxy coordinates, and leaderboard
    run_step("4/4: Recomputing analytics & generating artists-data.js", "build_data.py")
    
    print("\n" + "=" * 60)
    print("SUCCESS: All catalog data updated!")
    print("Your frontend at http://localhost:3000 will reflect the changes immediately via Vite HMR.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
