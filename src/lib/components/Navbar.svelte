<script>
  import { LayoutGrid, Layers, Disc3, Swords, Shuffle, Wand2, Sun, Moon } from 'lucide-svelte';

  let { portfolio } = $props();
  const stats = $derived(portfolio.catalogStats || {});
</script>

<header class="navbar surface-noise">
  <!-- 1. LEFT: Brand Identity -->
  <div class="nav-left">
    <a href="/" class="nav-brand">
      <div class="brand-icon-wrapper">
        <Disc3 size={15} strokeWidth={2.2} />
      </div>
      <div class="brand-wordmark">
        <span class="brand-title">Soundvault</span>
        <span class="brand-sub">{(stats.totalArtists || 149)} artists · {(stats.totalPlays || 4890).toLocaleString()} plays</span>
      </div>
    </a>
  </div>

  <!-- 2. CENTER: Main View Mode Switcher -->
  <div class="nav-center">
    <nav class="nav-view-switcher" aria-label="Catalog views">
      <button 
        type="button" 
        class="view-mode-btn" 
        class:active={portfolio.activeView === 'grid'}
        onclick={() => portfolio.activeView = 'grid'}
        title="Grid View (Hotkey: 1)"
      >
        <LayoutGrid size={12} strokeWidth={2} />
        <span>Grid</span>
      </button>

      <button 
        type="button" 
        class="view-mode-btn" 
        class:active={portfolio.activeView === 'deck'}
        onclick={() => portfolio.activeView = 'deck'}
        title="Solo Deck View (Hotkey: 2)"
      >
        <Layers size={12} strokeWidth={2} />
        <span>Deck</span>
      </button>

      <button 
        type="button" 
        class="view-mode-btn" 
        class:active={portfolio.activeView === 'galaxy'}
        onclick={() => portfolio.activeView = 'galaxy'}
        title="Record Crate View (Hotkey: 3)"
      >
        <Disc3 size={12} strokeWidth={2} />
        <span>Crate</span>
      </button>
    </nav>
  </div>

  <!-- 3. RIGHT: Studio Tools, Theme & Shortcuts -->
  <div class="nav-right">
    <div class="studio-toolbar">
      <!-- Quick Action Buttons -->
      <button 
        type="button" 
        class="tool-btn" 
        title="Shuffle Vault / Spin Vinyl (Hotkey: R)"
        onclick={() => portfolio.shuffleVault()}
      >
        <Shuffle size={12} strokeWidth={2} />
        <span>Shuffle</span>
      </button>

      <button 
        type="button" 
        class="tool-btn" 
        title="Music Mood Matchmaker (Hotkey: M)"
        onclick={() => portfolio.openMood()}
      >
        <Wand2 size={12} strokeWidth={2} />
        <span>Mood</span>
      </button>

      <button 
        type="button" 
        class="tool-btn" 
        title="Artist Battle Arena (Hotkey: B)"
        onclick={() => portfolio.openBattle()}
      >
        <Swords size={12} strokeWidth={2} />
        <span>VS Arena</span>
      </button>

      <div class="toolbar-divider"></div>

      <!-- Theme Switcher (Quick Toggle + Palette) -->
      <button 
        type="button" 
        class="theme-toggle-btn"
        title="Toggle Dark / Light Mode (Hotkey: T)"
        onclick={() => portfolio.toggleThemeMode()}
      >
        {#if portfolio.theme === 'light'}
          <Moon size={12} strokeWidth={2} />
        {:else}
          <Sun size={12} strokeWidth={2} />
        {/if}
      </button>

      <div class="theme-palette-wrap" title="Switch studio palette">
        <button 
          type="button" 
          class="theme-dot obsidian" 
          class:active={portfolio.theme === 'obsidian'}
          title="Mastering Room (Default)"
          onclick={() => portfolio.setTheme('obsidian')}
        ></button>
        <button 
          type="button" 
          class="theme-dot amber" 
          class:active={portfolio.theme === 'amber'}
          title="Tape Oxide Amber"
          onclick={() => portfolio.setTheme('amber')}
        ></button>
        <button 
          type="button" 
          class="theme-dot amoled" 
          class:active={portfolio.theme === 'amoled'}
          title="Vinyl Wax Black"
          onclick={() => portfolio.setTheme('amoled')}
        ></button>
        <button 
          type="button" 
          class="theme-dot light" 
          class:active={portfolio.theme === 'light'}
          title="Archival Paper Light"
          onclick={() => portfolio.setTheme('light')}
        ></button>
      </div>

      <!-- Shortcuts Key -->
      <button 
        type="button" 
        class="tool-btn-icon" 
        title="Keyboard Command Center (Hotkey: ?)"
        onclick={() => portfolio.openShortcuts()}
      >
        <span>?</span>
      </button>
    </div>
  </div>
</header>

<style>
  .navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 18px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    gap: 16px;
    min-height: 52px;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
  }

  /* 1. LEFT: Brand */
  .nav-left {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-shrink: 0;
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: inherit;
  }

  .brand-icon-wrapper {
    width: 28px;
    height: 28px;
    border-radius: var(--r-sm);
    background: var(--surface-2);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--oxide);
    flex-shrink: 0;
  }

  .brand-wordmark {
    display: flex;
    flex-direction: column;
  }

  .brand-title {
    font-family: var(--font-serif);
    font-size: 1.15rem;
    font-style: italic;
    font-weight: 400;
    letter-spacing: -0.01em;
    color: var(--linen);
    line-height: 1;
  }

  .brand-sub {
    font-size: 0.62rem;
    font-weight: 400;
    letter-spacing: 0.02em;
    color: var(--text-muted);
    font-family: var(--font-mono);
    margin-top: 2px;
  }

  /* 2. CENTER: View Switcher */
  .nav-center {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .nav-view-switcher {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    height: 32px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 2px;
    box-sizing: border-box;
  }

  .view-mode-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 100%;
    padding: 0 12px;
    border-radius: 3px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 500;
    cursor: pointer;
    transition: color 0.15s ease, background-color 0.15s ease;
    white-space: nowrap;
  }

  .view-mode-btn:hover {
    color: var(--text-primary);
  }

  .view-mode-btn.active {
    background: var(--surface);
    color: var(--linen);
    font-weight: 600;
    border: 1px solid var(--border);
  }

  /* 3. RIGHT: Studio Toolbar */
  .nav-right {
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }

  .studio-toolbar {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 2px 4px;
    height: 32px;
    box-sizing: border-box;
  }

  .tool-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    height: 26px;
    padding: 0 8px;
    border-radius: 3px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 500;
    cursor: pointer;
    transition: color 0.15s ease;
    white-space: nowrap;
  }

  .tool-btn:hover {
    color: var(--text-primary);
  }

  .toolbar-divider {
    width: 1px;
    height: 14px;
    background: var(--border);
    margin: 0 2px;
  }

  .theme-toggle-btn {
    width: 24px;
    height: 24px;
    border-radius: 3px;
    background: transparent;
    border: none;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: color 0.15s ease;
  }
  .theme-toggle-btn:hover {
    color: var(--text-primary);
  }

  /* Theme Palette Dots */
  .theme-palette-wrap {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 0 4px;
  }

  .theme-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: 1px solid transparent;
    cursor: pointer;
    padding: 0;
  }
  .theme-dot.obsidian { background: #E8443A; }
  .theme-dot.amber { background: #C8934A; }
  .theme-dot.amoled { background: #000000; border-color: #4D463E; }
  .theme-dot.light { background: #FCFAF6; border-color: #9C6B28; }

  .theme-dot.active {
    border-color: var(--linen);
    outline: 1px solid var(--oxide);
    outline-offset: 1px;
  }

  /* Shortcut Icon Button */
  .tool-btn-icon {
    width: 22px;
    height: 22px;
    border-radius: 3px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .tool-btn-icon:hover {
    background: var(--surface-3);
    color: var(--text-primary);
    border-color: var(--oxide);
  }



  @media (max-width: 768px) {
    .navbar { flex-wrap: wrap; }
    .nav-center { order: 3; width: 100%; justify-content: center; margin-top: 6px; }
    .tool-btn span { display: none; }
    .tool-btn { padding: 0 6px; }
  }
</style>


