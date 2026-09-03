<script>
  import { X, Wand2, Sparkles, RotateCcw, Zap, Moon, Flame, Clock, Disc3, Rocket, Globe, Music, Film, ArrowRight, Play } from 'lucide-svelte';

  let { portfolio } = $props();

  let step = $state(1);
  let selectedEnergy  = $state('high');
  let selectedEra     = $state('golden');
  let selectedTexture = $state('rock');
  let matchedArtists  = $state([]);

  // ── Question data ──────────────────────────────────────────────
  const energyOptions = [
    { id: 'high',      title: 'High Voltage & Adrenaline',    sub: 'Heavy beats, raw energy, roaring choruses',           icon: Zap   },
    { id: 'chill',     title: 'Midnight Chill & Atmosphere',  sub: 'Mellow grooves, smooth synths, late-night vibes',     icon: Moon  },
    { id: 'nostalgic', title: 'Timeless Soul & Raw Passion',  sub: 'Acoustic warmth, legendary songwriting, classic feel', icon: Flame },
  ];

  const eraOptions = [
    { id: 'classic', title: 'Vintage Classics',        sub: 'Pink Floyd, Queen, Michael Jackson — 1960s–1980s', icon: Clock  },
    { id: 'golden',  title: 'Golden 90s & 2000s',      sub: 'Linkin Park, Nirvana, Oasis, Eminem',             icon: Disc3  },
    { id: 'modern',  title: 'Modern Chart & Alt',      sub: 'The Weeknd, Adele, Arctic Monkeys — 2010s–2020s', icon: Rocket },
    { id: 'any',     title: 'Time-Traveler (Any Era)', sub: 'Open to gems across all 7 decades',               icon: Globe  },
  ];

  const textureOptions = [
    { id: 'rock', title: 'Heavy Riffs & Distortion',      sub: 'Classic Rock, Nu-Metal, Grunge, Alt-Rock',      icon: Flame   },
    { id: 'pop',  title: 'Pop Anthems & Glossy Synths',   sub: '80s/90s Pop, Modern Chart, Dance-Pop',          icon: Sparkles},
    { id: 'soul', title: 'Smooth Grooves & R&B Vocals',   sub: 'Soul, R&B, Hip-Hop, Mellow Melodies',           icon: Music   },
    { id: 'ost',  title: 'Epic Cinematic & Soundtracks',  sub: 'Film scores, high-octane OSTs, orchestral',     icon: Film    },
  ];

  // ── Improved scoring engine ────────────────────────────────────
  const ENERGY_GENRES = {
    high:      ['Rock', 'Metal', 'Grunge', 'Punk', 'Rap', 'Hip-Hop'],
    chill:     ['Soul', 'R&B', 'Electronic', 'Pop', 'Smooth', 'Eurodance', 'Cinematic'],
    nostalgic: ['Classic', 'Soul', 'R&B', 'Indie', 'Alt', 'Pop'],
  };
  const ERA_DECADES = {
    classic: ['1960s', '1970s', '1980s'],
    golden:  ['1990s', '2000s'],
    modern:  ['2010s', '2020s'],
    any:     [],
  };
  const TEXTURE_GENRES = {
    rock: ['Rock', 'Metal', 'Grunge', 'Punk'],
    pop:  ['Pop', 'Electronic', 'Eurodance', 'Chart'],
    soul: ['Soul', 'R&B', 'Hip-Hop', 'Rap', 'Smooth'],
    ost:  ['Cinematic', 'OST'],
  };

  function scoreArtist(artist) {
    let score = 0;

    // Energy match (30 pts)
    const energyKeywords = ENERGY_GENRES[selectedEnergy] || [];
    if (energyKeywords.some(k => artist.genre.includes(k))) score += 30;

    // Era match (40 pts) — 'any' always gives full points
    const eraDecades = ERA_DECADES[selectedEra];
    if (eraDecades.length === 0 || eraDecades.includes(artist.decade)) score += 40;
    else score += 5; // small consolation so no one drops to 0 entirely

    // Texture match (30 pts)
    const textureKeywords = TEXTURE_GENRES[selectedTexture] || [];
    if (textureKeywords.some(k => artist.genre.includes(k))) score += 30;

    // Bonus: top plays boost (normalized 0-10 pts)
    const maxPlays = Math.max(...portfolio.allArtists.map(a => a.totalPlays), 1);
    score += Math.round((artist.totalPlays / maxPlays) * 10);

    return score;
  }

  function calculateMatches() {
    const scored = portfolio.allArtists
      .map(a => ({ artist: a, score: scoreArtist(a) }))
      .sort((a, b) => b.score - a.score);

    const maxScore = scored[0]?.score || 1;
    matchedArtists = scored.slice(0, 5).map(({ artist, score }) => ({
      ...artist,
      matchPct: Math.round((score / maxScore) * 100),
    }));
    step = 4;
  }

  function resetQuiz() {
    step = 1;
    selectedEnergy  = 'high';
    selectedEra     = 'golden';
    selectedTexture = 'rock';
    matchedArtists  = [];
  }

  const STEPS = ['Energy', 'Era', 'Texture'];
