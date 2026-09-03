import subprocess
import json
import csv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
out_csv = DATA_DIR / "apple_music_extended.csv"

script = '''
(() => {
  const music = Application("Music");
  const playlist = music.playlists.byName("English");
  if (!playlist) {
    throw new Error("Playlist 'English' not found in Music.app");
  }
  
  const names = playlist.tracks.name();
  const artists = playlist.tracks.artist();
  const albums = playlist.tracks.album();
  const genres = playlist.tracks.genre();
  const plays = playlist.tracks.playedCount();
  const skips = playlist.tracks.skippedCount();
  const durations = playlist.tracks.duration();
  const years = playlist.tracks.year();
  const playedDates = playlist.tracks.playedDate();
  const datesAdded = playlist.tracks.dateAdded();
  
  const res = [];
  const len = names.length;
  for (let i = 0; i < len; i++) {
    res.push({
      Title: names[i] || "",
      Artist: artists[i] || "",
      Album: albums[i] || "",
      Genre: genres[i] || "",
      PlayCount: plays[i] || 0,
      SkipCount: skips[i] || 0,
      Year: years[i] || "",
      DurationSec: Math.round(durations[i] || 0),
      PlayedDate: playedDates[i] ? new Date(playedDates[i]).toISOString() : "",
      DateAdded: datesAdded[i] ? new Date(datesAdded[i]).toISOString() : ""
    });
  }
  return JSON.stringify(res);
})()
'''

print("Extracting English Playlist from Apple Music...")
proc = subprocess.run(["osascript", "-l", "JavaScript", "-e", script], capture_output=True, text=True)
if proc.returncode != 0:
    print("Error executing script:", proc.stderr)
    exit(1)

data = json.loads(proc.stdout)
print(f"Extracted {len(data)} curated tracks from 'English' playlist.")

fieldnames = ["Title", "Artist", "Album", "Genre", "PlayCount", "SkipCount", "Year", "DurationSec", "PlayedDate", "DateAdded"]
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Saved to {out_csv} successfully!")
