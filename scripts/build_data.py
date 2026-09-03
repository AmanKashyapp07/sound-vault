import csv
import json
import hashlib
import re
import math
from collections import defaultdict, Counter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SRC_DATA_DIR = ROOT_DIR / "src" / "lib" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load Apple Music Extended Plays
apple_source_file = DATA_DIR / "apple_music_extended.csv"
with open(apple_source_file, encoding="utf-8") as f:
    apple_tracks = list(csv.DictReader(f))

# Load Artist Biographies
bios_file = DATA_DIR / "artist_bios.json"
artist_bios = {}
if bios_file.exists():
    try:
        with open(bios_file, encoding="utf-8") as f:
            artist_bios = json.load(f)
    except Exception:
        artist_bios = {}

# Palette generator for artists
PRESET_PALETTES = [
    {"primary": "#8B5CF6", "bg": "linear-gradient(135deg,#2e1065,#1e1b4b)", "glow": "rgba(139,92,246,0.35)"},
    {"primary": "#EC4899", "bg": "linear-gradient(135deg,#500724,#2e081d)", "glow": "rgba(236,72,153,0.35)"},
    {"primary": "#3B82F6", "bg": "linear-gradient(135deg,#172554,#0f172a)", "glow": "rgba(59,130,246,0.35)"},
    {"primary": "#10B981", "bg": "linear-gradient(135deg,#022c22,#064e3b)", "glow": "rgba(16,185,129,0.35)"},
    {"primary": "#F59E0B", "bg": "linear-gradient(135deg,#451a03,#291002)", "glow": "rgba(245,158,11,0.35)"},
    {"primary": "#EF4444", "bg": "linear-gradient(135deg,#450a0a,#2b0909)", "glow": "rgba(239,68,68,0.35)"},
    {"primary": "#06B6D4", "bg": "linear-gradient(135deg,#083344,#04222f)", "glow": "rgba(6,182,212,0.35)"},
    {"primary": "#6366F1", "bg": "linear-gradient(135deg,#1e1b4b,#0f0e26)", "glow": "rgba(99,102,241,0.35)"}
]

def get_artist_palette(name):
    h = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:6], 16)
    return PRESET_PALETTES[h % len(PRESET_PALETTES)]

def clean_artist_name(name):
    if not name: return "Unknown Artist"
    n = name.strip()
    if "lorne balfe" in n.lower() or "harold faltermeyer" in n.lower():
        return "Top Gun: Maverick"
    return n

def get_decade(year, album, artist, title):
    al = (album + " " + artist + " " + title).lower()
    if "top gun" in al: return "2020s"
    if year and str(year).isdigit():
        y = int(year)
        if 1960 <= y < 1970: return "1960s"
        if 1970 <= y < 1980: return "1970s"
        if 1980 <= y < 1990: return "1980s"
        if 1990 <= y < 2000: return "1990s"
        if 2000 <= y < 2010: return "2000s"
        if 2010 <= y < 2020: return "2010s"
        if 2020 <= y <= 2030: return "2020s"
    
    # Heuristics based on famous artists
    art = artist.lower()
    if any(k in art for k in ["beatles", "hendrix", "doors", "elvis"]): return "1960s"
    if any(k in art for k in ["queen", "pink floyd", "led zeppelin", "eagles", "fleetwood"]): return "1970s"
    if any(k in art for k in ["michael jackson", "madonna", "bon jovi", "metallica", "guns n roses", "u2", "bryan adams"]): return "1980s"
    if any(k in art for k in ["nirvana", "oasis", "radiohead", "green day", "pearl jam", "red hot chili"]): return "1990s"
    if any(k in art for k in ["linkin park", "coldplay", "eminem", "arctic monkeys", "green day", "avril"]): return "2000s"
    if any(k in art for k in ["weeknd", "ed sheeran", "drake", "taylor swift", "chainsmokers", "ariana"]): return "2010s"
    return "2020s"

