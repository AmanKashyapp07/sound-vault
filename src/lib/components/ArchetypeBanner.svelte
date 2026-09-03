<script>
  let { portfolio } = $props();
  const stats = $derived(portfolio.catalogStats || {});
  const archetype = $derived(stats.archetype || {
    title: "The Sonic Time-Traveler",
    badge: "7 Decades Spanned · 81.6% Retention",
    bio: "Your English playlist bridges 1960s classic rock legends with 2020s alternative rock & chart hits, featuring 81.6% track retention and deep discography loyalty across 7 decades."
  });

  let isSpinningFast = $state(false);

  function triggerVinylRoulette() {
    isSpinningFast = true;
    setTimeout(() => {
      isSpinningFast = false;
      portfolio.shuffleVault();
    }, 450);
  }
</script>

<section class="archetype-hero-banner surface-noise">
  <div class="archetype-content-grid">
    <!-- LEFT: Editorial & Identity Story -->
    <div class="archetype-story-pane">
      <div class="archetype-tag-strip">
        <span class="sub-badge-text">7 Decades Spanned</span>
        <span class="badge-separator">·</span>
        <span class="sub-badge-meta">Master Cut</span>
        <span class="badge-separator">·</span>
        <span class="sub-badge-meta">81.6% Retention</span>
      </div>

      <h1 class="archetype-main-title">
        <em>{archetype.title}</em>
      </h1>

      <p class="archetype-narrative">
        An archive spanning 1960s classic rock icons through 2020s modern alternative & chart hits — defined by deep discography loyalty, multi-era continuity, and 4,890+ verified catalog plays.
      </p>
    </div>

    <!-- RIGHT: Vinyl Pressing + Studio Metric Strips -->
    <div class="archetype-visual-pane">
      <!-- Spinning Physical Vinyl Record -->
      <div 
        class="chrono-vinyl-stage" 
        onclick={triggerVinylRoulette} 
        title="Click to spin vinyl roulette"
        role="button"
        tabindex="0"
        onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') triggerVinylRoulette(); }}
      >
        <div class="chrono-vinyl" class:fast-spin={isSpinningFast}>
          <div class="vinyl-groove groove-1"></div>
          <div class="vinyl-groove groove-2"></div>
          <div class="vinyl-groove groove-3"></div>
          <div class="vinyl-groove groove-4"></div>
          <div class="vinyl-label-center">
            <span class="record-rpm">33 RPM</span>
            <div class="record-spindle"></div>
            <span class="record-side">SIDE A</span>
          </div>
          <div class="vinyl-shimmer"></div>
        </div>
      </div>

      <!-- Ruled Studio Metric Strips in Running Prose -->
      <div class="stat-rows">
        <div class="stat-row">
          <div class="stat-bar signal"></div>
          <div class="stat-row-data">
            <span class="stat-row-prose">
              <strong class="num">{stats.totalHours || 327.5} hrs</strong> logged — about {stats.totalDays || 13.6} days of continuous play
            </span>
          </div>
        </div>
        <div class="stat-row">
          <div class="stat-bar oxide"></div>
          <div class="stat-row-data">
            <span class="stat-row-prose">
              <strong class="num">{(stats.totalAlbums || 329).toLocaleString()}</strong> curated albums, {stats.overallCompletionRate || 81.6}% listened through
            </span>
          </div>
        </div>
        <div class="stat-row">
          <div class="stat-bar groove"></div>
          <div class="stat-row-data">
            <span class="stat-row-prose">
              <strong>{stats.topArtist ? stats.topArtist.name : 'Linkin Park'}</strong> leads the catalog at <span class="num">{stats.topArtist ? (stats.topArtist.plays || 444).toLocaleString() : 444}</span> plays
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .archetype-hero-banner {
    position: relative;
    background: var(--pressed);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 36px 40px;
    overflow: hidden;
  }

  .archetype-hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--signal) 0%, var(--oxide) 40%, transparent 100%);
  }

  .archetype-content-grid {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 40px;
    align-items: center;
  }

  /* Story Pane */
  .archetype-story-pane {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .archetype-tag-strip {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .badge-separator {
    color: var(--groove-light);
  }

  .sub-badge-text, .sub-badge-meta {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-secondary);
  }

  .archetype-main-title {
    font-family: var(--font-serif);
    font-size: clamp(2.3rem, 4.5vw, 3.5rem);
    font-style: italic;
    font-weight: 400;
    line-height: 1.05;
    color: var(--linen);
    letter-spacing: 0.01em;
    margin: 2px 0 4px;
  }

  .archetype-narrative {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 560px;
    font-weight: 400;
  }

  /* Visual Pane (Right) */
  .archetype-visual-pane {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 28px;
  }

  /* Physical Vinyl Disc */
  .chrono-vinyl-stage {
    position: relative;
    width: 124px;
    height: 124px;
    flex-shrink: 0;
    cursor: pointer;
  }

  .chrono-vinyl {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: #0D0B09;
    border: 1px solid #2B2620;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.8), inset 0 0 8px rgba(0,0,0,0.9);
    animation: vinylSpin 28s infinite linear;
  }

  .chrono-vinyl.fast-spin {
    animation: vinylSpin 0.35s infinite linear !important;
  }

  @keyframes vinylSpin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }

  .vinyl-groove {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(234, 228, 217, 0.04);
  }
  .groove-1 { inset: 8px; }
  .groove-2 { inset: 18px; }
  .groove-3 { inset: 28px; }
  .groove-4 { inset: 36px; }

  .vinyl-label-center {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: radial-gradient(circle, #8C2219 0%, #4D120D 100%);
    border: 2px solid #1C1814;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #F5EAE0;
    z-index: 2;
    box-shadow: 0 0 6px rgba(0,0,0,0.8);
  }

  .record-rpm {
    font-family: var(--font-mono);
    font-size: 0.42rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #E2AF68;
    line-height: 1;
  }

  .record-spindle {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #000;
    border: 1px solid #5A4838;
    margin: 2px 0;
  }

  .record-side {
    font-family: var(--font-mono);
    font-size: 0.38rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #F5EAE0;
    line-height: 1;
  }

  .vinyl-shimmer {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(
      from 0deg,
      transparent 0deg,
      rgba(234, 228, 217, 0.04) 50deg,
      transparent 110deg,
      rgba(200, 147, 74, 0.07) 230deg,
      transparent 290deg
    );
    pointer-events: none;
  }

  /* Ruled Studio Metric Strips */
  .stat-rows {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 220px;
  }

  .stat-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 2px 0;
  }

  .stat-bar {
    width: 3px;
    height: 28px;
    border-radius: 1px;
    flex-shrink: 0;
  }
  .stat-bar.signal { background: var(--signal); }
  .stat-bar.oxide  { background: var(--oxide); }
  .stat-bar.groove { background: var(--groove-light); }

  .stat-row-data {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }

  .stat-row-prose {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-secondary);
    line-height: 1.4;
    letter-spacing: 0.015em;
  }
  .stat-row-prose strong {
    color: var(--linen);
    font-weight: 600;
  }

  @media (max-width: 1100px) {
    .archetype-content-grid {
      grid-template-columns: 1fr;
      gap: 28px;
    }
    .archetype-visual-pane {
      justify-content: flex-start;
      width: 100%;
    }
    .stat-rows {
      flex: 1;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }
  }

  @media (max-width: 768px) {
    .archetype-hero-banner {
      padding: 24px 20px;
    }
    .archetype-main-title {
      font-size: 1.85rem;
    }
    .chrono-vinyl-stage {
      display: none;
    }
    .stat-rows {
      grid-template-columns: 1fr;
    }
  }
</style>