</script>

{#if portfolio.isMoodModalOpen}
  <div
    class="mood-backdrop"
    onclick={(e) => { if (e.target === e.currentTarget) portfolio.closeMood(); }}
    onkeydown={(e) => { if (e.key === 'Escape') portfolio.closeMood(); }}
    tabindex="0" role="dialog" aria-modal="true"
  >
    <div class="mood-card surface-noise">

      <!-- ── Header ──────────────────────────────────── -->
      <div class="mood-header">
        <div class="mood-heading">
          <div class="mood-eyebrow"><Wand2 size={11} /> <span>Mood Matchmaker</span></div>
          <h2>Music Mood Matchmaker</h2>
        </div>
        <button type="button" class="btn-close" onclick={() => portfolio.closeMood()} title="Close (Esc)">
          <X size={15} />
        </button>
      </div>

      <!-- ── Step Tracker ────────────────────────────── -->
      {#if step < 4}
        <div class="step-tracker">
          {#each STEPS as label, i}
            <div class="step-node" class:done={i + 1 < step} class:active={i + 1 === step} class:future={i + 1 > step}>
              <div class="step-circle">
                {#if i + 1 < step}
                  <svg width="10" height="10" viewBox="0 0 10 10"><path d="M2 5l2.5 2.5L8 2.5" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>
                {:else}
                  <span>{i + 1}</span>
                {/if}
              </div>
              <span class="step-label">{label}</span>
            </div>
            {#if i < 2}
              <div class="step-connector" class:done={i + 1 < step}></div>
            {/if}
          {/each}
        </div>
      {/if}

      <!-- ── Step 1: Energy ──────────────────────────── -->
      {#if step === 1}
        <div class="quiz-body">
          <p class="quiz-question">What energy are you channeling right now?</p>
          <div class="quiz-options">
            {#each energyOptions as opt}
              {@const Icon = opt.icon}
              <button
                type="button"
                class="opt-card"
                class:selected={selectedEnergy === opt.id}
                onclick={() => selectedEnergy = opt.id}
              >
                <div class="opt-accent"></div>
                <div class="opt-icon"><Icon size={20} /></div>
                <div class="opt-text">
                  <span class="opt-title">{opt.title}</span>
                  <span class="opt-sub">{opt.sub}</span>
                </div>
                <div class="opt-check">
                  {#if selectedEnergy === opt.id}
                    <div class="check-dot"></div>
                  {/if}
                </div>
              </button>
            {/each}
          </div>
          <div class="quiz-nav single">
            <button type="button" class="btn-primary" onclick={() => step = 2}>
              Continue to Era <ArrowRight size={13} />
            </button>
          </div>
        </div>
      {/if}

      <!-- ── Step 2: Era ─────────────────────────────── -->
      {#if step === 2}
        <div class="quiz-body">
          <p class="quiz-question">Which era sounds most compelling?</p>
          <div class="quiz-options">
            {#each eraOptions as opt}
              {@const Icon = opt.icon}
              <button
                type="button"
                class="opt-card"
                class:selected={selectedEra === opt.id}
                onclick={() => selectedEra = opt.id}
              >
                <div class="opt-accent"></div>
                <div class="opt-icon"><Icon size={20} /></div>
                <div class="opt-text">
                  <span class="opt-title">{opt.title}</span>
                  <span class="opt-sub">{opt.sub}</span>
                </div>
                <div class="opt-check">
                  {#if selectedEra === opt.id}
                    <div class="check-dot"></div>
                  {/if}
                </div>
              </button>
            {/each}
          </div>
          <div class="quiz-nav">
            <button type="button" class="btn-back" onclick={() => step = 1}>← Back</button>
            <button type="button" class="btn-primary" onclick={() => step = 3}>
              Continue to Texture <ArrowRight size={13} />
            </button>
          </div>
        </div>
      {/if}

      <!-- ── Step 3: Texture ─────────────────────────── -->
      {#if step === 3}
        <div class="quiz-body">
          <p class="quiz-question">What sonic texture do you want to feel?</p>
          <div class="quiz-options">
            {#each textureOptions as opt}
              {@const Icon = opt.icon}
              <button
                type="button"
                class="opt-card"
                class:selected={selectedTexture === opt.id}
                onclick={() => selectedTexture = opt.id}
              >
                <div class="opt-accent"></div>
                <div class="opt-icon"><Icon size={20} /></div>
                <div class="opt-text">
                  <span class="opt-title">{opt.title}</span>
                  <span class="opt-sub">{opt.sub}</span>
                </div>
                <div class="opt-check">
                  {#if selectedTexture === opt.id}
                    <div class="check-dot"></div>
                  {/if}
                </div>
              </button>
            {/each}
          </div>
          <div class="quiz-nav">
            <button type="button" class="btn-back" onclick={() => step = 2}>← Back</button>
            <button type="button" class="btn-primary reveal" onclick={calculateMatches}>
              <Sparkles size={13} /> Reveal Matches
            </button>
          </div>
        </div>
      {/if}

      <!-- ── Step 4: Results ─────────────────────────── -->
      {#if step === 4}
        <div class="results-body">
          <div class="results-header">
            <div class="results-eyebrow">
              <Sparkles size={11} />
              <span>Top {matchedArtists.length} frequency matches from your vault</span>
            </div>
            <div class="match-criteria">
              <span class="criteria-chip">{energyOptions.find(o => o.id === selectedEnergy)?.title.split(' ')[0]} energy</span>
              <span class="criteria-chip">{eraOptions.find(o => o.id === selectedEra)?.title}</span>
              <span class="criteria-chip">{textureOptions.find(o => o.id === selectedTexture)?.title.split(' ')[0]} texture</span>
            </div>
          </div>

          <div class="results-list">
            {#each matchedArtists as artist, idx}
              <div class="result-row" style="--rc: {artist.palette?.primary || '#C8934A'}">
                <div class="result-rank">
                  {#if idx === 0}<span class="rank-1">◆ 1</span>
                  {:else}<span>#{idx + 1}</span>
                  {/if}
                </div>

                <div class="result-art">
                  {#if artist.image}
                    <img src={artist.image} alt={artist.name} />
                  {:else}
                    <div class="result-art-fallback">{artist.name.slice(0, 2).toUpperCase()}</div>
                  {/if}
                </div>

                <div class="result-info">
                  <div class="result-name">{artist.name}</div>
                  <div class="result-meta">{artist.genre} · {artist.decade}</div>
                  {#if artist.songDetails?.[0]}
                    <div class="result-anthem">
                      <Play size={9} /> {artist.songDetails[0].title}
                    </div>
                  {/if}
                </div>

                <div class="result-match">
                  <div class="match-pct" style="color: var(--rc)">{artist.matchPct}%</div>
                  <div class="match-bar-wrap">
                    <div class="match-bar" style="width:{artist.matchPct}%; background: var(--rc)"></div>
                  </div>
                  <div class="match-lbl">match</div>
                </div>

                <button
                  type="button"
                  class="btn-inspect"
                  onclick={() => { portfolio.closeMood(); portfolio.openModal(artist); }}
                >
                  Open <ArrowRight size={11} />
                </button>
              </div>
            {/each}
          </div>

          <button type="button" class="btn-retake" onclick={resetQuiz}>
            <RotateCcw size={12} /> Retake Quiz
          </button>
        </div>
      {/if}

    </div>
  </div>
{/if}

<style>
  /* ── Backdrop ─────────────────────────────────────── */
  .mood-backdrop {
    position: fixed; inset: 0;
    background: rgba(8,7,5,0.9);
    backdrop-filter: blur(10px);
    z-index: 999;
    display: flex; align-items: center; justify-content: center;
    padding: 20px;
    animation: mFadeIn 0.14s ease-out;
  }
  @keyframes mFadeIn { from { opacity: 0; } to { opacity: 1; } }

  /* ── Card ─────────────────────────────────────────── */
  .mood-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    width: 100%; max-width: 600px;
    box-shadow: 0 30px 70px rgba(0,0,0,0.85);
    display: flex; flex-direction: column; gap: 0;
    overflow: hidden;
    animation: mScaleUp 0.18s var(--ease);
  }
  @keyframes mScaleUp {
    from { transform: scale(0.95); opacity: 0; }
    to   { transform: scale(1);    opacity: 1; }
  }

  /* ── Header ─────────────────────────────────────── */
  .mood-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 22px 14px;
    border-bottom: 1px solid var(--border);
  }
  .mood-eyebrow {
    display: inline-flex; align-items: center; gap: 5px;
    font-family: var(--font-mono); font-size: 0.6rem; font-weight: 700;
    letter-spacing: 0.1em; color: var(--oxide); text-transform: uppercase;
    margin-bottom: 3px;
  }
  .mood-heading h2 {
    font-family: var(--font-serif); font-size: 1.35rem; font-weight: 400;
    font-style: italic; color: var(--linen); line-height: 1;
  }
  .btn-close {
    width: 28px; height: 28px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-muted); display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.14s ease;
  }
  .btn-close:hover { color: var(--linen); border-color: var(--signal); }

  /* ── Step tracker ────────────────────────────────── */
  .step-tracker {
    display: flex; align-items: center;
    padding: 14px 22px;
    border-bottom: 1px solid var(--border);
    background: var(--surface-2);
  }
  .step-node {
    display: flex; align-items: center; gap: 7px;
    flex-shrink: 0;
  }
  .step-circle {
    width: 22px; height: 22px; border-radius: 50%;
    border: 1.5px solid var(--border);
    background: var(--surface);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.62rem; font-weight: 700;
    color: var(--text-muted);
    transition: all 0.2s ease;
  }
  .step-node.done .step-circle { background: var(--oxide); border-color: var(--oxide); color: #0D0B09; }
  .step-node.active .step-circle { border-color: var(--oxide); color: var(--oxide); background: color-mix(in srgb, var(--oxide) 10%, transparent); }
  .step-label {
    font-family: var(--font-mono); font-size: 0.62rem; font-weight: 600;
    color: var(--text-muted); letter-spacing: 0.04em;
    transition: color 0.15s ease;
  }
  .step-node.active .step-label { color: var(--linen); }
  .step-node.done .step-label { color: var(--oxide); }
  .step-connector {
    flex: 1; height: 1px; background: var(--border); margin: 0 8px;
    transition: background 0.3s ease;
  }
  .step-connector.done { background: var(--oxide); }

  /* ── Quiz body ───────────────────────────────────── */
  .quiz-body {
    padding: 20px 22px;
    display: flex; flex-direction: column; gap: 14px;
  }
  .quiz-question {
    font-family: var(--font-serif);
    font-size: 1.2rem; font-style: italic; font-weight: 400;
    color: var(--linen); letter-spacing: 0.01em;
    line-height: 1.3;
  }

  /* ── Option cards ────────────────────────────────── */
  .quiz-options { display: flex; flex-direction: column; gap: 6px; }

  .opt-card {
    position: relative;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 11px 14px 11px 18px;
    display: grid;
    grid-template-columns: 28px 1fr 20px;
    align-items: center;
    gap: 12px;
    cursor: pointer; text-align: left;
    transition: background 0.14s ease, border-color 0.14s ease, transform 0.14s ease;
    overflow: hidden;
  }
  .opt-card:hover {
    background: var(--surface-3);
    border-color: color-mix(in srgb, var(--oxide) 50%, transparent);
    transform: translateX(2px);
  }
  .opt-card.selected {
    background: color-mix(in srgb, var(--oxide) 6%, var(--surface-2));
    border-color: var(--oxide);
  }

  /* Left accent bar */
  .opt-accent {
    position: absolute; top: 0; left: 0; bottom: 0;
    width: 3px; background: transparent;
    transition: background 0.14s ease;
    border-radius: 2px 0 0 2px;
  }
  .opt-card.selected .opt-accent { background: var(--oxide); }

  .opt-icon { color: var(--oxide); display: flex; align-items: center; }
  .opt-card:not(.selected) .opt-icon { color: var(--text-muted); }

  .opt-text { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
  .opt-title {
    font-family: var(--font-sans); font-size: 0.85rem; font-weight: 700;
    color: var(--linen); letter-spacing: 0.01em;
  }
  .opt-sub {
    font-family: var(--font-mono); font-size: 0.66rem;
    color: var(--text-muted); letter-spacing: 0.01em;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }

  .opt-check {
    width: 16px; height: 16px; border-radius: 50%;
    border: 1.5px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: border-color 0.14s ease;
  }
  .opt-card.selected .opt-check { border-color: var(--oxide); }
  .check-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--oxide);
  }

  /* ── Navigation ──────────────────────────────────── */
  .quiz-nav {
    display: flex; align-items: center; gap: 8px;
    margin-top: 2px;
  }
  .quiz-nav.single { justify-content: flex-end; }

  .btn-back {
    padding: 8px 14px;
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: 2px; color: var(--text-muted);
    font-family: var(--font-mono); font-size: 0.7rem; font-weight: 600;
    cursor: pointer; transition: all 0.14s ease;
  }
  .btn-back:hover { color: var(--linen); border-color: var(--oxide); }

  .btn-primary {
    flex: 1; height: 38px;
    display: inline-flex; align-items: center; justify-content: center; gap: 7px;
    background: color-mix(in srgb, var(--oxide) 10%, transparent);
    border: 1px solid var(--oxide);
    border-radius: 2px; color: var(--oxide);
    font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
    cursor: pointer; transition: all 0.15s ease; letter-spacing: 0.03em;
  }
  .btn-primary:hover { background: var(--oxide); color: #0D0B09; }
  .btn-primary.reveal {
    background: var(--signal); border-color: var(--signal); color: #fff;
  }
  .btn-primary.reveal:hover { background: color-mix(in srgb, var(--signal) 80%, #000); }

  /* ── Results ─────────────────────────────────────── */
  .results-body {
    padding: 18px 22px;
    display: flex; flex-direction: column; gap: 12px;
  }

  .results-header {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }
  .results-eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: var(--font-mono); font-size: 0.62rem; font-weight: 700;
    color: var(--oxide); text-transform: uppercase; letter-spacing: 0.08em;
  }
  .match-criteria {
    display: flex; gap: 4px; flex-wrap: wrap; justify-content: flex-end;
  }
  .criteria-chip {
    font-family: var(--font-mono); font-size: 0.58rem; font-weight: 600;
    color: var(--text-muted); background: var(--surface-2);
    border: 1px solid var(--border); border-radius: 2px;
    padding: 2px 6px; letter-spacing: 0.04em;
  }

  /* Result rows */
  .results-list { display: flex; flex-direction: column; gap: 5px; }

  .result-row {
    display: grid;
    grid-template-columns: 28px 42px 1fr 64px 64px;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 3px;
    border: 1px solid transparent;
    background: var(--surface-2);
    transition: border-color 0.14s ease, background 0.14s ease;
  }
  .result-row:hover { border-color: var(--border); background: var(--surface-3); }

  .result-rank {
    font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700;
    color: var(--text-muted); text-align: center;
  }
  .rank-1 { color: var(--oxide); }

  .result-art {
    width: 42px; height: 42px; border-radius: 2px;
    overflow: hidden; flex-shrink: 0;
    border: 1px solid var(--border);
  }
  .result-art img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .result-art-fallback {
    width: 100%; height: 100%; background: var(--surface);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700;
    color: var(--rc);
  }

  .result-info { min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .result-name {
    font-family: var(--font-serif); font-size: 1rem; font-style: italic;
    font-weight: 400; color: var(--linen);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .result-meta {
    font-family: var(--font-mono); font-size: 0.62rem; color: var(--text-muted);
  }
  .result-anthem {
    display: inline-flex; align-items: center; gap: 4px;
    font-family: var(--font-mono); font-size: 0.62rem; color: var(--oxide);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }

  .result-match {
    display: flex; flex-direction: column; align-items: center; gap: 2px;
  }
  .match-pct {
    font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; line-height: 1;
  }
  .match-bar-wrap {
    width: 48px; height: 3px; background: var(--groove); border-radius: 2px; overflow: hidden;
  }
  .match-bar { height: 100%; border-radius: 2px; transition: width 0.4s ease; }
  .match-lbl {
    font-family: var(--font-mono); font-size: 0.52rem; font-weight: 700;
    color: var(--text-muted); letter-spacing: 0.08em; text-transform: uppercase;
  }

  .btn-inspect {
    display: inline-flex; align-items: center; justify-content: center; gap: 4px;
    padding: 6px 10px; border-radius: 2px;
    background: transparent; border: 1px solid var(--border);
    color: var(--text-muted); font-family: var(--font-mono);
    font-size: 0.66rem; font-weight: 700; cursor: pointer;
    transition: all 0.14s ease;
  }
  .btn-inspect:hover { border-color: var(--rc); color: var(--rc); }

  .btn-retake {
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
    padding: 7px 14px; align-self: center;
    background: transparent; border: 1px solid var(--border);
    border-radius: 2px; color: var(--text-muted);
    font-family: var(--font-mono); font-size: 0.68rem; font-weight: 600;
    cursor: pointer; transition: all 0.14s ease; margin-top: 2px;
  }
  .btn-retake:hover { color: var(--linen); border-color: var(--oxide); }

  @media (max-width: 520px) {
    .result-row { grid-template-columns: 24px 36px 1fr 50px; }
    .btn-inspect { display: none; }
  }
</style>
