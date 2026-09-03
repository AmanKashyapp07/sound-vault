<script>
  import { ChevronLeft, ChevronRight, RotateCw, Swords, ArrowRight } from 'lucide-svelte';

  let { portfolio } = $props();

  let isFlipped = $state(false);
  const artist = $derived(portfolio.filteredArtists[portfolio.currentSoloIndex] || null);

  $effect(() => {
    portfolio.currentSoloIndex;
    isFlipped = false;
  });

  function getInitials(name) {
    if (!name) return '◈';
    const words = name.trim().split(/\s+/).filter(w => /[a-zA-Z]/.test(w[0]));
    if (words.length === 0) return name.slice(0, 2).toUpperCase();
    if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }
</script> 

<div class="solo-deck-view">
  {#if !artist}
    <div class="empty-deck">No artists available in current filter.</div>
  {:else}
    {@const p = artist.palette || {}}
    {@const primary = p.primary || '#C8934A'}
    {@const bg = p.bg || '#231E19'}
    {@const songDetails = artist.songDetails || []}
    {@const topSongPreviews = songDetails.slice(0, 4)}

    <div class="solo-card-stage">
      <div 
        class="solo-card-inner"
        class:flipped={isFlipped}
      >
        <!-- FRONT -->
        <div class="flashcard-face flashcard-front surface-noise" style="border-left: 3px solid {primary};">
          <div>
            <div class="card-header-row">
              <div class="artist-avatar-sleeve" style="width:52px; height:52px; background:{bg}; border: 1px solid {primary}40;">
                {#if artist.image}
                  <img src={artist.image} alt={artist.name} class="artist-img-avatar" loading="lazy" />
                {:else}
                  {getInitials(artist.name)}
                {/if}
              </div>
              <div class="card-badges-group">
                <span class="card-plays-badge num">{artist.totalPlays.toLocaleString()} plays</span>
                <span class="card-decade-badge num">{artist.decade}</span>
              </div>
            </div>

            <div class="artist-identity-block">
              <h2 class="artist-card-name">{artist.name}</h2>
              <div class="artist-tagline">{artist.genre} · {artist.albumCount} {artist.albumCount === 1 ? 'album' : 'albums'}</div>
            </div>

            <div class="card-stats-ribbon">
              <div class="mini-stat-capsule">
                <span>TRACKS</span><strong class="num">{artist.trackCount}</strong>
              </div>
              <div class="mini-stat-capsule">
                <span>PLAYS</span><strong class="num">{artist.totalPlays}</strong>
              </div>
              <div class="mini-stat-capsule">
                <span>ALBUMS</span><strong class="num">{artist.albumCount}</strong>
              </div>
            </div>

            <div class="signature-tracks-box">
              {#each topSongPreviews as song, n}
                <div class="track-preview-item">
                  <div class="track-preview-left">
                    <span class="track-num num">{n + 1}</span>
                    <span class="track-name-text">{song.title}</span>
                  </div>
                  <span class="track-plays-pill num" class:highlight={song.plays >= 30}>{song.plays}p</span>
                </div>
              {/each}
            </div>
          </div>

          <div class="card-bottom-actions">
            <button type="button" class="btn-flip-card" onclick={() => isFlipped = true}>
              <RotateCw size={12} />
              <span>Tracklist</span>
            </button>
            <button type="button" class="btn-battle-card" onclick={() => portfolio.openBattle(artist)}>
              <Swords size={12} />
              <span>VS</span>
            </button>
            <button type="button" class="btn-inspect-modal" onclick={() => portfolio.openModal(artist)}>
              Discography
            </button>
          </div>
        </div>

        <!-- BACK -->
        <div class="flashcard-face flashcard-back surface-noise" style="border-left: 3px solid {primary};">
          <div>
            <div class="back-header">
              <h3>{artist.name}</h3>
              <button 
                type="button" 
                class="btn-unflip" 
                onclick={(e) => { e.stopPropagation(); isFlipped = false; }}
                onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.stopPropagation(); isFlipped = false; } }}
                title="Flip back to front"
              >
                Back ↩
              </button>
            </div>
            <p class="back-bio-text">{artist.bio}</p>
            <div class="back-tracklist-wrap">
              <div class="back-tracklist-label">
                {artist.trackCount} tracks logged ({artist.totalPlays} plays)
              </div>
              {#each songDetails as song, sIdx}
                <div class="back-track-item">
                  <span class="back-track-name num">{sIdx + 1}. {song.title}</span>
                  <span class="track-plays-pill num" class:highlight={song.plays >= 30}>{song.plays}p</span>
                </div>
              {/each}
            </div>
          </div>
          <div class="card-bottom-actions">
            <button type="button" class="btn-inspect-modal" style="width:100%" onclick={() => portfolio.openModal(artist)}>
              Full Discography Breakdown
            </button>
          </div>
        </div>

      </div>
    </div>

    <div class="deck-nav-controls">
      <button type="button" class="deck-nav-btn" title="Previous (← arrow)" onclick={portfolio.prevSoloCard}>
        <ChevronLeft size={16} />
      </button>
      <div class="deck-counter-badge num">
        {portfolio.currentSoloIndex + 1} of {portfolio.filteredArtists.length}
      </div>
      <button type="button" class="deck-nav-btn" title="Next (→ arrow)" onclick={portfolio.nextSoloCard}>
        <ChevronRight size={16} />
      </button>
    </div>
    <p class="deck-hint-text num">SPACE to flip / ← → to navigate / ESC to close</p>
  {/if}
</div>

<style>
  .solo-deck-view {
    display: flex; flex-direction: column; align-items: center;
    gap: 16px; padding: 12px 0;
  }

  .solo-card-stage {
    width: 100%; max-width: 480px; height: 460px;
    perspective: 1200px;
  }

  .solo-card-inner {
    position: relative; width: 100%; height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.4s var(--ease);
    border-radius: var(--r-md);
  }

  .solo-card-inner.flipped { transform: rotateY(180deg); }

  .flashcard-face {
    position: absolute; inset: 0;
    backface-visibility: hidden; -webkit-backface-visibility: hidden;
    border-radius: var(--r-md); padding: 24px 26px;
    display: flex; flex-direction: column; justify-content: space-between;
    background: var(--surface); border: 1px solid var(--border);
    border-bottom: 2px solid var(--groove);
  }

  .flashcard-front {
    z-index: 2;
    pointer-events: auto;
  }

  .flashcard-back {
    transform: rotateY(180deg);
    background: var(--surface-2);
    z-index: 1;
    pointer-events: none;
  }

  .solo-card-inner.flipped .flashcard-front {
    z-index: 1;
    pointer-events: none;
  }

  .solo-card-inner.flipped .flashcard-back {
    z-index: 10;
    pointer-events: auto;
  }

  .card-header-row {
    display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;
  }

  .artist-avatar-sleeve {
    border-radius: 2px;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-weight: 700; color: var(--linen);
    overflow: hidden;
  }
  .artist-img-avatar {
    width: 100%; height: 100%; object-fit: cover;
  }

  .card-badges-group { display: flex; align-items: center; gap: 6px; }
  .card-plays-badge {
    background: var(--surface-2); border: 1px solid var(--border);
    padding: 3px 8px; border-radius: 2px; font-family: var(--font-mono);
    font-size: 0.68rem; font-weight: 600; color: var(--oxide);
  }
  .card-decade-badge {
    background: var(--surface-3); border: 1px solid var(--border);
    padding: 3px 8px; border-radius: 2px;
    font-family: var(--font-mono); font-size: 0.68rem; color: var(--text-muted);
  }

  .artist-identity-block { margin-bottom: 14px; }
  .artist-card-name {
    font-family: var(--font-serif); font-size: 1.85rem; font-weight: 400;
    font-style: italic; color: var(--linen); letter-spacing: -0.01em; line-height: 1.1;
  }
  .artist-tagline {
    font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-muted); margin-top: 4px;
  }

  .card-stats-ribbon {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 8px 10px; margin-bottom: 14px;
  }
  .mini-stat-capsule {
    display: flex; flex-direction: column; align-items: center;
  }
  .mini-stat-capsule span {
    font-family: var(--font-mono);
    font-size: 0.58rem; font-weight: 600; letter-spacing: 0.06em; color: var(--text-muted);
  }
  .mini-stat-capsule strong {
    font-family: var(--font-mono); font-size: 0.95rem; font-weight: 700; color: var(--linen);
  }

  .signature-tracks-box { display: flex; flex-direction: column; gap: 4px; }
  .track-preview-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 3px 6px; font-size: 0.72rem;
    background: rgba(234, 228, 217, 0.02);
    border-radius: 2px;
  }
  .track-preview-left {
    display: flex; align-items: center; gap: 6px; overflow: hidden;
  }
  .track-num { font-family: var(--font-mono); font-size: 0.64rem; color: var(--text-muted); }
  .track-name-text { font-family: var(--font-mono); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .track-plays-pill { font-family: var(--font-mono); font-size: 0.65rem; color: var(--text-muted); }
  .track-plays-pill.highlight { color: var(--oxide); }

  .card-bottom-actions {
    display: flex; gap: 8px; padding-top: 12px; border-top: 1px solid var(--border);
  }
  .btn-flip-card {
    flex: 1; height: 32px; background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-sm); color: var(--text-secondary); font-family: var(--font-mono);
    font-size: 0.7rem; font-weight: 500;
    cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;
    transition: border-color 0.15s ease;
  }
  .btn-flip-card:hover { border-color: var(--oxide); color: var(--linen); }

  .btn-battle-card {
    height: 32px; padding: 0 12px; background: var(--surface-2); border: 1px solid rgba(232, 68, 58, 0.3);
    border-radius: var(--r-sm); color: var(--signal); font-family: var(--font-mono);
    font-size: 0.7rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 4px;
  }
  .btn-battle-card:hover { border-color: var(--signal); background: rgba(232, 68, 58, 0.1); }

  .btn-inspect-modal {
    height: 32px; padding: 0 14px; background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-sm); color: var(--text-secondary); font-family: var(--font-mono);
    font-size: 0.7rem; font-weight: 500; cursor: pointer;
  }
  .btn-inspect-modal:hover { border-color: var(--oxide); color: var(--linen); }

  .deck-nav-controls {
    display: flex; align-items: center; gap: 10px;
  }
  .deck-nav-btn {
    width: 34px; height: 34px; border-radius: var(--r-sm);
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-primary); display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.15s ease;
  }
  .deck-nav-btn:hover { border-color: var(--oxide); background: var(--surface-3); }
  .deck-counter-badge {
    font-family: var(--font-mono); font-size: 0.74rem; font-weight: 600;
    color: var(--text-secondary); background: var(--surface-2);
    border: 1px solid var(--border); padding: 5px 12px; border-radius: var(--r-sm);
  }
  .deck-hint-text {
    font-size: 0.65rem; color: var(--text-muted); font-family: var(--font-mono);
  }

  .back-header {
    display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;
  }
  .back-header h3 {
    font-family: var(--font-serif); font-size: 1.35rem; font-style: italic; color: var(--linen);
  }
  .btn-unflip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px;
    color: var(--text-muted);
    padding: 3px 10px;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 500;
    cursor: pointer;
    position: relative;
    z-index: 25;
    pointer-events: auto;
    transition: all 0.15s ease;
  }
  .btn-unflip:hover {
    color: var(--linen);
    border-color: var(--oxide);
    background: var(--surface-3);
  }
  .back-bio-text {
    font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 10px;
  }
  .back-tracklist-wrap {
    display: flex; flex-direction: column; gap: 3px; max-height: 220px;
    overflow-y: auto; padding-right: 6px;
  }
  .back-tracklist-label {
    font-family: var(--font-mono); font-size: 0.62rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);
  }
  .back-track-item {
    display: flex; justify-content: space-between; font-size: 0.7rem; padding: 3px 0; border-bottom: 1px solid rgba(234, 228, 217, 0.04);
  }
</style>
