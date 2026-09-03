<script>
  import { X, Swords, Trophy, Flame, Disc3, Clock, ShieldCheck, Shuffle, Crown, Music } from 'lucide-svelte';

  let { portfolio } = $props();

  let artistA = $derived(portfolio.battleArtist1 || portfolio.allArtists[0] || {});
  let artistB = $derived(portfolio.battleArtist2 || portfolio.allArtists[1] || portfolio.allArtists[0] || {});

  let searchA = $state('');
  let searchB = $state('');
  let selectOpenA = $state(false);
  let selectOpenB = $state(false);

  const colorA = $derived(artistA.palette?.primary || '#C8934A');
  const colorB = $derived(artistB.palette?.primary || '#E8443A');

  function getInitials(name) {
    if (!name) return '◈';
    const words = name.trim().split(/\s+/).filter(w => /[a-zA-Z]/.test(w[0]));
    if (words.length === 0) return name.slice(0, 2).toUpperCase();
    if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return (words[0][0] + words[1][0]).toUpperCase();
  }

  function pickRandomRival() {
    if (portfolio.allArtists.length < 2) return;
    let i = Math.floor(Math.random() * portfolio.allArtists.length);
    let j = Math.floor(Math.random() * portfolio.allArtists.length);
    while (j === i) j = Math.floor(Math.random() * portfolio.allArtists.length);
    portfolio.battleArtist1 = portfolio.allArtists[i];
    portfolio.battleArtist2 = portfolio.allArtists[j];
    portfolio.showToast(`${portfolio.battleArtist1.name} vs ${portfolio.battleArtist2.name}`);
  }

  const filteredListA = $derived(portfolio.allArtists.filter(a => a.name.toLowerCase().includes(searchA.toLowerCase())));
  const filteredListB = $derived(portfolio.allArtists.filter(a => a.name.toLowerCase().includes(searchB.toLowerCase())));

  const statsA = $derived({
    plays: artistA.totalPlays || 0,
    hours: artistA.totalHours || 0,
    albums: artistA.albumCount || 0,
    completion: artistA.completionRate || 0,
    tracks: artistA.trackCount || 0,
    topTrackPlays: artistA.songDetails?.[0]?.plays || 0,
    topTrackTitle: artistA.songDetails?.[0]?.title || 'N/A'
  });

  const statsB = $derived({
    plays: artistB.totalPlays || 0,
    hours: artistB.totalHours || 0,
    albums: artistB.albumCount || 0,
    completion: artistB.completionRate || 0,
    tracks: artistB.trackCount || 0,
    topTrackPlays: artistB.songDetails?.[0]?.plays || 0,
    topTrackTitle: artistB.songDetails?.[0]?.title || 'N/A'
  });

  const score = $derived.by(() => {
    let a = 0, b = 0;
    if (statsA.plays > statsB.plays) a++; else if (statsB.plays > statsA.plays) b++;
    if (statsA.hours > statsB.hours) a++; else if (statsB.hours > statsA.hours) b++;
    if (statsA.albums > statsB.albums) a++; else if (statsB.albums > statsA.albums) b++;
    if (statsA.completion > statsB.completion) a++; else if (statsB.completion > statsA.completion) b++;
    if (statsA.tracks > statsB.tracks) a++; else if (statsB.tracks > statsA.tracks) b++;
    if (statsA.topTrackPlays > statsB.topTrackPlays) a++; else if (statsB.topTrackPlays > statsA.topTrackPlays) b++;
    return { a, b };
  });

  function pct(va, vb) {
    const s = (va || 0) + (vb || 0);
    if (!s) return { a: 50, b: 50 };
    const a = Math.round((va / s) * 100);
    return { a, b: 100 - a };
  }

  const METRICS = $derived([
    { icon: Flame,       label: 'Total Plays',    valA: `${statsA.plays.toLocaleString()}`,           valB: `${statsB.plays.toLocaleString()}`,           winA: statsA.plays > statsB.plays,      winB: statsB.plays > statsA.plays,      bar: pct(statsA.plays, statsB.plays) },
    { icon: Clock,       label: 'Marathon Time',  valA: `${statsA.hours} hrs`,                        valB: `${statsB.hours} hrs`,                        winA: statsA.hours > statsB.hours,      winB: statsB.hours > statsA.hours,      bar: pct(statsA.hours, statsB.hours) },
    { icon: Disc3,       label: 'Albums',         valA: `${statsA.albums}`,                           valB: `${statsB.albums}`,                           winA: statsA.albums > statsB.albums,    winB: statsB.albums > statsA.albums,    bar: pct(statsA.albums, statsB.albums) },
    { icon: ShieldCheck, label: 'Retention',      valA: `${statsA.completion}%`,                      valB: `${statsB.completion}%`,                      winA: statsA.completion > statsB.completion, winB: statsB.completion > statsA.completion, bar: pct(statsA.completion, statsB.completion) },
    { icon: Music,       label: 'Catalog Size',   valA: `${statsA.tracks} tracks`,                    valB: `${statsB.tracks} tracks`,                    winA: statsA.tracks > statsB.tracks,    winB: statsB.tracks > statsA.tracks,    bar: pct(statsA.tracks, statsB.tracks) },
    { icon: Trophy,      label: 'Top Hit Anthem', valA: statsA.topTrackTitle, valA2: `${statsA.topTrackPlays} plays`, valB: statsB.topTrackTitle, valB2: `${statsB.topTrackPlays} plays`, winA: statsA.topTrackPlays > statsB.topTrackPlays, winB: statsB.topTrackPlays > statsA.topTrackPlays, bar: pct(statsA.topTrackPlays, statsB.topTrackPlays) }
  ]);
