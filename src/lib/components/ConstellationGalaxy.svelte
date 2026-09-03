<script>
  import { Disc3, ArrowRight, Play } from 'lucide-svelte';

  let { portfolio } = $props();

  let activeArtist = $state(null);
  let scrollContainer = $state(null);
  let selectedDecadeFilter = $state('all');

  const GENRE_SPINE_COLORS = {
    'Classic Rock':        '#C8934A',
    'Nu-Metal / Alt Rock': '#E8443A',
    'Indie / Alt Rock':    '#A67C52',
    '80s/90s Pop':         '#C25E34',
    'Hip-Hop / Rap':       '#9C6B28',
    'Modern Pop / Chart':  '#B89B72',
    'Grunge / Alt Rock':   '#7A7268',
    'Smooth Soul / R&B':   '#D4A373',
    'Eurodance / Electronic': '#6B6255',
    'Cinematic / OST':     '#5A5248'
  };

  const DECADE_TABS = ['all', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'];

  const allFiltered  = $derived(portfolio.filteredArtists);
  const displayedArtists = $derived.by(() => {
    if (selectedDecadeFilter === 'all') return allFiltered;
    return allFiltered.filter(a => a.decade === selectedDecadeFilter);
  });

  const selectedArtist = $derived(activeArtist || displayedArtists[0] || allFiltered[0] || portfolio.allArtists[0]);

  function pickDecade(dec) {
    activeArtist = null;
    selectedDecadeFilter = dec;
    scrollContainer?.scrollTo({ left: 0, behavior: 'smooth' });
  }
</script>

<div class="crate-root surface-noise">

  <!-- ── TOP: Header row ─────────────────────────────── -->
  <div class="crate-top">
    <div class="crate-heading">
      <div class="crate-eyebrow">
        <Disc3 size={11} />
        <span>Vinyl Archive</span>
      </div>
      <h2 class="crate-title">{displayedArtists.length} Records in Crate</h2>
    </div>

    <div class="crate-decade-tabs">
      {#each DECADE_TABS as dec}
        <button
          type="button"
          class="decade-tab"
          class:active={selectedDecadeFilter === dec}
          onclick={() => pickDecade(dec)}
        >{dec === 'all' ? 'All' : dec.slice(2)}</button>
      {/each}
    </div>
  </div>

  <!-- ── MIDDLE: Spine Rack ──────────────────────────── -->
  <div class="rack-shell">
    <div class="rack-bar top">
      <span>{displayedArtists.length} pressings</span>
      <span>33⅓ RPM · {selectedDecadeFilter === 'all' ? '7 Decades' : selectedDecadeFilter}</span>
    </div>

    <div class="rack-viewport" bind:this={scrollContainer}>
      <div class="rack-floor">
        {#each displayedArtists as artist, idx}
          {@const color = GENRE_SPINE_COLORS[artist.genre] || '#C8934A'}
          {@const active = selectedArtist?.id === artist.id}
          <button
            type="button"
            class="spine"
            class:active
            style="--c: {color}"
            onmouseenter={() => activeArtist = artist}
            onclick={() => { activeArtist = artist; portfolio.openModal(artist); }}
            title="{artist.name} · {artist.decade} · {artist.totalPlays} plays"
          >
            <span class="spine-idx">{String(idx + 1).padStart(2,'0')}</span>
            <span class="spine-label">{artist.name}</span>
            <div class="spine-notch" style="background:{color}"></div>
          </button>
        {/each}
      </div>
    </div>

    <div class="rack-bar bottom">
      <span>Hover to preview · Click to open full discography</span>
      <span>Master Tape Catalog</span>
    </div>
  </div>

  <!-- ── BOTTOM: Gatefold Inspector ─────────────────── -->
  {#if selectedArtist}
    {@const color = GENRE_SPINE_COLORS[selectedArtist.genre] || '#C8934A'}
    {@const maxP   = Math.max(...(selectedArtist.songDetails || [{ plays: 1 }]).map(s => s.plays || 1), 1)}

    <div class="gatefold" style="--gcolor: {color}">

      <!-- Art -->
      <div class="gf-art">
        {#if selectedArtist.image}
          <img src={selectedArtist.image} alt={selectedArtist.name} />
        {:else}
          <div class="gf-art-fallback"><Disc3 size={44} /></div>
        {/if}
        <div class="gf-art-overlay"></div>
        <div class="gf-art-spine" style="background:{color}"></div>
      </div>

      <!-- Main body -->
      <div class="gf-body">

        <!-- Top bar: identity + stats -->
        <div class="gf-top">
          <div class="gf-identity">
            <div class="gf-tags">
              <span class="gf-decade">{selectedArtist.decade}</span>
              <span class="gf-genre">{selectedArtist.genre}</span>
            </div>
            <h3 class="gf-artist">{selectedArtist.name}</h3>
          </div>

          <div class="gf-stat-band">
            <div class="gf-stat">
              <span class="gf-stat-val">{selectedArtist.totalPlays.toLocaleString()}</span>
              <span class="gf-stat-lbl">Plays</span>
            </div>
            <div class="gf-vr"></div>
            <div class="gf-stat">
              <span class="gf-stat-val">{selectedArtist.albumCount}</span>
              <span class="gf-stat-lbl">{selectedArtist.albumCount === 1 ? 'Album' : 'Albums'}</span>
            </div>
            <div class="gf-vr"></div>
            <div class="gf-stat">
              <span class="gf-stat-val">{selectedArtist.trackCount}</span>
              <span class="gf-stat-lbl">Tracks</span>
            </div>
            <div class="gf-vr"></div>
            <div class="gf-stat">
              <span class="gf-stat-val">{selectedArtist.totalHours || 0}h</span>
              <span class="gf-stat-lbl">Runtime</span>
            </div>
            <div class="gf-vr"></div>
            <div class="gf-stat">
              <span class="gf-stat-val" style="color: var(--gcolor)">{selectedArtist.completionRate || '—'}%</span>
              <span class="gf-stat-lbl">Retention</span>
            </div>
          </div>
        </div>

        <!-- Bottom: bio + tracks side by side -->
        <div class="gf-bottom">
          <div class="gf-bio-col">
            {#if selectedArtist.bio}
              <p class="gf-bio">{selectedArtist.bio.slice(0, 220)}…</p>
            {:else}
              <p class="gf-bio">Authentic Apple Music discography.</p>
            {/if}
          </div>

          <div class="gf-tracks-col">
            {#each (selectedArtist.songDetails || []).slice(0, 3) as song, si}
              <div class="gf-track">
                <span class="gf-track-idx">{si + 1}</span>
                <span class="gf-track-name">{song.title}</span>
                <div class="gf-bar-wrap">
                  <div class="gf-bar" style="width:{Math.max(6, Math.round((song.plays / maxP) * 100))}%"></div>
                </div>
                <span class="gf-track-plays">{song.plays}</span>
              </div>
            {/each}
          </div>

          <button
            type="button"
            class="gf-open-btn"
            onclick={() => portfolio.openModal(selectedArtist)}
          >
            View Full Discography
            <ArrowRight size={12} />
          </button>
        </div>

      </div>
    </div>
  {/if}

</div>

<style>
  /* ── Root ───────────────────────────────────────────── */
  .crate-root {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    display: flex;
    flex-direction: column;
    gap: 0;
    overflow: hidden;
  }

  /* ── Header ─────────────────────────────────────────── */
  .crate-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 20px 24px 16px;
    border-bottom: 1px solid var(--border);
    flex-wrap: wrap;
  }

  .crate-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--oxide);
    text-transform: uppercase;
    margin-bottom: 4px;
  }

  .crate-title {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: 400;
    font-style: italic;
    color: var(--linen);
    line-height: 1.1;
  }

  /* Decade tabs */
  .crate-decade-tabs {
    display: flex;
    gap: 2px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 3px;
  }

  .decade-tab {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 3px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 600;
    padding: 4px 10px;
    cursor: pointer;
    transition: all 0.12s ease;
    letter-spacing: 0.04em;
  }
  .decade-tab:hover { color: var(--linen); background: var(--surface-3); }
  .decade-tab.active {
    background: var(--surface);
    border-color: var(--oxide);
    color: var(--oxide);
  }

  /* ── Rack Shell ──────────────────────────────────────── */
  .rack-shell {
    background: #070604;
    border-bottom: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    padding: 8px 20px;
    gap: 6px;
  }

  .rack-bar {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    color: #3D372E;
    text-transform: uppercase;
    padding: 2px 6px;
  }
  .rack-bar.top { border-bottom: 1px solid #1C1812; padding-bottom: 6px; }
  .rack-bar.bottom { border-top: 1px solid #1C1812; padding-top: 6px; }

  /* Spine viewport */
  .rack-viewport {
    overflow-x: auto;
    overflow-y: visible;
    padding: 24px 8px 20px;
    scrollbar-width: thin;
    scrollbar-color: #2B251E #070604;
  }

  .rack-floor {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    min-width: max-content;
    height: 230px;
  }

  /* ── Individual Spine ───────────────────────────────── */
  .spine {
    --c: #C8934A;
    width: 28px;
    height: 200px;
    background: linear-gradient(180deg, #1A1612 0%, #120F0C 100%);
    border: 1px solid #2A231C;
    border-top: 2px solid var(--c);
    border-radius: 1px 1px 0 0;
    padding: 8px 3px 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    position: relative;
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.03), 2px 0 6px rgba(0,0,0,0.7);
    transition: transform 0.2s cubic-bezier(0.16,1,0.3,1), box-shadow 0.2s ease, border-color 0.15s ease, background 0.15s ease;
  }

  .spine:hover {
    transform: translateY(-20px);
    background: linear-gradient(180deg, #232019 0%, #1A1612 100%);
    border-color: var(--c);
    border-top-width: 3px;
    z-index: 10;
    box-shadow: 0 12px 28px rgba(0,0,0,0.85), inset -1px 0 0 rgba(255,255,255,0.06);
  }

  .spine.active {
    background: linear-gradient(180deg, #2A2117 0%, #1E1A12 100%);
    border-color: var(--oxide);
    border-top: 3px solid var(--oxide);
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.06);
  }

  .spine-idx {
    font-family: var(--font-mono);
    font-size: 0.5rem;
    font-weight: 700;
    color: #3D372E;
    line-height: 1;
  }
  .spine:hover .spine-idx, .spine.active .spine-idx { color: var(--c); }

  .spine-label {
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    font-family: var(--font-mono);
    font-size: 0.58rem;
    font-weight: 500;
    color: #7A6F62;
    white-space: nowrap;
    overflow: hidden;
    max-height: 138px;
    letter-spacing: 0.01em;
    line-height: 1;
    flex: 1;
    display: flex;
    align-items: center;
  }
  .spine:hover .spine-label { color: var(--linen); font-weight: 700; }
  .spine.active .spine-label { color: var(--linen); font-weight: 700; }

  .spine-notch {
    width: 16px;
    height: 4px;
    border-radius: 1px;
    opacity: 0.7;
  }
  .spine:hover .spine-notch, .spine.active .spine-notch { opacity: 1; }

  /* ── Gatefold Inspector ─────────────────────────────── */
  .gatefold {
    --gcolor: #C8934A;
    display: grid;
    grid-template-columns: 156px 1fr;
    gap: 0;
    background: var(--surface-2);
    border-top: 1px solid var(--border);
    height: 200px;   /* fixed — never changes */
  }

  /* Art column */
  .gf-art {
    position: relative;
    flex-shrink: 0;
    overflow: hidden;
    background: #0E0C09;
    height: 200px;
  }
  .gf-art img {
    width: 100%; height: 100%;
    object-fit: cover; display: block;
  }
  .gf-art-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to right, transparent 50%, rgba(13,11,9,0.55) 100%);
    pointer-events: none;
  }
  .gf-art-fallback {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    color: var(--gcolor);
  }
  .gf-art-spine {
    position: absolute;
    top: 0; bottom: 0; right: 0;
    width: 4px;
  }

  /* Body: everything to the right of the art */
  .gf-body {
    display: flex;
    flex-direction: column;
    min-width: 0;
    height: 200px;
    overflow: hidden;
    box-sizing: border-box;
  }

  /* Top portion: identity + stat band */
  .gf-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 16px 20px 12px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
  }

  .gf-identity {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }

  .gf-tags {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .gf-decade {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 700;
    color: var(--gcolor);
    background: color-mix(in srgb, var(--gcolor) 12%, transparent);
    border: 1px solid color-mix(in srgb, var(--gcolor) 30%, transparent);
    border-radius: 2px;
    padding: 1px 6px;
    letter-spacing: 0.05em;
  }
  .gf-genre {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
  }
  .gf-artist {
    font-family: var(--font-serif);
    font-size: 1.55rem;
    font-weight: 400;
    font-style: italic;
    color: var(--linen);
    line-height: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Stat band */
  .gf-stat-band {
    display: flex;
    align-items: center;
    gap: 0;
    flex-shrink: 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
  }
  .gf-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8px 16px;
    gap: 2px;
  }
  .gf-stat-val {
    font-family: var(--font-mono);
    font-size: 1rem;
    font-weight: 700;
    color: var(--linen);
    line-height: 1;
  }
  .gf-stat-lbl {
    font-family: var(--font-mono);
    font-size: 0.52rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    text-transform: uppercase;
  }
  .gf-vr {
    width: 1px;
    height: 34px;
    background: var(--border);
    flex-shrink: 0;
  }

  /* Bottom portion: bio + tracks + button */
  .gf-bottom {
    display: grid;
    grid-template-columns: 1fr auto auto;
    align-items: center;
    gap: 16px;
    padding: 10px 20px;
    flex: 1;
    min-height: 0;
  }

  .gf-bio-col { min-width: 0; }
  .gf-bio {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    line-height: 1.55;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  /* Tracks column */
  .gf-tracks-col {
    display: flex;
    flex-direction: column;
    gap: 4px;
    width: 220px;
    flex-shrink: 0;
    border-left: 1px solid var(--border);
    padding-left: 16px;
  }
  .gf-track {
    display: grid;
    grid-template-columns: 12px 1fr 46px 22px;
    align-items: center;
    gap: 6px;
  }
  .gf-track-idx {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--text-muted);
    text-align: right;
  }
  .gf-track-name {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--linen);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .gf-bar-wrap {
    height: 3px;
    background: var(--groove);
    border-radius: 2px;
    overflow: hidden;
  }
  .gf-bar {
    height: 100%;
    background: var(--gcolor);
    border-radius: 2px;
    transition: width 0.35s ease;
  }
  .gf-track-plays {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--text-muted);
    text-align: right;
  }

  /* CTA */
  .gf-open-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: color-mix(in srgb, var(--gcolor) 10%, transparent);
    border: 1px solid var(--gcolor);
    border-radius: 2px;
    color: var(--gcolor);
    font-family: var(--font-mono);
    font-size: 0.66rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
    align-self: center;
    flex-shrink: 0;
  }
  .gf-open-btn:hover {
    background: var(--gcolor);
    color: #0D0B09;
  }

  /* ── Responsive ─────────────────────────────────────── */
  @media (max-width: 860px) {
    .gatefold { grid-template-columns: 100px 1fr; height: auto; }
    .gf-art { height: auto; min-height: 200px; }
    .gf-body { height: auto; }
    .gf-bottom { grid-template-columns: 1fr; }
    .gf-tracks-col { width: auto; border-left: none; padding-left: 0; border-top: 1px solid var(--border); padding-top: 10px; }
  }

  @media (max-width: 600px) {
    .gatefold { grid-template-columns: 1fr; }
    .gf-art { height: 160px; }
    .gf-stat-band { flex-wrap: wrap; }
    .crate-top { flex-direction: column; align-items: flex-start; }
  }
</style>