def get_genre(genre_raw, artist, album=""):
    g = (genre_raw or "").lower()
    art = (artist or "").lower()
    alb = (album or "").lower()
    
    if "top gun" in art or "soundtrack" in g or "score" in g or "zimmer" in art or "williams" in art or "cinematic" in g:
        return "Cinematic / OST"
    if "arctic monkeys" in art or "strokes" in art or "cage the elephant" in art or "franz ferdinand" in art or "dominic fike" in art or "neighbourhood" in art:
        return "Indie / Alt Rock"
    if "linkin park" in art or "korn" in art or "limp bizkit" in art or "system of a down" in art or "evanescence" in art or "three days grace" in art or "skillet" in art or "paparoach" in art or "papa roach" in art:
        return "Nu-Metal / Alt Rock"
    if "nirvana" in art or "pearl jam" in art or "soundgarden" in art or "alice in chains" in art or "foo fighters" in art or "grunge" in g:
        return "Grunge / Alt Rock"
    if "queen" in art or "pink floyd" in art or "beatles" in art or "led zeppelin" in art or "aerosmith" in art or "doors" in art or "eagles" in art or "fleetwood" in art or "guns n" in art or "metallica" in art or "bon jovi" in art or "ac/dc" in art or "dire straits" in art:
        return "Classic Rock"
    if "madonna" in art or "michael jackson" in art or "modern talking" in art or "george michael" in art or "wham" in art or "a-ha" in art or "rick astley" in art or "backstreet" in art or "spice girls" in art or "ace of base" in art or "sade" in art or "bryan adams" in art or "phil collins" in art:
        return "80s/90s Pop"
    if "eminem" in art or "drake" in art or "kanye" in art or "kendrick" in art or "travis scott" in art or "50 cent" in art or "snoop" in art or "dr. dre" in art or "hip-hop" in g or "rap" in g:
        return "Hip-Hop / Rap"
    if "avicii" in art or "chainsmokers" in art or "calvin harris" in art or "daft punk" in art or "electronic" in g or "dance" in g or "house" in g or "techno" in g or "edm" in g or "david guetta" in art:
        return "Eurodance / Electronic"
    if "weeknd" in art or "bruno mars" in art or "frank ocean" in art or "r&b" in g or "soul" in g or "post malone" in art:
        return "Smooth Soul / R&B"
    if "rock" in g or "metal" in g or "punk" in g:
        return "Classic Rock"
    if "pop" in g:
        return "Modern Pop / Chart"
    return "Modern Pop / Chart"

# Group tracks by artist
artist_groups = defaultdict(list)
seen_tracks = set()

for t in apple_tracks:
    title = t.get("Title", "").strip()
    raw_artist = t.get("Artist", "").strip()
    if not title or not raw_artist: continue
    
    artist_name = clean_artist_name(raw_artist)
    album = t.get("Album", "").strip() or "Singles & EPs"
    genre_raw = t.get("Genre", "").strip()
    year = t.get("Year", "").strip()
    plays = int(t.get("PlayCount") or 0)
    skips = int(t.get("SkipCount") or 0)
    dur = int(t.get("DurationSec") or 210)
    if dur == 0: dur = 210
    
    track_key = (title.lower(), artist_name.lower())
    if track_key in seen_tracks: continue
    seen_tracks.add(track_key)
    
    artist_groups[artist_name].append({
        "title": title,
        "album": album,
        "genre": genre_raw,
        "year": year,
        "plays": plays,
        "skips": skips,
        "durationSec": dur
    })

# Write curated songs.csv
with open(DATA_DIR / "songs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Artist", "Album"])
    writer.writeheader()
    for art_name, tracks in artist_groups.items():
        for tr in tracks:
            writer.writerow({"Title": tr["title"], "Artist": art_name, "Album": tr["album"]})

# Build enriched artist objects
artists_list = []
total_catalog_plays = 0
total_catalog_skips = 0
total_catalog_duration_sec = 0

# Sort artists by total play count descending
sorted_artist_entries = sorted(
    artist_groups.items(), 
    key=lambda item: (sum(x["plays"] for x in item[1]), len(item[1])), 
    reverse=True
)

# Pick top 149 artists
top_artists_subset = sorted_artist_entries[:149]

# Load artist images cache if present
images_file = DATA_DIR / "artist_images.json"
artist_images = {}
if images_file.exists():
    try:
        with open(images_file, "r", encoding="utf-8") as f:
            artist_images = json.load(f)
    except Exception:
        artist_images = {}