</script>

{#if portfolio.isBattleModalOpen}
  <div
    class="battle-backdrop"
    onclick={(e) => { if (e.target === e.currentTarget) portfolio.closeBattle(); }}
    onkeydown={(e) => { if (e.key === 'Escape') portfolio.closeBattle(); }}
    tabindex="0" role="dialog" aria-modal="true"
  >
    <div class="battle-card surface-noise">

      <!-- ── Header ──────────────────────────────────── -->
      <div class="battle-header">
        <div class="battle-heading">
          <div class="battle-eyebrow"><Swords size={11} /> <span>Artist Battle Arena</span></div>
          <h2>Head-to-Head Clash</h2>
        </div>
        <div class="battle-header-actions">
          <button type="button" class="btn-random" onclick={pickRandomRival}>
            <Shuffle size={12} /> Random Matchup
          </button>
          <button type="button" class="btn-close" onclick={() => portfolio.closeBattle()} title="Close (Esc)">
            <X size={15} />
          </button>
        </div>
      </div>

      <!-- ── Fighter Ring ────────────────────────────── -->
      <div class="fighter-ring">

        <!-- Side A -->
        <div class="fighter" style="--fc: {colorA}">
          <div class="fighter-art" class:has-crown={score.a > score.b}>
            {#if artistA.image}
              <img src={artistA.image} alt={artistA.name} />
            {:else}
              <div class="fighter-initials">{getInitials(artistA.name)}</div>
            {/if}
            {#if score.a > score.b}
              <div class="fighter-crown-badge"><Crown size={12} /></div>
            {/if}
            <div class="fighter-score-chip">{score.a}</div>
          </div>

          <div class="fighter-selector-wrap">
            <button
              type="button"
              class="fighter-select-btn"
              onclick={() => { selectOpenA = !selectOpenA; selectOpenB = false; }}
            >
              <span class="fighter-name">{artistA.name}</span>
              <span class="chevron">▾</span>
            </button>
            {#if selectOpenA}
              <div class="dropdown-popover">
                <input type="text" placeholder="Search…" bind:value={searchA} class="dropdown-search" />
                <div class="dropdown-list">
                  {#each filteredListA as a}
                    <button
                      type="button" class="dropdown-item"
                      class:active={a.id === artistA.id}
                      onclick={() => { portfolio.battleArtist1 = a; selectOpenA = false; }}
                    >
                      <span>{a.name}</span><small>{a.totalPlays}p</small>
                    </button>
                  {/each}
                </div>
              </div>
            {/if}
          </div>

          <div class="fighter-meta">{artistA.genre} · {artistA.decade}</div>
        </div>

        <!-- VS Divider -->
        <div class="vs-zone">
          <div class="vs-pill">VS</div>
          <div class="score-tally">
            <span class="tally-a" style="color:{colorA}">{score.a}</span>
            <span class="tally-sep">—</span>
            <span class="tally-b" style="color:{colorB}">{score.b}</span>
          </div>
        </div>

        <!-- Side B -->
        <div class="fighter right" style="--fc: {colorB}">
          <div class="fighter-art" class:has-crown={score.b > score.a}>
            {#if artistB.image}
              <img src={artistB.image} alt={artistB.name} />
            {:else}
              <div class="fighter-initials">{getInitials(artistB.name)}</div>
            {/if}
            {#if score.b > score.a}
              <div class="fighter-crown-badge"><Crown size={12} /></div>
            {/if}
            <div class="fighter-score-chip">{score.b}</div>
          </div>

          <div class="fighter-selector-wrap">
            <button
              type="button"
              class="fighter-select-btn"
              onclick={() => { selectOpenB = !selectOpenB; selectOpenA = false; }}
            >
              <span class="fighter-name">{artistB.name}</span>
              <span class="chevron">▾</span>
            </button>
            {#if selectOpenB}
              <div class="dropdown-popover right-drop">
                <input type="text" placeholder="Search…" bind:value={searchB} class="dropdown-search" />
                <div class="dropdown-list">
                  {#each filteredListB as b}
                    <button
                      type="button" class="dropdown-item"
                      class:active={b.id === artistB.id}
                      onclick={() => { portfolio.battleArtist2 = b; selectOpenB = false; }}
                    >
                      <span>{b.name}</span><small>{b.totalPlays}p</small>
                    </button>
                  {/each}
                </div>
              </div>
            {/if}
          </div>

          <div class="fighter-meta">{artistB.genre} · {artistB.decade}</div>
        </div>

      </div>

      <!-- ── Stat Clash Rows ─────────────────────────── -->
      <div class="clash-table">
        {#each METRICS as m}
          {@const MetricIcon = m.icon}
          <div class="clash-row">
            <div class="clash-val left" class:win={m.winA}>
              {#if m.valA2}<div class="clash-sub">{m.valA}</div><div class="clash-sub2">{m.valA2}</div>
              {:else}{m.valA}{/if}
            </div>

            <div class="clash-center">
              <div class="clash-label">
                <MetricIcon size={10} />
                <span>{m.label}</span>
              </div>
              <div class="clash-bar">
                <div class="clash-bar-a" style="width:{m.bar.a}%; background:{colorA}"></div>
                <div class="clash-bar-b" style="width:{m.bar.b}%; background:{colorB}"></div>
              </div>
            </div>

            <div class="clash-val right" class:win={m.winB}>
              {#if m.valB2}<div class="clash-sub">{m.valB}</div><div class="clash-sub2">{m.valB2}</div>
              {:else}{m.valB}{/if}
            </div>
          </div>
        {/each}
      </div>

      <!-- ── Footer ────────────────────────────────── -->
      <div class="battle-footer">
        <button type="button" class="btn-inspect" style="border-color:{colorA}" onclick={() => { portfolio.closeBattle(); portfolio.openModal(artistA); }}>
          Inspect {artistA.name}
        </button>
        <button type="button" class="btn-inspect" style="border-color:{colorB}" onclick={() => { portfolio.closeBattle(); portfolio.openModal(artistB); }}>
          Inspect {artistB.name}
        </button>
      </div>

    </div>
  </div>
{/if}

<style>
  /* ── Backdrop ─────────────────────────────────────── */
  .battle-backdrop {
    position: fixed; inset: 0;
    background: rgba(8,7,5,0.88);
    backdrop-filter: blur(10px);
    z-index: 999;
    display: flex; align-items: center; justify-content: center;
    padding: 20px;
    animation: bFadeIn 0.14s ease-out;
  }
  @keyframes bFadeIn { from { opacity: 0; } to { opacity: 1; } }

  /* ── Card ─────────────────────────────────────────── */
  .battle-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    width: 100%;
    max-width: 700px;
    box-shadow: 0 30px 70px rgba(0,0,0,0.85);
    display: flex;
    flex-direction: column;
    gap: 0;
    overflow: hidden;              /* NO scroll */
    animation: bScaleUp 0.18s var(--ease);
  }
  @keyframes bScaleUp {
    from { transform: scale(0.95); opacity: 0; }
    to   { transform: scale(1);    opacity: 1; }
  }

  /* ── Header ─────────────────────────────────────── */
  .battle-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 22px 14px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
  }
  .battle-eyebrow {
    display: inline-flex; align-items: center; gap: 5px;
    font-family: var(--font-mono); font-size: 0.6rem; font-weight: 700;
    letter-spacing: 0.1em; color: var(--signal); text-transform: uppercase;
    margin-bottom: 3px;
  }
  .battle-heading h2 {
    font-family: var(--font-serif); font-size: 1.35rem; font-weight: 400;
    font-style: italic; color: var(--linen); line-height: 1;
  }
  .battle-header-actions {
    display: flex; align-items: center; gap: 8px;
  }
  .btn-random {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 12px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--linen); font-family: var(--font-mono);
    font-size: 0.68rem; font-weight: 600; cursor: pointer;
    transition: all 0.14s ease; letter-spacing: 0.03em;
  }
  .btn-random:hover { border-color: var(--oxide); background: var(--surface-3); }
  .btn-close {
    width: 28px; height: 28px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-muted); display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.14s ease;
  }
  .btn-close:hover { color: var(--linen); border-color: var(--signal); }

  /* ── Fighter Ring ────────────────────────────────── */
  .fighter-ring {
    display: grid;
    grid-template-columns: 1fr 80px 1fr;
    align-items: center;
    padding: 18px 22px 14px;
    border-bottom: 1px solid var(--border);
    background: var(--surface-2);
    flex-shrink: 0;
  }

  .fighter {
    display: flex; flex-direction: column;
    align-items: center; gap: 8px;
    text-align: center;
  }
  .fighter.right { align-items: center; }

  /* Art */
  .fighter-art {
    position: relative;
    width: 76px; height: 76px;
    border-radius: 3px;
    border: 2px solid var(--border);
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(0,0,0,0.65);
    transition: border-color 0.15s ease;
  }
  .fighter-art.has-crown {
    border-color: var(--fc);
    box-shadow: 0 6px 20px rgba(0,0,0,0.6), 0 0 14px color-mix(in srgb, var(--fc) 30%, transparent);
  }
  .fighter-art img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .fighter-initials {
    width: 100%; height: 100%; background: var(--surface);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 1.2rem; font-weight: 700; color: var(--fc);
  }
  .fighter-crown-badge {
    position: absolute; top: -7px; right: -7px;
    color: var(--oxide); filter: drop-shadow(0 2px 4px rgba(0,0,0,0.9));
  }
  .fighter-score-chip {
    position: absolute; bottom: 3px; left: 50%; transform: translateX(-50%);
    background: rgba(0,0,0,0.75); border: 1px solid var(--fc);
    border-radius: 10px; padding: 0 6px;
    font-family: var(--font-mono); font-size: 0.62rem; font-weight: 700;
    color: var(--fc); line-height: 1.5; backdrop-filter: blur(4px);
  }

  /* Selector */
  .fighter-selector-wrap { position: relative; width: 100%; max-width: 200px; }
  .fighter-select-btn {
    width: 100%; padding: 5px 10px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 2px; color: var(--linen);
    font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700;
    cursor: pointer; display: flex; align-items: center; justify-content: space-between;
    gap: 6px; transition: border-color 0.14s ease;
  }
  .fighter-select-btn:hover { border-color: var(--fc); }
  .fighter-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .chevron { color: var(--text-muted); font-size: 0.7rem; flex-shrink: 0; }

  .fighter-meta {
    font-family: var(--font-mono); font-size: 0.6rem;
    color: var(--text-muted); letter-spacing: 0.03em;
  }

  /* Dropdown */
  .dropdown-popover {
    position: absolute; top: calc(100% + 4px); left: 0; right: 0;
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: 4px; padding: 6px; z-index: 60;
    box-shadow: 0 16px 40px rgba(0,0,0,0.85);
  }
  .dropdown-popover.right-drop { left: auto; right: 0; }
  .dropdown-search {
    width: 100%; padding: 5px 8px; background: var(--surface);
    border: 1px solid var(--border); border-radius: 2px;
    color: var(--linen); font-family: var(--font-mono); font-size: 0.7rem;
    margin-bottom: 5px; outline: none; box-sizing: border-box;
  }
  .dropdown-search:focus { border-color: var(--oxide); }
  .dropdown-list { max-height: 160px; overflow-y: auto; display: flex; flex-direction: column; gap: 1px; }
  .dropdown-item {
    display: flex; justify-content: space-between; align-items: center;
    padding: 5px 8px; background: transparent; border: none;
    border-radius: 2px; color: var(--text-secondary);
    font-family: var(--font-mono); font-size: 0.7rem; cursor: pointer; text-align: left;
  }
  .dropdown-item small { color: var(--text-muted); font-size: 0.62rem; }
  .dropdown-item:hover, .dropdown-item.active { background: var(--surface-3); color: var(--linen); }

  /* VS divider */
  .vs-zone {
    display: flex; flex-direction: column; align-items: center; gap: 6px;
  }
  .vs-pill {
    width: 38px; height: 38px; border-radius: 50%;
    background: var(--surface); border: 1px solid var(--signal);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
    color: var(--signal); letter-spacing: 0.06em;
    box-shadow: 0 0 14px rgba(232,68,58,0.25);
  }
  .score-tally {
    display: flex; align-items: center; gap: 4px;
    font-family: var(--font-mono); font-size: 0.82rem; font-weight: 700;
  }
  .tally-sep { color: var(--text-muted); }

  /* ── Clash Table ─────────────────────────────────── */
  .clash-table {
    display: flex; flex-direction: column;
    padding: 10px 22px;
    gap: 4px;
    flex-shrink: 0;
  }

  .clash-row {
    display: grid;
    grid-template-columns: 110px 1fr 110px;
    align-items: center;
    gap: 10px;
    padding: 6px 10px;
    border-radius: 2px;
    transition: background 0.12s ease;
  }
  .clash-row:hover { background: var(--surface-2); }

  .clash-val {
    font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600;
    color: var(--text-secondary); font-variant-numeric: tabular-nums;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .clash-val.left  { text-align: left; }
  .clash-val.right { text-align: right; }
  .clash-val.win   { color: var(--linen); font-weight: 700; }

  .clash-sub  { font-size: 0.76rem; font-weight: 700; line-height: 1.2; }
  .clash-sub2 { font-size: 0.6rem; color: var(--text-muted); font-weight: 500; }
  .clash-val.win .clash-sub { color: var(--linen); }

  .clash-center {
    display: flex; flex-direction: column; align-items: center; gap: 3px;
  }
  .clash-label {
    display: inline-flex; align-items: center; gap: 4px;
    font-family: var(--font-mono); font-size: 0.55rem; font-weight: 700;
    letter-spacing: 0.1em; color: var(--text-muted); text-transform: uppercase;
  }
  .clash-bar {
    width: 100%; height: 4px; border-radius: 2px;
    background: var(--groove);
    display: flex; overflow: hidden;
  }
  .clash-bar-a { height: 100%; transition: width 0.35s ease; border-radius: 2px 0 0 2px; }
  .clash-bar-b { height: 100%; transition: width 0.35s ease; border-radius: 0 2px 2px 0; }

  /* ── Footer ─────────────────────────────────────── */
  .battle-footer {
    display: flex; gap: 0;
    border-top: 1px solid var(--border);
    flex-shrink: 0;
  }
  .btn-inspect {
    flex: 1; height: 38px;
    background: var(--surface-2);
    border: none;
    border-top: 2px solid transparent;
    color: var(--text-secondary);
    font-family: var(--font-mono); font-size: 0.72rem; font-weight: 600;
    cursor: pointer; transition: all 0.14s ease; letter-spacing: 0.02em;
  }
  .btn-inspect:first-child { border-right: 1px solid var(--border); }
  .btn-inspect:hover { color: var(--linen); background: var(--surface-3); }

  /* ── Responsive ──────────────────────────────────── */
  @media (max-width: 580px) {
    .fighter-ring { grid-template-columns: 1fr; gap: 8px; }
    .vs-zone { flex-direction: row; }
    .clash-row { grid-template-columns: 80px 1fr 80px; gap: 6px; }
    .clash-val { font-size: 0.7rem; }
  }
</style>
