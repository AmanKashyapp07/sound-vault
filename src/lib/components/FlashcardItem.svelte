<script>
  import { RotateCw, Swords, ArrowRight } from 'lucide-svelte';

  let { artist, portfolio } = $props();

  let isFlipped = $state(false);

  const p       = $derived(artist.palette || {});
  const primary = $derived(p.primary || '#C8934A');
  const bg      = $derived(p.bg || '#231E19');

  function getInitials(name) {
    if (!name) return '◈';
    const words = name.trim().split(/\s+/).filter(w => /[a-zA-Z]/.test(w[0]));
    if (words.length === 0) return name.slice(0, 2).toUpperCase();
    if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }

  const initials    = $derived(getInitials(artist.name));
  const songDetails = $derived(artist.songDetails || []);
  const topTracks   = $derived(songDetails.slice(0, 4));
  const maxPlays    = $derived(songDetails[0]?.plays || 1);
</script>

<div
  class="fc-wrapper"
  class:flipped={isFlipped}
  role="region"
  aria-label="{artist.name} card"
>
  <div class="fc-inner">

    <!-- ── FRONT (Crate Spine Left-Edge) ───────────────────────── -->
    <div class="fc-face fc-front surface-noise" style="border-left: 3px solid {primary};">
      
      <div class="fc-main-content">
        <!-- Header row: Avatar Sleeve + Decade Badge -->
        <div class="fc-header-row">
          <div class="artist-sleeve-thumb" style="background: {bg}; border: 1px solid {primary}40">
            {#if artist.image}
              <img src={artist.image} alt={artist.name} class="artist-img-thumb" loading="lazy" />
            {:else}
              <span class="initials-fallback" style="color: {primary}">{initials}</span>
            {/if}
          </div>
          
          <div class="fc-badges-wrap">
            <span class="fc-decade-pill num">{artist.decade}</span>
          </div>
        </div>

        <!-- Artist Identity (Fixed Height for Perfect Consistency) -->
        <div class="fc-identity-box">
          <h3 class="fc-artist-title" title={artist.name}>{artist.name}</h3>
          <div class="fc-genre-sub">{artist.genre} · {artist.decade}</div>
        </div>

        <!-- Standardized 3-Stat Metric Strip -->
        <div class="fc-stats-strip">
          <div class="fc-stat-col">
            <span class="fc-stat-num num">{artist.totalPlays.toLocaleString()}</span>
            <span class="fc-stat-lbl">Plays</span>
          </div>
          <div class="fc-stat-divider"></div>
          <div class="fc-stat-col">
            <span class="fc-stat-num num">{artist.albumCount}</span>
            <span class="fc-stat-lbl">{artist.albumCount === 1 ? 'Album' : 'Albums'}</span>
          </div>
          <div class="fc-stat-divider"></div>
          <div class="fc-stat-col">
            <span class="fc-stat-num num">{artist.trackCount}</span>
            <span class="fc-stat-lbl">Tracks</span>
          </div>
        </div>

        <!-- Consistent 4-Slot Tracklist Box -->
        <div class="fc-tracklist-box">
          {#each topTracks as song, idx}
            {@const pct = Math.max(8, Math.round((song.plays / maxPlays) * 100))}
            <div class="fc-track-row" title="{song.title} ({song.plays} plays)">
              <span class="fc-track-idx num">{idx + 1}</span>
              <span class="fc-track-title">{song.title}</span>
              <div class="fc-track-sparkline-track">
                <div class="fc-track-sparkline-bar" style="width: {pct}%; background: {primary}"></div>
              </div>
              <span class="fc-track-plays num" class:highlight={song.plays >= 30}>{song.plays}</span>
            </div>
          {/each}
        </div>
      </div>

      <!-- Consistent Action Bar -->
      <div class="fc-actions">
        <button 
          type="button" 
          class="fc-btn fc-btn-main" 
          onclick={() => portfolio.openModal(artist)}
          title="Open complete discography and liner notes"
        >
          <span>View Discography</span>
          <ArrowRight size={11} />
        </button>
        <div class="fc-actions-sub">
          <button 
            type="button" 
            class="fc-btn fc-btn-sec" 
            onclick={() => isFlipped = true}
            title="Flip card for complete tracklist & bio"
          >
            <RotateCw size={10} />
            <span>Tracklist</span>
          </button>
          <button 
            type="button" 
            class="fc-btn fc-btn-battle" 
            onclick={() => portfolio.openBattle(artist)}
            title="Launch Artist Battle Arena against a rival"
          >
            <Swords size={10} />
            <span>VS</span>
          </button>
        </div>
      </div>

    </div>

    <!-- ── BACK ────────────────────────────────────────────────── -->
    <div class="fc-face fc-back surface-noise" style="border-left: 3px solid {primary};">
      <div class="fc-back-header">
        <div class="fc-back-title-wrap">
          <h3 class="fc-back-name">{artist.name}</h3>
          <span class="fc-back-meta">{artist.genre} · {artist.decade}</span>
        </div>
        <button
          type="button"
          class="btn-flip-back"
          onclick={(e) => { e.stopPropagation(); isFlipped = false; }}
          title="Flip back to front"
        >
          ↩ Front
        </button>
      </div>

      {#if artist.bio}
        <p class="fc-back-bio">{artist.bio.slice(0, 180)}…</p>
      {/if}

      <div class="fc-back-scroll-list">
        <div class="fc-back-list-hdr">
          <span>Catalog Tracks ({artist.trackCount})</span>
          <span class="num">{artist.totalPlays} plays</span>
        </div>
        {#each songDetails as song, sIdx}
          <div class="fc-back-item">
            <span class="fc-back-item-title num">{sIdx + 1}. {song.title}</span>
            <span class="fc-back-item-plays num">{song.plays}</span>
          </div>
        {/each}
      </div>

      <div class="fc-actions">
        <button 
          type="button" 
          class="fc-btn fc-btn-main" 
          onclick={() => portfolio.openModal(artist)}
        >
          <span>Full Breakdown</span>
          <ArrowRight size={11} />
        </button>
        <div class="fc-actions-sub">
          <button 
            type="button" 
            class="fc-btn fc-btn-battle" 
            style="flex: 1;"
            onclick={() => portfolio.openBattle(artist)}
          >
            <Swords size={10} />
            <span>Battle Rival</span>
          </button>
        </div>
      </div>
    </div>

  </div>
</div>

<style>
  /* ── 3D Card Shell ────────────────────────────── */
  .fc-wrapper {
    perspective: 1000px;
    height: 385px;
  }

  .fc-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    border-radius: var(--r-md);
  }

  .fc-wrapper.flipped .fc-inner {
    transform: rotateY(180deg);
  }

  .fc-face {
    position: absolute;
    inset: 0;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: var(--r-md);
    background: var(--surface);
    border: 1px solid var(--border);
    border-bottom: 2px solid var(--groove);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    padding: 16px 18px 14px;
    box-sizing: border-box;
  }

  .fc-front {
    z-index: 2;
    pointer-events: auto;
  }

  .fc-back {
    transform: rotateY(180deg);
    background: var(--surface-2);
    z-index: 1;
    pointer-events: none;
  }

  .fc-wrapper.flipped .fc-front {
    z-index: 1;
    pointer-events: none;
  }

  .fc-wrapper.flipped .fc-back {
    z-index: 10;
    pointer-events: auto;
  }

  .fc-main-content {
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
    min-height: 0;
  }

  /* ── Header: Square Album Art Sleeve + Decade ──── */
  .fc-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .artist-sleeve-thumb {
    width: 44px;
    height: 44px;
    border-radius: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.55);
  }

  .artist-img-thumb {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .initials-fallback {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    font-weight: 700;
  }

  .fc-decade-pill {
    background: var(--surface-2);
    border: 1px solid var(--border);
    padding: 2px 7px;
    border-radius: var(--r-sm);
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.04em;
  }

  /* ── Identity (Locked Height for 100% Uniformity) ── */
  .fc-identity-box {
    min-height: 44px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2px;
  }

  .fc-artist-title {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--linen);
    line-height: 1.2;
    letter-spacing: -0.01em;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin: 0;
  }

  .fc-genre-sub {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* ── 3-Stat Metric Strip ───────────────────────── */
  .fc-stats-strip {
    display: flex;
    align-items: center;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 3px;
    overflow: hidden;
  }

  .fc-stat-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5px 6px;
    gap: 1px;
  }

  .fc-stat-num {
    font-family: var(--font-mono);
    font-size: 0.86rem;
    font-weight: 700;
    color: var(--linen);
    line-height: 1;
  }

  .fc-stat-lbl {
    font-family: var(--font-mono);
    font-size: 0.52rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    text-transform: uppercase;
  }

  .fc-stat-divider {
    width: 1px;
    height: 24px;
    background: var(--border);
    flex-shrink: 0;
  }

  /* ── 4-Slot Tracklist Box ──────────────────────── */
  .fc-tracklist-box {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-height: 98px;
  }

  .fc-track-row {
    display: grid;
    grid-template-columns: 14px 1fr 38px 24px;
    align-items: center;
    gap: 6px;
    padding: 2.5px 4px;
    border-radius: 2px;
    transition: background 0.12s ease;
  }

  .fc-track-row:hover {
    background: rgba(234, 228, 217, 0.04);
  }

  .fc-track-idx {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--text-muted);
    text-align: right;
  }

  .fc-track-title {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--linen);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .fc-track-sparkline-track {
    height: 3px;
    background: var(--groove);
    border-radius: 2px;
    overflow: hidden;
  }

  .fc-track-sparkline-bar {
    height: 100%;
    border-radius: 2px;
    transition: width 0.3s ease;
  }

  .fc-track-plays {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
    text-align: right;
    font-variant-numeric: tabular-nums;
  }

  .fc-track-plays.highlight {
    color: var(--oxide);
    font-weight: 700;
  }

  /* ── Action Buttons ────────────────────────────── */
  .fc-actions {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding-top: 10px;
    border-top: 1px solid var(--border);
    flex-shrink: 0;
  }

  .fc-actions-sub {
    display: flex;
    gap: 6px;
  }

  .fc-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 700;
    border-radius: 2px;
    cursor: pointer;
    transition: all 0.14s ease;
    letter-spacing: 0.02em;
    box-sizing: border-box;
  }

  .fc-btn-main {
    width: 100%;
    height: 32px;
    background: color-mix(in srgb, var(--oxide) 10%, transparent);
    border: 1px solid var(--oxide);
    color: var(--oxide);
  }

  .fc-btn-main:hover {
    background: var(--oxide);
    color: #0D0B09;
  }

  .fc-btn-sec {
    flex: 1;
    height: 28px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-muted);
  }

  .fc-btn-sec:hover {
    border-color: var(--oxide);
    color: var(--linen);
  }

  .fc-btn-battle {
    height: 28px;
    padding: 0 14px;
    background: var(--surface-2);
    border: 1px solid rgba(232, 68, 58, 0.35);
    color: var(--signal);
  }

  .fc-btn-battle:hover {
    border-color: var(--signal);
    background: rgba(232, 68, 58, 0.1);
  }

  /* ── Card Back Details ─────────────────────────── */
  .fc-back-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }

  .fc-back-name {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--linen);
    margin: 0;
    line-height: 1.2;
  }

  .fc-back-meta {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
    display: block;
    margin-top: 2px;
  }

  .btn-flip-back {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 2px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.64rem;
    padding: 3px 8px;
    cursor: pointer;
    transition: all 0.14s ease;
  }

  .btn-flip-back:hover {
    color: var(--linen);
    border-color: var(--oxide);
  }

  .fc-back-bio {
    font-family: var(--font-mono);
    font-size: 0.66rem;
    color: var(--text-secondary);
    line-height: 1.45;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .fc-back-scroll-list {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding-right: 2px;
  }

  .fc-back-list-hdr {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .fc-back-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0;
    border-bottom: 1px solid rgba(234, 228, 217, 0.04);
    font-size: 0.68rem;
  }

  .fc-back-item-title {
    font-family: var(--font-mono);
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 190px;
  }

  .fc-back-item-plays {
    font-family: var(--font-mono);
    color: var(--text-muted);
  }
</style>