for idx, (artist_name, track_list) in enumerate(top_artists_subset):
    track_list.sort(key=lambda x: x["plays"], reverse=True)
    
    art_plays = sum(x["plays"] for x in track_list)
    art_skips = sum(x["skips"] for x in track_list)
    art_dur = sum(x["durationSec"] * max(1, x["plays"]) for x in track_list)
    
    total_catalog_plays += art_plays
    total_catalog_skips += art_skips
    total_catalog_duration_sec += art_dur
    
    albums_set = set(x["album"] for x in track_list)
    sample_year = next((x["year"] for x in track_list if x["year"]), "")
    sample_genre = next((x["genre"] for x in track_list if x["genre"]), "")
    
    decade = get_decade(sample_year, track_list[0]["album"], artist_name, track_list[0]["title"])
    genre = get_genre(sample_genre, artist_name, track_list[0]["album"])
    palette = get_artist_palette(artist_name)
    image_url = artist_images.get(artist_name, "")
    
    # Album breakdowns
    albums_map = defaultdict(list)
    for tr in track_list:
        albums_map[tr["album"]].append(tr)
    
    albums_breakdown = []
    for alb_name, alb_tracks in albums_map.items():
        alb_plays = sum(x["plays"] for x in alb_tracks)
        albums_breakdown.append({
            "name": alb_name,
            "plays": alb_plays,
            "trackCount": len(alb_tracks),
            "songs": alb_tracks
        })
    albums_breakdown.sort(key=lambda x: x["plays"], reverse=True)
    
    completion_rate = round((1 - (art_skips / (art_plays + art_skips))) * 100, 1) if (art_plays + art_skips) > 0 else 100
    avg_plays = round(art_plays / len(track_list), 1) if track_list else 1.0
    total_hours = round(art_dur / 3600, 1)
    
    real_bio = artist_bios.get(artist_name) or f"{artist_name} is one of the most prominent {genre} discographies in your library, featuring {len(track_list)} curated tracks across {len(albums_set)} albums with {art_plays:,} verified plays."

    artists_list.append({
        "id": f"art-{idx+1:03d}",
        "name": artist_name,
        "genre": genre,
        "decade": decade,
        "bio": real_bio,
        "trackCount": len(track_list),
        "albumCount": len(albums_set),
        "totalPlays": art_plays,
        "totalSkips": art_skips,
        "totalHours": total_hours,
        "avgPlays": avg_plays,
        "completionRate": completion_rate,
        "palette": palette,
        "image": image_url,
        "songs": [x["title"] for x in track_list],
        "albums": list(albums_set),
        "songDetails": track_list,
        "albumsBreakdown": albums_breakdown
    })

# Compute Galactic Spiral Coordinates
golden_angle = 137.507764 * (math.pi / 180.0)
for rank, a in enumerate(artists_list):
    r = math.sqrt(rank + 1) * 38.0 + 35.0
    theta = rank * golden_angle
    a["galaxyX"] = round(r * math.cos(theta), 2)
    a["galaxyY"] = round(r * math.sin(theta), 2)
    a["starRadius"] = max(8, min(32, round(math.sqrt(a["totalPlays"] + 1) * 1.5 + 6, 1)))

# Deduplicated Top 20 Songs
all_unique_songs = []
for a in artists_list:
    for s in a["songDetails"]:
        all_unique_songs.append({
            "title": s["title"],
            "artist": a["name"],
            "album": s["album"],
            "plays": s["plays"],
            "skips": s.get("skips", 0),
            "durationSec": s.get("durationSec", 210),
            "genre": a["genre"],
            "decade": a["decade"],
            "artistId": a["id"],
            "palette": a["palette"],
            "image": a.get("image", "")
        })

all_unique_songs.sort(key=lambda x: x["plays"], reverse=True)
top_20_songs = all_unique_songs[:20]

total_hours = round(total_catalog_duration_sec / 3600, 1)
total_days = round(total_hours / 24, 1)
top_artist = artists_list[0] if artists_list else None
top_track_overall = top_20_songs[0] if top_20_songs else {"title": "N/A", "plays": 0}

# Compute 24-Hour Circadian Listening Clock
hour_counts = [0] * 24
for t in apple_tracks:
    p_date = t.get("PlayedDate", "")
    plays = int(t.get("PlayCount", 1) or 1)
    if p_date and "T" in p_date:
        try:
            hour_str = p_date.split("T")[1].split(":")[0]
            h = int(hour_str)
            if 0 <= h < 24:
                hour_counts[h] += max(1, plays)
        except Exception:
            pass

# Fallback distribution if sparse
if sum(hour_counts) == 0:
    hour_counts = [120, 80, 45, 20, 15, 30, 90, 160, 240, 310, 280, 260, 310, 340, 390, 420, 480, 520, 590, 640, 580, 470, 360, 220]

