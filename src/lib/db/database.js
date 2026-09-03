import initSqlJs from 'sql.js';
import { ARTIST_PORTFOLIO_DATA } from '../data/artists-data.js';

let dbInstance = null;
let isReady = false;
const listeners = new Set();

/**
 * Initializes the in-memory SQLite WASM database from /soundvault.db
 */
export async function initSqliteDatabase() {
  if (dbInstance) return dbInstance;

  try {
    const SQL = await initSqlJs({
      locateFile: (file) => `/${file}`
    });

    // Fetch the binary SQLite database
    const response = await fetch('/soundvault.db');
    if (!response.ok) {
      throw new Error(`Failed to fetch soundvault.db: ${response.statusText}`);
    }

    const arrayBuffer = await response.arrayBuffer();
    dbInstance = new SQL.Database(new Uint8Array(arrayBuffer));
    isReady = true;

    // Attach to window in dev for debugging / SQL exploration
    if (typeof window !== 'undefined') {
      window.__soundvault_db = {
        db: dbInstance,
        query: runSqlQuery,
        exec: (sql) => runSqlQuery(sql)
      };
      console.log('⚡ [Soundvault] In-Memory SQLite WASM database initialized successfully!');
    }

    notifyListeners();
    return dbInstance;
  } catch (error) {
    console.warn('[Soundvault] SQLite WASM load error, falling back to cached snapshot:', error);
    isReady = false;
    return null;
  }
}

function notifyListeners() {
  for (const fn of listeners) {
    try { fn(dbInstance); } catch (e) { console.error(e); }
  }
}

export function onDatabaseReady(callback) {
  if (isReady && dbInstance) {
    callback(dbInstance);
  } else {
    listeners.add(callback);
  }
  return () => listeners.delete(callback);
}

/**
 * Execute a raw SQL query against the in-memory SQLite database
 * @param {string} sql
 * @param {Array|Object} params
 * @returns {Array<Object>}
 */
export function runSqlQuery(sql, params = []) {
  if (!dbInstance) {
    console.warn('[Soundvault DB] Database not ready yet for query:', sql);
    return [];
  }

  try {
    const stmt = dbInstance.prepare(sql);
    if (params && (Array.isArray(params) ? params.length > 0 : Object.keys(params).length > 0)) {
      stmt.bind(params);
    }

    const rows = [];
    while (stmt.step()) {
      rows.push(stmt.getAsObject());
    }
    stmt.free();
    return rows;
  } catch (err) {
    console.error('[Soundvault DB] SQL execution error:', err, 'SQL:', sql);
    return [];
  }
}

function mapArtistRow(row) {
  if (!row) return null;
  return {
    id: row.id,
    name: row.name,
    genre: row.genre,
    decade: row.decade,
    bio: row.bio,
    trackCount: Number(row.trackCount),
    albumCount: Number(row.albumCount),
    totalPlays: Number(row.totalPlays),
    totalSkips: Number(row.totalSkips),
    totalHours: Number(row.totalHours),
    avgPlays: Number(row.avgPlays),
    completionRate: Number(row.completionRate),
    palette: {
      primary: row.palette_primary || '#C8934A',
      bg: row.palette_bg || '#231E19',
      glow: row.palette_glow || 'rgba(200,147,74,0.3)'
    },
    image: row.image || '',
    galaxyX: Number(row.galaxyX),
    galaxyY: Number(row.galaxyY),
    starRadius: Number(row.starRadius),
    songs: row.songs_json ? JSON.parse(row.songs_json) : [],
    albums: row.albums_json ? JSON.parse(row.albums_json) : [],
    songDetails: row.songDetails_json ? JSON.parse(row.songDetails_json) : [],
    albumsBreakdown: row.albumsBreakdown_json ? JSON.parse(row.albumsBreakdown_json) : []
  };
}

/**
 * Retrieve all artists from SQLite
 */
export function getAllArtists() {
  if (!dbInstance) {
    return ARTIST_PORTFOLIO_DATA?.artists || [];
  }

  const rows = runSqlQuery('SELECT * FROM artists ORDER BY totalPlays DESC');
  return rows.map(mapArtistRow);
}

/**
 * Filter artists using SQL WHERE clauses
 */
export function filterArtistsSql({ search = '', decade = 'all', genre = 'all', sortBy = 'plays-desc' } = {}) {
  if (!dbInstance) {
    let result = (ARTIST_PORTFOLIO_DATA?.artists || []).slice();
    if (decade !== 'all') result = result.filter(a => a.decade === decade);
    if (genre !== 'all') result = result.filter(a => a.genre === genre);
    if (search.trim()) {
      const q = search.toLowerCase().trim();
      result = result.filter(a => a.name.toLowerCase().includes(q) || a.genre.toLowerCase().includes(q));
    }
    return result;
  }

  let sql = 'SELECT * FROM artists WHERE 1=1';
  const params = [];

  if (decade !== 'all') {
    sql += ' AND decade = ?';
    params.push(decade);
  }

  if (genre !== 'all') {
    sql += ' AND genre = ?';
    params.push(genre);
  }

  if (search && search.trim()) {
    sql += ' AND (name LIKE ? OR genre LIKE ? OR decade LIKE ? OR songs_json LIKE ? OR albums_json LIKE ?)';
    const term = `%${search.trim()}%`;
    params.push(term, term, term, term, term);
  }

  switch (sortBy) {
    case 'plays-desc':
      sql += ' ORDER BY totalPlays DESC';
      break;
    case 'hours-desc':
      sql += ' ORDER BY totalHours DESC';
      break;
    case 'tracks-desc':
      sql += ' ORDER BY trackCount DESC';
      break;
    case 'name-asc':
      sql += ' ORDER BY name ASC';
      break;
    case 'albums-desc':
      sql += ' ORDER BY albumCount DESC';
      break;
    case 'completion-desc':
      sql += ' ORDER BY completionRate DESC';
      break;
    default:
      sql += ' ORDER BY totalPlays DESC';
  }

  const rows = runSqlQuery(sql, params);
  return rows.map(mapArtistRow);
}

/**
 * Retrieve Catalog Meta Stats from SQLite
 */
export function getCatalogStats() {
  if (!dbInstance) {
    return ARTIST_PORTFOLIO_DATA?.catalogStats || {};
  }

  const rows = runSqlQuery("SELECT value FROM catalog_meta WHERE key = 'catalog_stats'");
  if (rows.length > 0 && rows[0].value) {
    return JSON.parse(rows[0].value);
  }
  return ARTIST_PORTFOLIO_DATA?.catalogStats || {};
}

/**
 * Retrieve Top Songs from SQLite
 */
export function getTopSongs(limit = 20) {
  if (!dbInstance) {
    return (ARTIST_PORTFOLIO_DATA?.catalogStats?.top20Songs || []).slice(0, limit);
  }

  const rows = runSqlQuery('SELECT * FROM songs ORDER BY plays DESC LIMIT ?', [limit]);
  return rows.map(r => ({
    title: r.title,
    artist: r.artist,
    album: r.album,
    plays: Number(r.plays),
    skips: Number(r.skips),
    durationSec: Number(r.durationSec),
    genre: r.genre,
    decade: r.decade,
    artistId: r.artist_id,
    image: r.image
  }));
}
