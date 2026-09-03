<script>
  import { ChevronRight } from 'lucide-svelte';

  let { portfolio } = $props();
  const stats = $derived(portfolio.catalogStats || {});
  const decadeEvolution = $derived(stats.decadeEvolution || []);
  const maxPlays = $derived(Math.max(...decadeEvolution.map(d => d.totalPlays || 1), 1));
</script>

<div class="decade-horizon-container surface-noise">
  <div class="decade-horizon-header">
    <div class="dhh-left">
      <h3>Decade Evolution Index</h3>
      <p>Continuous trajectory across 7 distinct eras of recorded music — select any node to filter</p>
    </div>

    <div class="dhh-summary-pill">
      <span>7 ERAS RECORDED</span>
      <strong class="num">{(stats.totalPlays || 4890).toLocaleString()} Plays</strong>
    </div>
  </div>

  <!-- Horizontal Scrollable Decade Cards -->
  <div class="decade-strip-scroll">
    {#each decadeEvolution as d}
      {@const isActive = portfolio.activeDecade === d.decade}
      {@const fillPct = Math.round(((d.totalPlays || 0) / maxPlays) * 100)}
      <button 
        type="button" 
        class="decade-horizon-card"
        class:active={isActive}
        onclick={() => portfolio.activeDecade = (isActive ? 'all' : d.decade)}
        title="Filter universe by {d.decade}"
      >
        <div class="dhc-top">
          <span class="dhc-year num">{d.decade}</span>
          <span class="dhc-tracks-badge num">{d.trackCount} trk</span>
        </div>

        <div class="dhc-plays-row">
          <span class="dhc-plays-num num">{d.totalPlays.toLocaleString()}</span>
          <span class="dhc-plays-unit">plays</span>
        </div>

        <div class="dhc-artists-preview">
          {#each d.topArtists.slice(0, 2) as artistName}
            <span class="dhc-artist-name">{artistName}</span>
          {/each}
        </div>

        <!-- Proportional tape fill gauge -->
        <div class="dhc-gauge-track">
          <div class="dhc-gauge-fill" style="width: {fillPct}%"></div>
        </div>

        <div class="dhc-footer">
          <span class="dhc-filter-label">{isActive ? 'Filtering era' : 'Explore era'}</span>
          <ChevronRight size={11} />
        </div>
      </button>
    {/each}
  </div>
</div>

<style>
  .decade-horizon-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 22px 26px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: relative;
    overflow: hidden;
  }

  .decade-horizon-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }

  .dhh-left {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .dhh-left h3 {
    font-family: var(--font-serif);
    font-size: 1.45rem;
    font-weight: 400;
    color: var(--linen);
    letter-spacing: -0.01em;
  }

  .dhh-left p {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .dhh-summary-pill {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 5px 12px;
  }
  .dhh-summary-pill span {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
  }
  .dhh-summary-pill strong {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--linen);
  }

  .decade-strip-scroll {
    display: grid;
    grid-template-columns: repeat(7, minmax(130px, 1fr));
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 4px;
  }

  .decade-horizon-card {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 8px;
    cursor: pointer;
    text-align: left;
    transition: border-color 0.15s ease, background 0.15s ease;
    min-height: 130px;
    position: relative;
    overflow: hidden;
  }

  .decade-horizon-card:hover {
    background: var(--surface-3);
    border-color: var(--border-hover);
  }

  .decade-horizon-card.active {
    background: var(--surface-3);
    border-color: var(--oxide);
  }

  .dhc-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4px;
  }

  .dhc-year {
    font-family: var(--font-mono);
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--linen);
  }

  .dhc-tracks-badge {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 1px 5px;
    border-radius: 2px;
  }

  .dhc-plays-row {
    display: flex;
    align-items: baseline;
    gap: 4px;
  }

  .dhc-plays-num {
    font-family: var(--font-mono);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--linen);
  }
  .decade-horizon-card.active .dhc-plays-num {
    color: var(--oxide);
  }

  .dhc-plays-unit {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
  }

  .dhc-artists-preview {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin: 2px 0;
    min-width: 0;
  }

  .dhc-artist-name {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-secondary);
    line-height: 1.25;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    letter-spacing: 0.01em;
  }

  /* Tape Gauge */
  .dhc-gauge-track {
    width: 100%;
    height: 3px;
    background: var(--groove);
    border-radius: 1px;
    overflow: hidden;
    margin-top: 2px;
  }

  .dhc-gauge-fill {
    height: 100%;
    background: var(--oxide);
    border-radius: 1px;
  }
  .decade-horizon-card.active .dhc-gauge-fill {
    background: var(--signal);
  }

  .dhc-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 600;
    color: var(--oxide);
    margin-top: 2px;
  }
  .decade-horizon-card.active .dhc-footer {
    color: var(--signal);
  }

  @media (max-width: 1024px) {
    .decade-strip-scroll {
      grid-template-columns: repeat(4, 1fr);
    }
  }

  @media (max-width: 768px) {
    .decade-horizon-header {
      flex-direction: column;
      align-items: flex-start;
    }
    .decade-strip-scroll {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