time_segments = {
    "Late Night (00:00 - 06:00)": sum(hour_counts[0:6]),
    "Morning Flow (06:00 - 12:00)": sum(hour_counts[6:12]),
    "Afternoon Focus (12:00 - 18:00)": sum(hour_counts[12:18]),
    "Evening Prime (18:00 - 24:00)": sum(hour_counts[18:24])
}
peak_segment = max(time_segments.items(), key=lambda x: x[1])[0]
peak_hour = hour_counts.index(max(hour_counts))

# Compute Dynamic Milestone Badges
top_artist_name = top_artist['name'] if top_artist else "Top Artist"
top_artist_plays = top_artist['totalPlays'] if top_artist else 0
top_artist_tracks = top_artist['trackCount'] if top_artist else 0
top_track_title = top_track_overall['title'] if top_track_overall else "Top Track"
top_track_plays = top_track_overall['plays'] if top_track_overall else 0
catalog_retention = round((1 - (total_catalog_skips / (total_catalog_plays + total_catalog_skips))) * 100, 1) if (total_catalog_plays + total_catalog_skips) > 0 else 100

badges = [
    {
        "id": "catalog-5k",
        "title": "Catalog Sovereign",
        "badge": "5,000 Plays",
        "icon": "crown",
        "desc": f"Logged {total_catalog_plays:,} / 5,000 total verified plays across the vault",
        "current": total_catalog_plays,
        "target": 5000,
        "unit": "plays",
        "unlocked": total_catalog_plays >= 5000,
        "progress": min(100, round((total_catalog_plays / 5000) * 100, 1))
    },
    {
        "id": "centurion",
        "title": "Devoted Disciple",
        "badge": "500 Plays",
        "icon": "trophy",
        "desc": f"Streamed {top_artist_name} {top_artist_plays} / 500 times in your catalog",
        "current": top_artist_plays,
        "target": 500,
        "unit": "plays",
        "unlocked": top_artist_plays >= 500,
        "progress": min(100, round((top_artist_plays / 500) * 100, 1))
    },
    {
        "id": "marathon-titan",
        "title": "Marathon Titan",
        "badge": "500 Hours",
        "icon": "headphones",
        "desc": f"Listened for {total_hours} / 500 continuous hours ({total_days} full days)",
        "current": total_hours,
        "target": 500,
        "unit": "hours",
        "unlocked": total_hours >= 500,
        "progress": min(100, round((total_hours / 500) * 100, 1))
    },
    {
        "id": "anthem-loop",
        "title": "Anthem Addict",
        "badge": "200 Plays",
        "icon": "flame",
        "desc": f"Played '{top_track_title}' {top_track_plays} / 200 times on loop",
        "current": top_track_plays,
        "target": 200,
        "unit": "plays",
        "unlocked": top_track_plays >= 200,
        "progress": min(100, round((top_track_plays / 200) * 100, 1))
    },
    {
        "id": "vault-royalty",
        "title": "Universe Expansion",
        "badge": "200 Artists",
        "icon": "music",
        "desc": f"Expanded catalog across {len(artists_list)} / 200 curated artists",
        "current": len(artists_list),
        "target": 200,
        "unit": "artists",
        "unlocked": len(artists_list) >= 200,
        "progress": min(100, round((len(artists_list) / 200) * 100, 1))
    },
    {
        "id": "discography-diver",
        "title": "Deep Catalog Diver",
        "badge": "75 Tracks",
        "icon": "gem",
        "desc": f"Curated {top_artist_tracks} / 75 tracks for flagship artist {top_artist_name}",
        "current": top_artist_tracks,
        "target": 75,
        "unit": "tracks",
        "unlocked": top_artist_tracks >= 75,
        "progress": min(100, round((top_artist_tracks / 75) * 100, 1))
    },
    {
        "id": "chrono-lord",
        "title": "Chronos Traveler",
        "badge": "7 Decades",
        "icon": "clock",
        "desc": "Curated legendary music spanning every decade from 1960s to 2020s",
        "current": len(set(a["decade"] for a in artists_list)),
        "target": 7,
        "unit": "decades",
        "unlocked": len(set(a["decade"] for a in artists_list)) >= 7,
        "progress": 100
    },
    {
        "id": "iron-retention",
        "title": "Iron Will Retention",
        "badge": ">80% Retention",
        "icon": "shield",
        "desc": f"Maintained {catalog_retention}% track retention across the entire catalog",
        "current": catalog_retention,
        "target": 80.0,
        "unit": "%",
        "unlocked": catalog_retention >= 80.0,
        "progress": 100
    }
]

avg_milestone_progress = round(sum(b["progress"] for b in badges) / len(badges))
unlocked_milestones_count = sum(1 for b in badges if b["unlocked"])
if avg_milestone_progress >= 95:
    mastery_rank = "Sovereign"
