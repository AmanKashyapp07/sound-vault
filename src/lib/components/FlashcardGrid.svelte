<script>
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';
  import FlashcardItem from './FlashcardItem.svelte';

  let { portfolio } = $props();
</script>

<div class="flashcards-grid-view">
  {#if portfolio.filteredArtists.length === 0}
    <div class="empty-state">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/>
      </svg>
      <h3>No Artists Found</h3>
      <p>Try adjusting your search keywords or active genre and era filters.</p>
    </div>
  {:else}
    {#each portfolio.filteredArtists as artist (artist.id)}
      <div animate:flip={{ duration: 350 }} transition:fade={{ duration: 200 }}>
        <FlashcardItem {artist} {portfolio} />
      </div>
    {/each}
  {/if}
</div>

<style>
  .flashcards-grid-view {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
    align-items: stretch;
  }

  .empty-state {
    grid-column: 1 / -1;
    text-align: center;
    padding: 80px 20px;
    color: var(--text-muted);
  }
  .empty-state svg { opacity: 0.3; margin-bottom: 14px; }
  .empty-state h3 {
    font-family: var(--font-display); font-weight: 600;
    color: var(--text-secondary); margin-bottom: 6px;
  }
  .empty-state p { font-size: 0.83rem; }

  @media (max-width: 680px) {
    .flashcards-grid-view { grid-template-columns: 1fr; }
  }
</style>
