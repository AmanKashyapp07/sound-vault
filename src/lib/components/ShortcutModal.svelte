<script>
  import { X, Keyboard } from 'lucide-svelte';

  let { portfolio } = $props();

  const shortcuts = [
    { key: '1', action: 'Switch to Grid View', category: 'Navigation' },
    { key: '2', action: 'Switch to Solo Deck View', category: 'Navigation' },
    { key: '3', action: 'Switch to Record Crate View', category: 'Navigation' },
    { key: 'B', action: 'Launch Artist Battle Arena', category: 'Clash' },
    { key: 'R', action: 'Spin Vinyl Roulette (Shuffle)', category: 'Discovery' },
    { key: 'T', action: 'Toggle Dark / Light Studio Mode', category: 'System' },
    { key: 'C', action: 'Open 24h Circadian Clock', category: 'Analytics' },
    { key: 'M', action: 'Music Mood Matchmaker Quiz', category: 'Discovery' },
    { key: 'E', action: 'Export Shareable Sound Capsule', category: 'Export' },
    { key: 'A', action: 'View Vault Milestones & Badges', category: 'Gamification' },
    { key: '?', action: 'Toggle Command Center Overlay', category: 'Help' },
    { key: 'Esc', action: 'Close Any Active Modal', category: 'System' }
  ];
</script>

{#if portfolio.isShortcutModalOpen}
  <div 
    class="shortcut-backdrop" 
    onclick={(e) => { if (e.target === e.currentTarget) portfolio.closeShortcuts(); }}
    onkeydown={(e) => { if (e.key === 'Escape') portfolio.closeShortcuts(); }}
    tabindex="0"
    role="dialog"
    aria-modal="true"
  >
    <div class="shortcut-modal-card surface-noise">
      
      <div class="shortcut-header">
        <div class="shortcut-title-wrap">
          <div class="keyboard-icon-box">
            <Keyboard size={15} />
          </div>
          <div>
            <h2>Keyboard Command Center</h2>
            <span class="shortcut-sub">Studio shortcuts to navigate Soundvault quickly</span>
          </div>
        </div>

        <button type="button" class="btn-close-shortcut" onclick={() => portfolio.closeShortcuts()}>
          <X size={15} />
        </button>
      </div>

      <div class="shortcuts-grid">
        {#each shortcuts as s}
          <div class="shortcut-row">
            <div class="shortcut-keycap num">{s.key}</div>
            <div class="shortcut-desc-wrap">
              <span class="shortcut-action">{s.action}</span>
              <span class="shortcut-cat">{s.category}</span>
            </div>
          </div>
        {/each}
      </div>

      <div class="shortcut-footer">
        <span>Press <strong class="num">?</strong> anywhere in Soundvault to toggle this command overlay</span>
      </div>

    </div>
  </div>
{/if}

<style>
  .shortcut-backdrop {
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

  .shortcut-modal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    width: 100%;
    max-width: 620px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
    padding: 24px 28px;
    display: flex; flex-direction: column; gap: 16px;
    animation: scaleUp 0.2s var(--ease);
  }

  @keyframes scaleUp {
    from { transform: scale(0.96); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }

  .shortcut-header {
    display: flex; align-items: center; justify-content: space-between;
  }
  .shortcut-title-wrap {
    display: flex; align-items: center; gap: 12px;
  }
  .keyboard-icon-box {
    width: 32px; height: 32px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--oxide); display: flex; align-items: center; justify-content: center;
  }
  .shortcut-title-wrap h2 {
    font-family: var(--font-serif); font-size: 1.45rem; font-weight: 400;
    color: var(--linen); letter-spacing: -0.01em;
  }
  .shortcut-sub {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-muted); display: block; margin-top: 1px;
  }

  .btn-close-shortcut {
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-muted); width: 28px; height: 28px;
    border-radius: 2px; display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.15s ease;
  }
  .btn-close-shortcut:hover {
    color: var(--linen); border-color: var(--oxide);
  }

  .shortcuts-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 8px 12px; max-height: 380px; overflow-y: auto;
  }

  .shortcut-row {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 10px; background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
  }

  .shortcut-keycap {
    min-width: 26px; height: 24px; padding: 0 6px;
    background: var(--surface); border: 1px solid var(--groove);
    border-bottom: 2px solid var(--groove-light);
    border-radius: 2px; display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.68rem; font-weight: 700;
    color: var(--oxide);
  }

  .shortcut-desc-wrap {
    display: flex; flex-direction: column; min-width: 0;
  }
  .shortcut-action {
    font-family: var(--font-mono);
    font-size: 0.72rem; color: var(--linen); font-weight: 500;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .shortcut-cat {
    font-family: var(--font-mono);
    font-size: 0.6rem; color: var(--text-muted);
  }

  .shortcut-footer {
    display: flex; align-items: center; gap: 8px;
    padding-top: 10px; border-top: 1px solid var(--border);
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-muted);
  }
  .shortcut-footer strong { color: var(--linen); }

  @media (max-width: 600px) {
    .shortcuts-grid { grid-template-columns: 1fr; }
  }
</style>
