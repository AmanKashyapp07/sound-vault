<script>
  let { portfolio } = $props();
</script>

{#if portfolio.toastVisible}
  <div class="toast-container">
    <div class="toast">
      <span class="toast-dot"></span>
      <span>{portfolio.toastMessage}</span>
    </div>
  </div>
{/if}

<style>
  .toast-container {
    position: fixed; top: 22px; right: 22px;
    z-index: 400; display: flex; flex-direction: column;
    pointer-events: none;
  }
  .toast {
    background: var(--surface);
    border: 1px solid var(--border-hover);
    border-radius: var(--r-md);
    padding: 9px 16px;
    color: var(--text-primary);
    font-size: 0.8rem; font-weight: 500;
    display: flex; align-items: center; gap: 8px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    animation: toastIn 0.25s var(--ease);
  }
  @keyframes toastIn {
    from { opacity: 0; transform: translateX(16px); }
    to   { opacity: 1; transform: translateX(0); }
  }
  .toast-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); }
</style>
