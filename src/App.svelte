<script>
  import { createPortfolioState } from './lib/stores/portfolioState.svelte.js';
  import Navbar from './lib/components/Navbar.svelte';
  import ArchetypeBanner from './lib/components/ArchetypeBanner.svelte';
  import ListeningAnalytics from './lib/components/ListeningAnalytics.svelte';
  import Leaderboard from './lib/components/Leaderboard.svelte';
  import DecadeHorizon from './lib/components/DecadeHorizon.svelte';
  import ControlsBar from './lib/components/ControlsBar.svelte';
  import FlashcardGrid from './lib/components/FlashcardGrid.svelte';
  import SoloDeck from './lib/components/SoloDeck.svelte';
  import ConstellationGalaxy from './lib/components/ConstellationGalaxy.svelte';
  import DiscographyModal from './lib/components/DiscographyModal.svelte';
  import ArtistBattleModal from './lib/components/ArtistBattleModal.svelte';
  import ListeningClock from './lib/components/ListeningClock.svelte';
  import CapsuleExportModal from './lib/components/CapsuleExportModal.svelte';
  import MilestonesModal from './lib/components/MilestonesModal.svelte';
  import MoodQuizModal from './lib/components/MoodQuizModal.svelte';
  import ShortcutModal from './lib/components/ShortcutModal.svelte';
  import Toast from './lib/components/Toast.svelte';

  const portfolio = createPortfolioState();

  function handleKeydown(e) {
    if (
      portfolio.selectedArtistModal || 
      portfolio.isBattleModalOpen || 
      portfolio.isClockModalOpen || 
      portfolio.isCapsuleModalOpen || 
      portfolio.isMilestonesModalOpen || 
      portfolio.isMoodModalOpen ||
      portfolio.isShortcutModalOpen
    ) {
      if (e.key === 'Escape') {
        portfolio.closeModal();
        portfolio.closeBattle();
        portfolio.closeClock();
        portfolio.closeCapsule();
        portfolio.closeMilestones();
        portfolio.closeMood();
        portfolio.closeShortcuts();
      }
      return;
    }

    // Ignore hotkeys when typing in input fields
    if (['INPUT', 'TEXTAREA'].includes(e.target?.tagName)) return;

    if (e.key === '1') portfolio.activeView = 'grid';
    if (e.key === '2') portfolio.activeView = 'deck';
    if (e.key === '3') portfolio.activeView = 'galaxy';
    if (e.key === 't' || e.key === 'T') portfolio.toggleThemeMode();
    if (e.key === 'b' || e.key === 'B') portfolio.openBattle();
    if (e.key === 'r' || e.key === 'R') portfolio.shuffleVault();
    if (e.key === 'c' || e.key === 'C') portfolio.openClock();
    if (e.key === 'm' || e.key === 'M') portfolio.openMood();
    if (e.key === 'e' || e.key === 'E') portfolio.openCapsule();
    if (e.key === 'a' || e.key === 'A') portfolio.openMilestones();
    if (e.key === '?' || e.key === '/') {
      e.preventDefault();
      portfolio.openShortcuts();
    }

    if (portfolio.activeView === 'deck') {
      if (e.key === 'ArrowLeft') portfolio.prevSoloCard();
      if (e.key === 'ArrowRight') portfolio.nextSoloCard();
    }
  }

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const totalFilteredPlays = $derived(
    portfolio.filteredArtists.reduce((acc, a) => acc + (a.totalPlays || 0), 0)
  );
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="ambient-background"></div>
<Toast {portfolio} />

<div class="app-container">
  <Navbar {portfolio} />

  <ArchetypeBanner {portfolio} />

  <section class="analytics-hero-section">
    <ListeningAnalytics {portfolio} />
    <Leaderboard {portfolio} />
  </section>

  <DecadeHorizon {portfolio} />

  <ControlsBar {portfolio} />

  <main>
    {#if portfolio.activeView === 'grid'}
      <FlashcardGrid {portfolio} />
    {:else if portfolio.activeView === 'deck'}
      <SoloDeck {portfolio} />
    {:else if portfolio.activeView === 'galaxy'}
      <ConstellationGalaxy {portfolio} />
    {/if}

    <div class="catalog-footer">
      <span class="num">Showing {portfolio.filteredArtists.length} of {portfolio.allArtists.length} artists / {totalFilteredPlays.toLocaleString()} total plays</span>
      <button type="button" class="btn-to-top" onclick={scrollToTop}>↑ Top of Archive</button>
    </div>
  </main>
</div>

<!-- Modals & Overlays -->
<DiscographyModal {portfolio} />
<ArtistBattleModal {portfolio} />
<ListeningClock {portfolio} />
<CapsuleExportModal {portfolio} />
<MilestonesModal {portfolio} />
<MoodQuizModal {portfolio} />
<ShortcutModal {portfolio} />

<style>
  .analytics-hero-section {
    display: grid;
    grid-template-columns: 0.95fr 1.05fr;
    gap: 20px;
    align-items: stretch;
  }

  .catalog-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 24px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .btn-to-top {
    padding: 6px 14px;
    border-radius: var(--r-sm);
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-to-top:hover {
    border-color: var(--oxide);
    color: var(--linen);
  }

  @media (max-width: 1024px) {
    .analytics-hero-section {
      grid-template-columns: 1fr;
    }
  }
</style>