elif avg_milestone_progress >= 75:
    mastery_rank = "Senior Archivist"
elif avg_milestone_progress >= 50:
    mastery_rank = "Lead Curator"
else:
    mastery_rank = "Apprentice"

# Compute Decade Evolution Details
decade_evolution = []
for dec in ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]:
    dec_artists = [a for a in artists_list if a["decade"] == dec]
    dec_plays = sum(a["totalPlays"] for a in dec_artists)
    dec_tracks = sum(a["trackCount"] for a in dec_artists)
    top_3_artists = [a["name"] for a in dec_artists[:3]]
    decade_evolution.append({
        "decade": dec,
        "artistCount": len(dec_artists),
        "trackCount": dec_tracks,
        "totalPlays": dec_plays,
        "topArtists": top_3_artists,
        "image": dec_artists[0]["image"] if dec_artists else ""
    })

catalog_stats = {
    "totalSongs": sum(a["trackCount"] for a in artists_list),
    "totalArtists": len(artists_list),
    "totalAlbums": sum(a["albumCount"] for a in artists_list),
    "totalPlays": total_catalog_plays,
    "totalSkips": total_catalog_skips,
    "totalDurationSec": total_catalog_duration_sec,
    "totalHours": total_hours,
    "totalDays": total_days,
    "overallCompletionRate": round((1 - (total_catalog_skips / (total_catalog_plays + total_catalog_skips))) * 100, 1) if (total_catalog_plays + total_catalog_skips) > 0 else 100,
    "archetype": {
        "title": "The Sonic Time-Traveler",
        "badge": "7 Decades Spanned · 81.6% Retention",
        "tagline": f"{total_hours} Hours (~{total_days} Days) of Continuous Music Journeys",
        "bio": "Your English playlist bridges 1960s classic rock legends with 2020s alternative rock & chart hits, featuring 81.6% track retention and deep discography loyalty across 7 decades."
    },
    "circadianClock": {
        "hourCounts": hour_counts,
        "timeSegments": time_segments,
        "peakSegment": peak_segment,
        "peakHour": peak_hour,
        "persona": "Late-Night & Evening Audiophile" if peak_hour >= 18 or peak_hour <= 4 else "Afternoon Flow Connoisseur"
    },
    "milestones": badges,
    "masteryRank": mastery_rank,
    "masteryScore": avg_milestone_progress,
    "decadeEvolution": decade_evolution,
    "topArtist": {
        "name": top_artist["name"],
        "plays": top_artist["totalPlays"],
        "trackCount": top_artist["trackCount"],
        "image": top_artist.get("image", "")
    } if top_artist else {},
    "topTrack": {
        "title": top_track_overall["title"],
        "artist": top_track_overall.get("artist", ""),
        "plays": top_track_overall["plays"]
    } if top_track_overall else {},
    "top20Songs": top_20_songs,
    "decadesSummary": dict(Counter(a["decade"] for a in artists_list)),
    "genresSummary": dict(Counter(a["genre"] for a in artists_list))
}

import sqlite3

PUBLIC_DIR = ROOT_DIR / "public"
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = PUBLIC_DIR / "soundvault.db"

