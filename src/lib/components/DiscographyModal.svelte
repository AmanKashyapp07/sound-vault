<script>
  import { X } from 'lucide-svelte';

  let { portfolio } = $props();

  const artist = $derived(portfolio.selectedArtistModal);

  function getInitials(name) {
    if (!name) return '◈';
    const words = name.trim().split(/\s+/).filter(w => /[a-zA-Z]/.test(w[0]));
    if (words.length === 0) return name.slice(0, 2).toUpperCase();
    if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }

  function handleKeydown(e) {
    if (e.key === 'Escape') portfolio.closeModal();
  }
</script>

<svelte:window onkeydown={handleKeydown} />

{#if artist}
  {@const bgColor = artist.palette ? artist.palette.primary : '#C8934A'}
  {@const albumsBreakdown = artist.albumsBreakdown || []}

  <div 
    class="modal-backdrop open" 
    onclick={(e) => { if (e.target === e.currentTarget) portfolio.closeModal(); }}
    onkeydown={(e) => { if (e.key === 'Escape' || e.key === 'Enter') portfolio.closeModal(); }}
    role="dialog"
    aria-modal="true"
    tabindex="-1"
  >
    <div class="artist-modal-dialog surface-noise">
      <button type="button" class="modal-close-btn" onclick={portfolio.closeModal}>
        <X size={15} />
      </button>

      <div class="modal-artist-header">
        <div 
          class="modal-avatar"
          style="background: {bgColor}18; border: 1px solid {bgColor}40;"
        >
          {#if artist.image}
            <img src={artist.image} alt={artist.name} class="modal-img" />
          {:else}
            {getInitials(artist.name)}
          {/if}
        </div>
        <div class="modal-title-wrap">
          <div class="modal-pre-tag num">{artist.decade} PRESSING / {artist.genre}</div>
          <h2>{artist.name}</h2>
          <p class="num">{artist.trackCount} Tracks / {artist.albumCount} Albums / {artist.totalHours || 0} hrs verified runtime</p>
        </div>
      </div>

      <div class="modal-metrics-strip">
        <div class="modal-metric-chip">
          <span>TOTAL PLAYS</span>
          <strong class="num">{artist.totalPlays.toLocaleString()}</strong>
        </div>
        <div class="modal-metric-chip">
          <span>RUNTIME</span>
          <strong class="num">{artist.totalHours || 0} hrs</strong>
        </div>
        <div class="modal-metric-chip">
          <span>ALBUMS</span>
          <strong class="num">{artist.albumCount}</strong>
        </div>
        <div class="modal-metric-chip">
          <span>RETENTION</span>
          <strong class="num">{artist.completionRate}%</strong>
        </div>
      </div>

      <div class="modal-bio-card">
        {artist.bio || `${artist.name} is a verified artist in the catalog with ${artist.totalPlays} total plays across ${artist.trackCount} tracks.`}
      </div>

      <div class="modal-albums-label">Album Pressings & Composition Breakdown</div>

      <div class="modal-albums-scroll">
        {#if albumsBreakdown.length === 0}
          <div style="color:var(--text-muted); font-size:0.8rem; font-family:var(--font-mono);">No detailed album data recorded.</div>
        {:else}
          {#each albumsBreakdown as alb}
            <div class="album-disc-card">
              <div class="album-disc-header">
                <span class="album-disc-title">{alb.name}</span>
                <span class="album-disc-badge num">{alb.plays} plays / {alb.trackCount} tracks</span>
              </div>
              <div class="album-songs-list">
                {#each (alb.songs || []) as s}
                  <div class="album-song-chip" title={s.title}>
                    <span class="song-title-text">{s.title}</span>
                    <span class="track-plays-pill num" class:highlight={s.plays >= 30}>{s.plays}p</span>
                  </div>
                {/each}
              </div>
            </div>
          {/each}
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed; inset: 0;
    background: rgba(8, 7, 5, 0.85);
    backdrop-filter: blur(8px);
    z-index: 300; display: flex;
    align-items: center; justify-content: center;
    padding: 24px;
    animation: fadeIn 0.15s var(--ease);
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
  }

  .artist-modal-dialog {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    width: 100%; max-width: 680px;
    max-height: 88vh; display: flex;
    flex-direction: column; padding: 28px;
    position: relative;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8);
    animation: scaleUp 0.2s var(--ease);
  }

  @keyframes scaleUp {
    from { opacity: 0; transform: scale(0.97) translateY(6px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
  }

  .modal-close-btn {
    position: absolute; top: 18px; right: 18px;
    width: 28px; height: 28px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-muted); cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.15s ease;
  }
  .modal-close-btn:hover { color: var(--linen); border-color: var(--oxide); }

  .modal-artist-header {
    display: flex; align-items: center; gap: 16px; margin-bottom: 20px;
  }
  .modal-avatar {
    width: 54px; height: 54px; border-radius: 2px;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700;
    color: var(--linen); overflow: hidden; flex-shrink: 0;
  }
  .modal-img {
    width: 100%; height: 100%; object-fit: cover;
  }

  .modal-pre-tag {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--oxide);
    font-weight: 600;
    letter-spacing: 0.06em;
  }

  .modal-title-wrap h2 {
    font-family: var(--font-serif); font-size: 1.7rem;
    font-weight: 400; font-style: italic; color: var(--linen); letter-spacing: -0.01em;
    margin: 2px 0;
  }
  .modal-title-wrap p {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-muted);
  }

  .modal-metrics-strip {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;
    margin-bottom: 14px;
  }
  .modal-metric-chip {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 8px 10px;
    display: flex; flex-direction: column; gap: 2px;
  }
  .modal-metric-chip span {
    font-family: var(--font-mono);
    font-size: 0.58rem; font-weight: 600; text-transform: uppercase;
    color: var(--text-muted); letter-spacing: 0.06em;
  }
  .modal-metric-chip strong {
    font-family: var(--font-mono); font-size: 0.95rem;
    font-weight: 700; color: var(--linen);
  }

  .modal-bio-card {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 12px 14px;
    font-family: var(--font-mono);
    font-size: 0.74rem; color: var(--text-secondary); line-height: 1.45;
    margin-bottom: 16px;
  }

  .modal-albums-label {
    font-family: var(--font-mono);
    font-size: 0.64rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--text-muted); margin-bottom: 8px;
  }

  .modal-albums-scroll {
    display: flex; flex-direction: column; gap: 8px;
    overflow-y: auto; padding-right: 4px; max-height: 300px;
  }

  .album-disc-card {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 10px 12px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .album-disc-header {
    display: flex; justify-content: space-between; align-items: center;
  }
  .album-disc-title {
    font-family: var(--font-mono);
    font-size: 0.78rem; font-weight: 600; color: var(--linen);
  }
  .album-disc-badge {
    font-size: 0.64rem; color: var(--text-muted); font-family: var(--font-mono);
  }

  .album-songs-list {
    display: flex; flex-wrap: wrap; gap: 5px;
  }
  .album-song-chip {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-secondary);
    padding: 3px 8px; background: var(--surface);
    border: 1px solid var(--border); border-radius: 2px;
    display: flex; align-items: center; gap: 6px;
  }
  .song-title-text {
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 180px;
  }
  .track-plays-pill {
    font-size: 0.62rem; color: var(--text-muted);
  }
  .track-plays-pill.highlight { color: var(--oxide); font-weight: 600; }

  @media (max-width: 680px) {
    .modal-metrics-strip { grid-template-columns: repeat(2, 1fr); }
  }
</style>
