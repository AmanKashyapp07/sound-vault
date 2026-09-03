<script>
  import { X, Trophy, Sparkles, CheckCircle2, Shield, Flame, Disc3, Clock, Headphones, Gem, Crown, Music } from 'lucide-svelte';

  let { portfolio } = $props();
  const stats = $derived(portfolio.catalogStats || {});
  const badges = $derived(stats.milestones || []);
  const unlockedCount = $derived(badges.filter(b => b.unlocked).length);
  const overallScore = $derived(stats.masteryScore || (badges.length > 0 ? Math.round(badges.reduce((acc, b) => acc + (b.progress || 0), 0) / badges.length) : 0));
  const masteryRank = $derived(stats.masteryRank || (overallScore >= 95 ? 'Sovereign' : (overallScore >= 75 ? 'Senior Archivist' : (overallScore >= 50 ? 'Lead Curator' : 'Apprentice'))));
</script>

{#if portfolio.isMilestonesModalOpen}
  <div 
    class="milestones-backdrop" 
    onclick={(e) => { if (e.target === e.currentTarget) portfolio.closeMilestones(); }}
    onkeydown={(e) => { if (e.key === 'Escape') portfolio.closeMilestones(); }}
    tabindex="0"
    role="dialog"
    aria-modal="true"
  >
    <div class="milestones-modal-card surface-noise">
      
      <!-- Header -->
      <div class="milestones-header">
        <div class="milestones-title-wrap">
          <div class="trophy-box">
            <Trophy size={16} />
          </div>
          <div>
            <h2>Vault Milestones & Achievements</h2>
            <span class="milestones-sub">Gamified listening accomplishments calculated from your Apple Music history</span>
          </div>
        </div>

        <button type="button" class="btn-close-milestones" onclick={() => portfolio.closeMilestones()} title="Close (Esc)">
          <X size={16} />
        </button>
      </div>

      <!-- Mastery Level Ribbon -->
      <div class="mastery-ribbon">
        <div class="mastery-left">
          <Sparkles size={16} class="gold-icon" />
          <div>
            <span class="mastery-title">VAULT MASTERY: {masteryRank.toUpperCase()}</span>
            <span class="mastery-sub">{unlockedCount} of {badges.length} Milestones Mastered · {overallScore}% Vault Completion</span>
          </div>
        </div>
        <div class="mastery-pct">{overallScore}%</div>
      </div>

      <!-- Badges Grid -->
      <div class="badges-grid">
        {#each badges as b}
          <div class="badge-card" class:unlocked={b.unlocked}>
            <div class="badge-icon-wrap" class:unlocked-icon={b.unlocked}>
              {#if b.id === 'centurion'}
                <Trophy size={18} class="gold-icon" />
              {:else if b.id === 'chrono-lord'}
                <Clock size={18} class="gold-icon" />
              {:else if b.id === 'marathon-titan'}
                <Headphones size={18} class="gold-icon" />
              {:else if b.id === 'iron-retention'}
                <Shield size={18} class="gold-icon" />
              {:else if b.id === 'discography-diver'}
                <Gem size={18} class="gold-icon" />
              {:else if b.id === 'anthem-loop'}
                <Flame size={18} class="gold-icon" />
              {:else if b.id === 'catalog-5k'}
                <Crown size={18} class="gold-icon" />
              {:else}
                <Music size={18} class="gold-icon" />
              {/if}

              {#if b.unlocked}
                <CheckCircle2 size={13} class="badge-check-icon" />
              {/if}
            </div>

            <div class="badge-content">
              <div class="badge-top-line">
                <span class="badge-name">{b.title}</span>
                <span class="badge-pill" class:unlocked-pill={b.unlocked}>{b.badge}</span>
              </div>
              <p class="badge-desc">{b.desc}</p>
              
              <div class="badge-progress-wrap">
                <div class="badge-progress-bar">
                  <div 
                    class="badge-progress-fill" 
                    class:unlocked-fill={b.unlocked}
                    style="width: {b.progress}%"
                  ></div>
                </div>
                <span class="badge-progress-label" class:unlocked-label={b.unlocked}>
                  {b.unlocked ? 'Mastered' : `${b.progress}%`}
                </span>
              </div>
            </div>
          </div>
        {/each}
      </div>

    </div>
  </div>
{/if}

<style>
  .milestones-backdrop {
    position: fixed; inset: 0;
    background: rgba(8, 7, 5, 0.85);
    backdrop-filter: blur(8px);
    z-index: 999;
    display: flex; align-items: center; justify-content: center;
    padding: 20px;
    animation: fadeIn 0.15s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .milestones-modal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    width: 100%;
    max-width: 740px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
    padding: 26px 30px;
    display: flex; flex-direction: column; gap: 18px;
    animation: scaleUp 0.2s var(--ease);
  }

  @keyframes scaleUp {
    from { transform: scale(0.96); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }

  .milestones-header {
    display: flex; align-items: center; justify-content: space-between;
  }
  .milestones-title-wrap {
    display: flex; align-items: center; gap: 12px;
  }
  .trophy-box {
    width: 32px; height: 32px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--oxide); display: flex; align-items: center; justify-content: center;
  }
  .milestones-title-wrap h2 {
    font-family: var(--font-serif); font-size: 1.55rem; font-weight: 400;
    font-style: italic; color: var(--linen); letter-spacing: 0.01em; line-height: 1.15;
  }
  .milestones-sub {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-muted); display: block; margin-top: 2px;
    letter-spacing: 0.02em;
  }

  .btn-close-milestones {
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-muted); width: 28px; height: 28px;
    border-radius: 2px; display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.15s ease;
  }
  .btn-close-milestones:hover {
    color: var(--linen); border-color: var(--oxide);
  }

  /* Ribbon */
  .mastery-ribbon {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--surface-2);
    border: 1px solid var(--oxide);
    border-radius: var(--r-sm); padding: 12px 16px;
  }
  .mastery-left {
    display: flex; align-items: center; gap: 10px;
  }
  :global(.gold-icon) { color: var(--oxide); }
  .mastery-title {
    font-family: var(--font-sans); font-size: 0.84rem; font-weight: 700;
    color: var(--linen); letter-spacing: 0.02em; display: block;
  }
  .mastery-sub {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-muted);
    letter-spacing: 0.02em;
  }
  .mastery-pct {
    font-family: var(--font-mono); font-size: 1.35rem; font-weight: 700;
    color: var(--oxide); letter-spacing: 0.02em;
  }

  /* Grid */
  .badges-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .badge-card {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--groove-light);
    border-radius: var(--r-sm); padding: 12px 14px;
    display: flex; gap: 12px; align-items: flex-start;
    transition: all 0.15s ease;
  }
  .badge-card:hover {
    background: var(--surface-3);
    border-color: var(--border-hover);
  }
  .badge-card.unlocked {
    border-color: rgba(200, 147, 74, 0.35);
    border-left: 3px solid var(--oxide);
  }
  .badge-card.unlocked:hover {
    border-color: var(--oxide);
  }

  .badge-icon-wrap {
    position: relative;
    width: 36px; height: 36px; border-radius: 2px;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    color: var(--text-muted);
    flex-shrink: 0;
  }
  .badge-icon-wrap.unlocked-icon {
    color: var(--oxide);
    background: rgba(200, 147, 74, 0.08);
    border-color: rgba(200, 147, 74, 0.25);
  }
  :global(.badge-check-icon) {
    position: absolute; bottom: -3px; right: -3px;
    color: var(--oxide); background: var(--surface); border-radius: 50%;
  }

  .badge-content {
    display: flex; flex-direction: column; gap: 3px; flex: 1; min-width: 0;
  }
  .badge-top-line {
    display: flex; align-items: center; justify-content: space-between; gap: 6px;
  }
  .badge-name {
    font-family: var(--font-mono); font-size: 0.82rem; font-weight: 700;
    color: var(--linen); letter-spacing: -0.01em;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .badge-pill {
    font-family: var(--font-mono);
    font-size: 0.6rem; font-weight: 600; color: var(--text-muted);
    background: var(--surface); border: 1px solid var(--border);
    padding: 1px 5px; border-radius: 2px;
    white-space: nowrap;
  }
  .badge-pill.unlocked-pill {
    color: var(--oxide);
    border-color: rgba(200, 147, 74, 0.3);
    background: rgba(200, 147, 74, 0.1);
  }

  .badge-desc {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-secondary); line-height: 1.4;
    letter-spacing: 0.01em;
  }

  .badge-progress-wrap {
    display: flex; align-items: center; gap: 8px; margin-top: 4px;
  }
  .badge-progress-bar {
    flex: 1; height: 3px; border-radius: 1px;
    background: var(--groove); overflow: hidden;
  }
  .badge-progress-fill {
    height: 100%; background: var(--oxide);
    border-radius: 1px;
    opacity: 0.75;
  }
  .badge-progress-fill.unlocked-fill {
    opacity: 1;
    background: var(--oxide);
  }
  .badge-progress-label {
    font-family: var(--font-mono); font-size: 0.62rem; color: var(--text-muted);
    min-width: 35px; text-align: right;
  }
  .badge-progress-label.unlocked-label {
    color: var(--oxide);
    font-weight: 700;
  }

  @media (max-width: 650px) {
    .badges-grid { grid-template-columns: 1fr; }
  }
</style>
