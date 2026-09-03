<script>
  let { portfolio } = $props();
  const topArtists = $derived(portfolio.allArtists.slice(0, 15));
  const top20Songs = $derived(portfolio.catalogStats.top20Songs || []);

  function getInitials(name) {
    if (!name) return '◈';
    const words = name.trim().split(/\s+/).filter(w => /[a-zA-Z]/.test(w[0]));
    if (words.length === 0) return name.slice(0, 2).toUpperCase();
    if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }

  function formatRank(num) {
    return num < 10 ? `0${num}` : `${num}`;
  }
</script>

<div class="analytics-card surface-noise">
  <div class="analytics-header leaderboard-header-flex">
    <div>
      <h2>Leaderboard</h2>
      <p>
        {portfolio.leaderboardTab === 'artists' 
          ? 'Verified artist discographies' 
          : 'Top 20 tracked compositions'}
      </p>
    </div>
    <div class="leaderboard-tabs-wrap">
      <button 
        type="button"
        class="leaderboard-tab-btn" 
        class:active={portfolio.leaderboardTab === 'artists'}
        onclick={() => portfolio.leaderboardTab = 'artists'}
      >
        Artists
      </button>
      <button 
        type="button"
        class="leaderboard-tab-btn" 
        class:active={portfolio.leaderboardTab === 'songs'}
        onclick={() => portfolio.leaderboardTab = 'songs'}
      >
        Tracks
      </button>
    </div>
  </div>

  <div class="titans-list">
    {#if portfolio.leaderboardTab === 'artists'}
      {#each topArtists as artist, idx}
        {@const color = artist.palette ? artist.palette.primary : '#C8934A'}
        <div 
          class="titan-row"
          class:rank-1={idx === 0}
          class:rank-top5={idx > 0 && idx < 5}
          style="--row-spine: {color}"
          onclick={() => portfolio.openModal(artist)}
          role="button"
          tabindex="0"
          onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') portfolio.openModal(artist); }}
        >
          <div class="titan-left">
            <span class="titan-rank num">{formatRank(idx + 1)}</span>

            <div class="titan-avatar" style="background: {color}15; border: 1px solid {color}33;">
              {#if artist.image}
                <img src={artist.image} alt={artist.name} class="titan-img" loading="lazy" />
              {:else}
                {getInitials(artist.name)}
              {/if}
            </div>

            <div class="titan-info-wrap">
              <div class="titan-name" title={artist.name}>
                <span>{artist.name}</span>
              </div>
              <div class="titan-genre">{artist.genre} · {artist.albumCount} {artist.albumCount === 1 ? 'album' : 'albums'}</div>
            </div>
          </div>

          <div class="titan-right">
            <span class="titan-plays num">{artist.totalPlays.toLocaleString()}</span>
            <span class="titan-plays-lbl">plays</span>
          </div>
        </div>
      {/each}
    {:else}
      {#each top20Songs as song, idx}
        {@const color = song.palette ? song.palette.primary : '#C8934A'}
        {@const targetArtist = portfolio.allArtists.find(a => a.name.toLowerCase() === song.artist.toLowerCase())}
        <div 
          class="titan-row"
          class:rank-1={idx === 0}
          class:rank-top5={idx > 0 && idx < 5}
          style="--row-spine: {color}"
          onclick={() => targetArtist && portfolio.openModal(targetArtist)}
          role="button"
          tabindex="0"
          onkeydown={(e) => { if ((e.key === 'Enter' || e.key === ' ') && targetArtist) portfolio.openModal(targetArtist); }}
        >
          <div class="titan-left">
            <span class="titan-rank num">{formatRank(idx + 1)}</span>

            <div class="titan-avatar" style="background: {color}15; border: 1px solid {color}33;">
              {#if song.image}
                <img src={song.image} alt={song.artist} class="titan-img" loading="lazy" />
              {:else}
                {getInitials(song.artist)}
              {/if}
            </div>

            <div class="titan-info-wrap">
              <div class="titan-name" title={song.title}>
                <span>{song.title}</span>
              </div>
              <div class="titan-genre" title="{song.artist} • {song.album}">{song.artist} · {song.album}</div>
            </div>
          </div>

          <div class="titan-right">
            <span class="titan-plays num">{song.plays.toLocaleString()}</span>
            <span class="titan-plays-lbl">plays</span>
          </div>
        </div>
      {/each}
    {/if}
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

  .analytics-header { margin-bottom: 16px; }
  .analytics-header.leaderboard-header-flex {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 16px;
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

  .leaderboard-tabs-wrap {
    display: flex; align-items: center; gap: 2px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 2px;
    flex-shrink: 0;
  }
  .leaderboard-tab-btn {
    padding: 4px 10px;
    border-radius: 3px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 500;
    cursor: pointer;
    text-align: center;
    transition: color 0.15s ease, background 0.15s ease;
    white-space: nowrap;
  }
  .leaderboard-tab-btn:hover { color: var(--text-secondary); }
  .leaderboard-tab-btn.active {
    background: var(--surface);
    color: var(--linen);
    font-weight: 600;
    border: 1px solid var(--border);
  }

  .titans-list {
    display: flex;
    flex-direction: column;
    height: 320px;
    max-height: 320px;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: 4px;
    width: 100%;
    box-sizing: border-box;
  }
  .titans-list::-webkit-scrollbar { width: 4px; }
  .titans-list::-webkit-scrollbar-thumb { background: var(--groove); border-radius: 2px; }

  /* Physical Studio Table-List Row with Flush Left-Edge Border */
  .titan-row {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 7px 10px 7px 12px;
    border-left: 3px solid var(--row-spine, var(--groove));
    border-bottom: 1px solid rgba(234, 228, 217, 0.04);
    cursor: pointer;
    transition: background 0.15s ease, border-left-color 0.15s ease;
    gap: 12px;
    width: 100%;
    box-sizing: border-box;
    background: transparent;
  }

  .titan-row:hover {
    background: var(--surface-2);
  }

  .titan-row.rank-1 {
    border-left-color: var(--signal) !important;
    background: rgba(232, 68, 58, 0.03);
  }

  .titan-row.rank-top5 {
    border-left-color: var(--oxide) !important;
  }

  .titan-left {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
    flex: 1;
    overflow: hidden;
  }

  /* Two-Digit Rank Number */
  .titan-rank {
    width: 22px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    flex-shrink: 0;
  }

  .titan-row.rank-1 .titan-rank {
    color: var(--signal);
    font-weight: 700;
  }
  .titan-row.rank-top5 .titan-rank {
    color: var(--oxide);
  }

  /* Square Record Jacket Thumbnail */
  .titan-avatar {
    width: 28px;
    height: 28px;
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 700;
    color: var(--text-secondary);
    letter-spacing: 0.02em;
    flex-shrink: 0;
    overflow: hidden;
  }
  .titan-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .titan-info-wrap {
    min-width: 0;
    flex: 1;
    overflow: hidden;
  }
  .titan-name {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--linen);
    line-height: 1.25;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .titan-genre {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 1px;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .titan-right {
    flex-shrink: 0;
    display: flex;
    align-items: baseline;
    gap: 4px;
  }

  .titan-plays {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--linen);
  }
  .titan-row.rank-1 .titan-plays {
    color: var(--signal);
  }

  .titan-plays-lbl {
    font-size: 0.62rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }
</style>
