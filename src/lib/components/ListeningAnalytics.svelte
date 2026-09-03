<script>
  import { Clock, Trophy, Sparkles } from 'lucide-svelte';

  let { portfolio } = $props();
  const stats = $derived(portfolio.catalogStats || {});
  const decadesSummary = $derived(stats.decadesSummary || {});
  const decades = $derived(Object.keys(decadesSummary).sort());

  const ERA_COLORS = {
    '1960s': '#D97706',
    '1970s': '#E8443A',
    '1980s': '#C25E34',
    '1990s': '#9C6B28',
    '2000s': '#6B6255',
    '2010s': '#9E9484',
    '2020s': '#EAE4D9'
  };

  const totalArtists = $derived(stats.totalArtists || 149);
</script>

<div class="analytics-card surface-noise">
  <div class="analytics-header">
    <div class="analytics-title-row">
      <div>
        <h2>Listening Analytics</h2>
        <p>Catalog archive across {totalArtists} artists, {(stats.totalSongs || 623).toLocaleString()} tracks, and {(stats.totalPlays || 4890).toLocaleString()} plays</p>
      </div>

      <div class="analytics-quick-tools">
        <button type="button" class="btn-analytics-tool" onclick={() => portfolio.openClock()} title="View 24-Hour Circadian Rhythm">
          <Clock size={11} strokeWidth={2} />
          <span>24h Clock</span>
        </button>
        <button type="button" class="btn-analytics-tool" onclick={() => portfolio.openMilestones()} title="View Vault Achievements">
          <Trophy size={11} strokeWidth={2} />
          <span>Badges</span>
        </button>
        <button type="button" class="btn-analytics-tool" onclick={() => portfolio.openCapsule()} title="Export Shareable PNG Card">
          <Sparkles size={11} strokeWidth={2} />
          <span>Capsule</span>
        </button>
      </div>
    </div>
  </div>

  <div class="metrics-row">
    <!-- Card 1: Tape Counter Total Volume -->
    <div class="analytics-stat-card">
      <div class="stat-top-line">
        <span class="tape-wheel num">{(stats.totalPlays || 5286).toLocaleString()}</span>
        <span class="stat-meta-pill">Catalog Plays</span>
      </div>
      <div class="stat-prose-sub">Total verified streams logged</div>
    </div>

    <!-- Card 2: Retention Gauge -->
    <div class="analytics-stat-card">
      <div class="stat-top-line">
        <span class="tape-wheel num">{stats.overallCompletionRate || 81.7}%</span>
        <span class="stat-meta-pill">Retention</span>
      </div>
      <div class="meter-bar-track">
        <div class="meter-bar-fill" style="width: {stats.overallCompletionRate || 81.7}%"></div>
      </div>
      <div class="stat-prose-sub">Full discography playthrough rate</div>
    </div>

    <!-- Card 3: Top Artist -->
    <div class="analytics-stat-card">
      <div class="stat-top-line">
        <span class="stat-feature-title">{stats.topArtist ? stats.topArtist.name : 'Linkin Park'}</span>
        <span class="stat-meta-pill">Top Artist</span>
      </div>
      <div class="stat-prose-sub">
        Leads with <strong class="num">{stats.topArtist ? (stats.topArtist.plays || 400).toLocaleString() : 400}</strong> plays across {stats.topArtist ? stats.topArtist.albumCount : 22} albums
      </div>
    </div>

    <!-- Card 4: Top Cut -->
    <div class="analytics-stat-card">
      <div class="stat-top-line">
        <span class="stat-feature-title">"{stats.topTrack ? stats.topTrack.title : 'Babydoll'}"</span>
        <span class="stat-meta-pill">Top Cut</span>
      </div>
      <div class="stat-prose-sub">
        Most spun composition with <strong class="num">{stats.topTrack ? stats.topTrack.plays : 146}</strong> plays
      </div>
    </div>
  </div>

  <div class="era-dist-container">
    <div class="era-bar-header">
      <span>Era Distribution</span>
      <span class="num">1960s – 2020s</span>
    </div>
    <div class="era-stacked-bar">
      {#each decades as decade}
        {@const count = decadesSummary[decade]}
        {@const pct = ((count / totalArtists) * 100).toFixed(1)}
        {@const color = ERA_COLORS[decade] || '#C8934A'}
        <button
          type="button"
          class="era-segment"
          style="width: {pct}%; background-color: {color}"
          title="{decade}: {count} artists ({pct}%)"
          onclick={() => portfolio.activeDecade = decade}
        ></button>
      {/each}
    </div>

    <div class="era-legend-row">
      {#each decades as decade}
        {@const count = decadesSummary[decade]}
        {@const color = ERA_COLORS[decade] || '#C8934A'}
        <button
          type="button"
          class="era-legend-item"
          class:active={portfolio.activeDecade === decade}
          onclick={() => portfolio.activeDecade = (portfolio.activeDecade === decade ? 'all' : decade)}
        >
          <span class="era-legend-dot" style="background: {color}"></span>
          <span>{decade} ({count})</span>
        </button>
      {/each}
    </div>
  </div>
</div>

<style>
  .analytics-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    min-width: 0;
    position: relative;
    overflow: hidden;
  }

  .analytics-header { margin-bottom: 24px; }
  .analytics-title-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }
  .analytics-header h2 {
    font-family: var(--font-serif);
    font-size: 1.55rem;
    font-weight: 400;
    color: var(--linen);
    letter-spacing: 0.01em;
    line-height: 1.15;
    margin-bottom: 3px;
  }
  .analytics-header p {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    font-weight: 400;
  }

  .analytics-quick-tools {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .btn-analytics-tool {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 500;
    cursor: pointer;
    transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
  }

  .btn-analytics-tool:hover {
    border-color: var(--oxide);
    background: var(--surface-3);
    color: var(--linen);
  }

  /* Redesigned Studio Analytics 2x2 Grid */
  .metrics-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 22px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(234, 228, 217, 0.06);
  }
  
  .analytics-stat-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 6px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 12px 14px;
    min-width: 0;
  }

  .stat-top-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 4px;
  }

  .tape-wheel {
    font-family: var(--font-mono);
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--linen);
    letter-spacing: 0.025em;
    line-height: 1;
  }

  .stat-feature-title {
    font-family: var(--font-mono);
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--linen);
    line-height: 1.2;
    letter-spacing: 0.01em;
  }

  .stat-meta-pill {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    font-weight: 600;
    color: var(--oxide);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 2px 6px;
    border-radius: 2px;
    white-space: nowrap;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    flex-shrink: 0;
  }

  .stat-prose-sub {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    line-height: 1.4;
    letter-spacing: 0.015em;
  }
  .stat-prose-sub strong {
    color: var(--linen);
    font-weight: 600;
  }

  .meter-bar-track {
    width: 100%;
    height: 3px;
    background: var(--groove);
    border-radius: 1px;
    overflow: hidden;
    margin: 4px 0 6px;
  }
  .meter-bar-fill {
    height: 100%;
    background: var(--oxide);
    border-radius: 1px;
  }

  .era-dist-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: auto;
  }

  .era-bar-header {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
  }

  .era-stacked-bar {
    width: 100%;
    height: 4px;
    background: var(--surface-2);
    border-radius: 2px;
    display: flex;
    overflow: hidden;
    gap: 1px;
  }

  .era-segment {
    height: 100%;
    cursor: pointer;
    border: none;
    padding: 0;
    transition: opacity 0.15s ease;
  }
  .era-segment:hover { opacity: 0.8; }

  .era-legend-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 12px;
    margin-top: 2px;
  }

  .era-legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
    font-family: var(--font-mono);
    font-size: 0.64rem;
    color: var(--text-muted);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: color 0.15s ease;
  }
  .era-legend-item:hover, .era-legend-item.active {
    color: var(--linen);
  }

  .era-legend-dot {
    width: 4px;
    height: 4px;
    border-radius: 1px;
  }

  @media (max-width: 800px) {
    .metrics-row {
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }
  }
</style>
