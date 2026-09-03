<script>
  let { portfolio } = $props();
  const topSongs = $derived(portfolio.catalogStats?.top20Songs || []);
</script>

<div class="track-ticker-bar">
  <div class="ticker-label">
    <span class="ticker-live-dot"></span>
    <span class="ticker-tag">TOP TRACKS</span>
  </div>

  <div class="ticker-marquee-wrap">
    <div class="ticker-track">
      <!-- Repeat twice for seamless infinite marquee loop -->
      {#each [1, 2] as _}
        {#each topSongs as song, idx}
          {@const artistObj = portfolio.allArtists.find(a => a.name === song.artist) || portfolio.allArtists[0]}
          <button 
            type="button" 
            class="ticker-item"
            onclick={() => { if (artistObj) portfolio.openModal(artistObj); }}
            title="Inspect {song.artist}"
          >
            <span class="ticker-rank num">#{idx + 1}</span>
            <span class="ticker-song">{song.title}</span>
            <span class="ticker-by">by</span>
            <span class="ticker-artist">{song.artist || 'Legend'}</span>
            <span class="ticker-badge num">{song.plays} plays</span>
            <span class="ticker-sep">·</span>
          </button>
        {/each}
      {/each}
    </div>
  </div>
</div>

<style>
  .track-ticker-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 34px;
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    backdrop-filter: blur(16px);
    z-index: 100;
    display: flex;
    align-items: center;
    overflow: hidden;
  }

  .ticker-label {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 0 14px;
    height: 100%;
    background: var(--surface-2);
    border-right: 1px solid var(--border);
    flex-shrink: 0;
    z-index: 2;
  }

  .ticker-live-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #10B981;
  }

  .ticker-tag {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    white-space: nowrap;
  }

  .ticker-marquee-wrap {
    display: flex;
    overflow: hidden;
    white-space: nowrap;
    width: 100%;
  }

  .ticker-track {
    display: flex;
    align-items: center;
    gap: 14px;
    animation: marqueeScroll 45s linear infinite;
    will-change: transform;
  }

  .track-ticker-bar:hover .ticker-track {
    animation-play-state: paused;
  }

  @keyframes marqueeScroll {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
  }

  .ticker-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: none;
    color: var(--text-secondary);
    font-family: var(--font-mono);
    font-size: 0.7rem;
    cursor: pointer;
    padding: 0 4px;
    transition: color 0.15s ease;
  }

  .ticker-item:hover {
    color: var(--text-primary);
  }

  .ticker-rank {
    color: var(--text-muted);
    font-weight: 600;
  }
  .ticker-song {
    color: var(--text-primary);
    font-weight: 600;
  }
  .ticker-by {
    color: var(--text-muted);
    font-size: 0.65rem;
  }
  .ticker-artist {
    color: var(--text-secondary);
    font-weight: 500;
  }
  .ticker-badge {
    font-size: 0.65rem;
    color: var(--text-muted);
  }
  .ticker-sep {
    color: rgba(255, 255, 255, 0.12);
    margin-left: 6px;
  }
</style>
