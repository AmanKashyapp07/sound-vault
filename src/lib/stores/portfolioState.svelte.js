import { 
  initSqliteDatabase, 
  getAllArtists, 
  getCatalogStats, 
  filterArtistsSql, 
  runSqlQuery,
  onDatabaseReady 
} from '../db/database.js';

export function createPortfolioState() {
  let dbReady = $state(false);
  let allArtists = $state(getAllArtists());
  let catalogStats = $state(getCatalogStats());

  // Initialize SQLite in-memory engine
  if (typeof window !== 'undefined') {
    initSqliteDatabase().then(() => {
      dbReady = true;
      allArtists = getAllArtists();
      catalogStats = getCatalogStats();
    });

    onDatabaseReady(() => {
      dbReady = true;
      allArtists = getAllArtists();
      catalogStats = getCatalogStats();
    });
  }

  let activeView = $state('grid'); // 'grid' | 'deck' | 'galaxy'
  let searchQuery = $state('');
  let activeDecade = $state('all');
  let activeGenre = $state('all');
  let sortBy = $state('plays-desc');
  let leaderboardTab = $state('artists'); // 'artists' | 'songs'
  let selectedArtistModal = $state(null);
  let currentSoloIndex = $state(0);
  let toastMessage = $state('');
  let toastVisible = $state(false);
  let toastTimeout = null;

  const filteredArtists = $derived.by(() => {
    return filterArtistsSql({
      search: searchQuery,
      decade: activeDecade,
      genre: activeGenre,
      sortBy: sortBy
    });
  });

  let isBattleModalOpen = $state(false);
  let battleArtist1 = $state(null);
  let battleArtist2 = $state(null);

  let isClockModalOpen = $state(false);
  let isMilestonesModalOpen = $state(false);
  let isCapsuleModalOpen = $state(false);
  let isMoodModalOpen = $state(false);
  let isShortcutModalOpen = $state(false);

  const initialTheme = typeof localStorage !== 'undefined' ? (localStorage.getItem('soundvault_theme') || 'obsidian') : 'obsidian';
  let theme = $state(initialTheme);

  function setTheme(newTheme) {
    theme = newTheme;
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('soundvault_theme', newTheme);
    }
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', newTheme);
    }
    showToast(`Switched theme to: ${newTheme.toUpperCase()}`);
  }

  // Initialize theme on mount if in browser
  if (typeof document !== 'undefined') {
    document.documentElement.setAttribute('data-theme', initialTheme);
  }

  function showToast(msg) {
    toastMessage = msg;
    toastVisible = true;
    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      toastVisible = false;
    }, 2200);
  }

  function openModal(artist) {
    selectedArtistModal = artist;
  }

  function closeModal() {
    selectedArtistModal = null;
  }

  function openBattle(artistA = null, artistB = null) {
    battleArtist1 = artistA || allArtists[0] || null;
    battleArtist2 = artistB || allArtists[1] || allArtists[0] || null;
    isBattleModalOpen = true;
  }

  function closeBattle() {
    isBattleModalOpen = false;
  }

  function openClock() { isClockModalOpen = true; }
  function closeClock() { isClockModalOpen = false; }

  function openMilestones() { isMilestonesModalOpen = true; }
  function closeMilestones() { isMilestonesModalOpen = false; }

  function openCapsule() { isCapsuleModalOpen = true; }
  function closeCapsule() { isCapsuleModalOpen = false; }

  function openMood() { isMoodModalOpen = true; }
  function closeMood() { isMoodModalOpen = false; }

  function openShortcuts() { isShortcutModalOpen = true; }
  function closeShortcuts() { isShortcutModalOpen = false; }

  function shuffleVault() {
    if (allArtists.length === 0) return;
    const randomIndex = Math.floor(Math.random() * allArtists.length);
    const chosen = allArtists[randomIndex];
    
    // Find index in filtered or show directly
    const filteredIdx = filteredArtists.findIndex(a => a.id === chosen.id);
    if (filteredIdx !== -1) {
      currentSoloIndex = filteredIdx;
    }
    
    showToast(`Dropped needle on: ${chosen.name}`);
    openModal(chosen);
  }

  function nextSoloCard() {
    if (filteredArtists.length === 0) return;
    currentSoloIndex = (currentSoloIndex + 1) % filteredArtists.length;
  }

  function prevSoloCard() {
    if (filteredArtists.length === 0) return;
    currentSoloIndex = (currentSoloIndex - 1 + filteredArtists.length) % filteredArtists.length;
  }

  return {
    get allArtists() { return allArtists; },
    get catalogStats() { return catalogStats; },
    get filteredArtists() { return filteredArtists; },
    get activeView() { return activeView; },
    set activeView(val) { activeView = val; },
    get searchQuery() { return searchQuery; },
    set searchQuery(val) { searchQuery = val; },
    get activeDecade() { return activeDecade; },
    set activeDecade(val) { activeDecade = val; },
    get activeGenre() { return activeGenre; },
    set activeGenre(val) { activeGenre = val; },
    get sortBy() { return sortBy; },
    set sortBy(val) { sortBy = val; },
    get leaderboardTab() { return leaderboardTab; },
    set leaderboardTab(val) { leaderboardTab = val; },
    get selectedArtistModal() { return selectedArtistModal; },
    get currentSoloIndex() { return currentSoloIndex; },
    set currentSoloIndex(val) { currentSoloIndex = val; },
    get toastMessage() { return toastMessage; },
    get toastVisible() { return toastVisible; },
    get isBattleModalOpen() { return isBattleModalOpen; },
    get battleArtist1() { return battleArtist1; },
    set battleArtist1(val) { battleArtist1 = val; },
    get battleArtist2() { return battleArtist2; },
    set battleArtist2(val) { battleArtist2 = val; },
    get isClockModalOpen() { return isClockModalOpen; },
    get isMilestonesModalOpen() { return isMilestonesModalOpen; },
    get isCapsuleModalOpen() { return isCapsuleModalOpen; },
    get isMoodModalOpen() { return isMoodModalOpen; },
    get isShortcutModalOpen() { return isShortcutModalOpen; },
    get dbReady() { return dbReady; },
    runSql: runSqlQuery,
    get theme() { return theme; },
    setTheme,
    showToast,
    openModal,
    closeModal,
    openBattle,
    closeBattle,
    openClock,
    closeClock,
    openMilestones,
    closeMilestones,
    openCapsule,
    closeCapsule,
    openMood,
    closeMood,
    openShortcuts,
    closeShortcuts,
    shuffleVault,
    nextSoloCard,
    prevSoloCard
  };
}
