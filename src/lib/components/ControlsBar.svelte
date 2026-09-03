<script>
  import { Search, X } from 'lucide-svelte';

  let { portfolio } = $props();

  const decades = ['all', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'];
  const genres = [
    { label: 'All genres', val: 'all' },
    { label: 'Classic Rock', val: 'Classic Rock' },
    { label: 'Nu-Metal / Alt Rock', val: 'Nu-Metal / Alt Rock' },
    { label: 'Indie / Alt Rock', val: 'Indie / Alt Rock' },
    { label: '80s/90s Pop', val: '80s/90s Pop' },
    { label: 'Hip-Hop / Rap', val: 'Hip-Hop / Rap' },
    { label: 'Modern Pop', val: 'Modern Pop / Chart' },
    { label: 'Grunge', val: 'Grunge / Alt Rock' },
    { label: 'Smooth Soul / R&B', val: 'Smooth Soul / R&B' },
    { label: 'Electronic', val: 'Eurodance / Electronic' },
    { label: 'Cinematic / OST', val: 'Cinematic / OST' }
  ];

  function handleSortChange(e) {
    portfolio.sortBy = e.target.value;
    const selectedText = e.target.options[e.target.selectedIndex].text;
    portfolio.showToast(`Sorted by ${selectedText}`);
  }
</script>

<section class="catalog-controls-bar surface-noise">
  <div class="search-and-sort-row">
    <div class="search-input-wrapper">
      <Search size={13} class="search-icon" />
      <input 
        type="text" 
        class="search-input" 
        placeholder="Filter catalog by artist, track, composition, era…"
        bind:value={portfolio.searchQuery}
      />
      {#if portfolio.searchQuery}
        <button 
          type="button" 
          class="search-clear-btn visible" 
          onclick={() => portfolio.searchQuery = ''}
          title="Clear filter"
        >
          <X size={12} />
        </button>
      {/if}
    </div>

    <select class="custom-select" value={portfolio.sortBy} onchange={handleSortChange}>
      <option value="plays-desc">Sort: Most played</option>
      <option value="hours-desc">Sort: Listening hours</option>
      <option value="tracks-desc">Sort: Track count</option>
      <option value="albums-desc">Sort: Album count</option>
      <option value="completion-desc">Sort: Retention rate</option>
      <option value="name-asc">Sort: A – Z</option>
    </select>
  </div>

  <div class="filter-pills-scroll">
    {#each decades as dec}
      <button 
        type="button"
        class="filter-pill" 
        class:active={portfolio.activeDecade === dec}
        onclick={() => portfolio.activeDecade = dec}
      >
        {dec === 'all' ? 'All eras' : dec}
      </button>
    {/each}
  </div>

  <div class="filter-pills-scroll">
    {#each genres as g}
      <button 
        type="button"
        class="filter-pill" 
        class:active={portfolio.activeGenre === g.val}
        onclick={() => portfolio.activeGenre = g.val}
      >
        {g.label}
      </button>
    {/each}
  </div>
</section>

<style>
  .catalog-controls-bar {
    display: flex; flex-direction: column; gap: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
  }

  .search-and-sort-row {
    display: flex; gap: 10px; align-items: center;
  }

  .search-input-wrapper {
    position: relative; flex: 1; display: flex; align-items: center;
  }

  :global(.search-icon) {
    position: absolute; left: 12px;
    color: var(--text-muted); pointer-events: none;
  }

  .search-input {
    width: 100%; height: 36px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 0 32px 0 34px;
    color: var(--linen);
    font-family: var(--font-mono);
    font-size: 0.76rem; font-weight: 400;
    outline: none; transition: border-color 0.15s ease;
  }
  .search-input:focus {
    border-color: var(--oxide);
  }
  .search-input::placeholder { color: var(--text-muted); }

  .search-clear-btn {
    position: absolute; right: 8px;
    width: 20px; height: 20px; border-radius: 2px;
    background: var(--surface-3); border: 1px solid var(--border);
    color: var(--text-muted); cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: color 0.15s ease;
  }
  .search-clear-btn:hover { color: var(--linen); }

  .custom-select {
    height: 36px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 0 12px;
    color: var(--linen);
    font-family: var(--font-mono);
    font-size: 0.74rem; font-weight: 500;
    outline: none; cursor: pointer;
    transition: border-color 0.15s ease;
    min-width: 180px;
  }
  .custom-select:hover { border-color: var(--border-hover); }
  .custom-select:focus { border-color: var(--oxide); }

  .filter-pills-scroll {
    display: flex; gap: 5px; overflow-x: auto;
    padding-bottom: 2px; scrollbar-width: none;
  }
  .filter-pills-scroll::-webkit-scrollbar { display: none; }

  .filter-pill {
    padding: 4px 10px;
    border-radius: 3px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.68rem; font-weight: 500;
    cursor: pointer; white-space: nowrap; flex-shrink: 0;
    transition: all 0.15s ease;
  }
  .filter-pill:hover {
    border-color: var(--oxide); color: var(--linen);
  }
  .filter-pill.active {
    background: var(--surface-3);
    border-color: var(--oxide);
    color: var(--linen);
    font-weight: 600;
  }

  @media (max-width: 768px) {
    .search-and-sort-row { flex-direction: column; align-items: stretch; }
  }
</style>