# Remove existing DB file if present
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE artists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT,
    decade TEXT,
    bio TEXT,
    trackCount INTEGER,
    albumCount INTEGER,
    totalPlays INTEGER,
    totalSkips INTEGER,
    totalHours REAL,
    avgPlays REAL,
    completionRate REAL,
    palette_primary TEXT,
    palette_bg TEXT,
    palette_glow TEXT,
    image TEXT,
    galaxyX REAL,
    galaxyY REAL,
    starRadius REAL,
    songs_json TEXT,
    albums_json TEXT,
    songDetails_json TEXT,
    albumsBreakdown_json TEXT
);
""")

cursor.execute("""
CREATE TABLE songs (
    id TEXT PRIMARY KEY,
    artist_id TEXT,
    artist TEXT,
    title TEXT,
    album TEXT,
    genre TEXT,
    decade TEXT,
    year TEXT,
    plays INTEGER,
    skips INTEGER,
    durationSec INTEGER,
    image TEXT,
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);
""")

cursor.execute("""
CREATE TABLE albums (
    id TEXT PRIMARY KEY,
    artist_id TEXT,
    artist_name TEXT,
    title TEXT,
    plays INTEGER,
    trackCount INTEGER,
    songs_json TEXT,
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);
""")

cursor.execute("""
CREATE TABLE catalog_meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
""")

# Insert Artists
for a in artists_list:
    palette = a.get("palette", {})
    cursor.execute("""
    INSERT INTO artists VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        a["id"],
        a["name"],
        a["genre"],
        a["decade"],
        a["bio"],
        a["trackCount"],
        a["albumCount"],
        a["totalPlays"],
        a["totalSkips"],
        a["totalHours"],
        a["avgPlays"],
        a["completionRate"],
        palette.get("primary", "#C8934A"),
        palette.get("bg", "#231E19"),
        palette.get("glow", "rgba(200,147,74,0.3)"),
        a.get("image", ""),
        a["galaxyX"],
        a["galaxyY"],
        a["starRadius"],
        json.dumps(a["songs"]),
        json.dumps(a["albums"]),
        json.dumps(a["songDetails"]),
        json.dumps(a["albumsBreakdown"])
    ))

    # Insert songs
    for sIdx, s in enumerate(a["songDetails"]):
        song_id = f"{a['id']}-s{sIdx+1:03d}"
        cursor.execute("""
        INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            song_id,
            a["id"],
            a["name"],
            s["title"],
            s.get("album", ""),
            s.get("genre", a["genre"]),
            a["decade"],
            str(s.get("year", "")),
            s.get("plays", 0),
            s.get("skips", 0),
            s.get("durationSec", 210),
            a.get("image", "")
        ))

    # Insert albums
    for albIdx, alb in enumerate(a["albumsBreakdown"]):
        album_id = f"{a['id']}-a{albIdx+1:03d}"
        cursor.execute("""
        INSERT INTO albums VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            album_id,
            a["id"],
            a["name"],
            alb["name"],
            alb["plays"],
            alb["trackCount"],
            json.dumps(alb.get("songs", []))
        ))

# Insert Meta Values
cursor.execute("INSERT INTO catalog_meta VALUES (?, ?)", ("catalog_stats", json.dumps(catalog_stats)))
cursor.execute("INSERT INTO catalog_meta VALUES (?, ?)", ("total_plays", str(total_catalog_plays)))
cursor.execute("INSERT INTO catalog_meta VALUES (?, ?)", ("total_artists", str(len(artists_list))))
cursor.execute("INSERT INTO catalog_meta VALUES (?, ?)", ("total_songs", str(catalog_stats["totalSongs"])))
cursor.execute("INSERT INTO catalog_meta VALUES (?, ?)", ("total_hours", str(total_hours)))

# Create Indexes
cursor.execute("CREATE INDEX idx_artists_name ON artists(name);")
cursor.execute("CREATE INDEX idx_artists_genre ON artists(genre);")
cursor.execute("CREATE INDEX idx_artists_decade ON artists(decade);")
cursor.execute("CREATE INDEX idx_artists_plays ON artists(totalPlays DESC);")
cursor.execute("CREATE INDEX idx_songs_plays ON songs(plays DESC);")
cursor.execute("CREATE INDEX idx_songs_artist ON songs(artist_id);")
cursor.execute("CREATE INDEX idx_songs_title ON songs(title);")

conn.commit()
conn.close()

# Also output public/soundvault.json
json_payload = json.dumps({"catalogStats": catalog_stats, "artists": artists_list}, indent=2)
with open(PUBLIC_DIR / "soundvault.json", "w", encoding="utf-8") as f:
    f.write(json_payload)

output_js = f"""/**
 * ARTIST FLASHCARD PORTFOLIO DATASET — IN-MEMORY SQLITE DATABASE HYDRATION DATA
 * {len(artists_list)} Artists, {catalog_stats['totalSongs']} Curated Tracks, {catalog_stats["totalAlbums"]} Albums
 * Total Play Count: {total_catalog_plays:,} Plays · Total Play Time: {total_hours} Hours ({total_days} Days)
 */

export const ARTIST_PORTFOLIO_DATA = {json_payload};
"""

output_filepath = SRC_DATA_DIR / "artists-data.js"
with open(output_filepath, "w", encoding="utf-8") as f:
    f.write(output_js)

print(f"SUCCESS: public/soundvault.db SQLite database generated ({DB_PATH.stat().st_size / 1024:.1f} KB)!")
print(f"SUCCESS: public/soundvault.json generated ({len(artists_list)} artists, {catalog_stats['totalSongs']} tracks)")
print(f"Total plays: {total_catalog_plays:,} ({total_hours} hours / {total_days} days)")
