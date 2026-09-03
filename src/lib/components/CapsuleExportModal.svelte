<script>
  import { X, Download, Share2, Sparkles, Check } from 'lucide-svelte';

  let { portfolio } = $props();
  const stats = $derived(portfolio.catalogStats || {});
  const topArtist = $derived(stats.topArtist || portfolio.allArtists[0] || {});
  const topTrack = $derived(stats.topTrack || {});

  let canvasEl = $state(null);
  let isCopied = $state(false);

  function drawCapsuleCard() {
    if (!canvasEl) return;
    const ctx = canvasEl.getContext('2d');
    const width = 800;
    const height = 1100;
    canvasEl.width = width;
    canvasEl.height = height;

    // 1. Deep Matte Tape Surface Background
    ctx.fillStyle = '#0D0B09';
    ctx.fillRect(0, 0, width, height);

    // Warm Oxide Halo Gradients
    const glow1 = ctx.createRadialGradient(400, 160, 20, 400, 160, 420);
    glow1.addColorStop(0, 'rgba(200, 147, 74, 0.16)');
    glow1.addColorStop(1, 'transparent');
    ctx.fillStyle = glow1;
    ctx.fillRect(0, 0, width, height);

    const glow2 = ctx.createRadialGradient(680, 850, 10, 680, 850, 360);
    glow2.addColorStop(0, 'rgba(232, 68, 58, 0.12)');
    glow2.addColorStop(1, 'transparent');
    ctx.fillStyle = glow2;
    ctx.fillRect(0, 0, width, height);

    // 2. Archival Double Border Frame
    ctx.strokeStyle = 'rgba(200, 147, 74, 0.35)';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(36, 36, width - 72, height - 72);

    ctx.strokeStyle = 'rgba(234, 228, 217, 0.08)';
    ctx.lineWidth = 1;
    ctx.strokeRect(44, 44, width - 88, height - 88);

    // Corner Register Marks (+)
    ctx.fillStyle = 'rgba(200, 147, 74, 0.6)';
    ctx.font = '14px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('+', 36, 36);
    ctx.fillText('+', width - 36, 36);
    ctx.fillText('+', 36, height - 36);
    ctx.fillText('+', width - 36, height - 36);

    // 3. Header Wordmark & Serial
    ctx.textAlign = 'left';
    ctx.fillStyle = '#EAE4D9';
    ctx.font = 'italic 46px "Instrument Serif", Georgia, serif';
    ctx.fillText('Soundvault', 68, 100);

    ctx.fillStyle = '#C8934A';
    ctx.font = 'bold 11px "IBM Plex Mono", monospace';
    ctx.fillText('ARCHIVAL AUDIO CAPSULE · APPLE MUSIC LOG', 68, 126);

    ctx.fillStyle = '#70695E';
    ctx.font = '10px "IBM Plex Mono", monospace';
    ctx.textAlign = 'right';
    ctx.fillText('SERIES 2026 // STEREO MASTER', width - 68, 100);
    ctx.fillText('7 DECADES · 149 ARTISTS', width - 68, 118);

    // Divider Rule
    ctx.strokeStyle = 'rgba(234, 228, 217, 0.12)';
    ctx.beginPath();
    ctx.moveTo(68, 146);
    ctx.lineTo(width - 68, 146);
    ctx.stroke();

    // 4. Archetype Identity Card
    ctx.fillStyle = 'rgba(26, 23, 19, 0.85)';
    ctx.strokeStyle = 'rgba(200, 147, 74, 0.3)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(68, 168, width - 136, 120, 6);
    ctx.fill();
    ctx.stroke();

    // Oxide Left Spine on Archetype
    ctx.fillStyle = '#C8934A';
    ctx.fillRect(68, 168, 4, 120);

    ctx.textAlign = 'left';
    ctx.fillStyle = '#C8934A';
    ctx.font = 'bold 10px "IBM Plex Mono", monospace';
    ctx.fillText('CURATED LISTENER IDENTITY', 92, 198);

    ctx.fillStyle = '#EAE4D9';
    ctx.font = 'italic 32px "Instrument Serif", Georgia, serif';
    ctx.fillText(stats.archetype?.title || 'The Sonic Time-Traveler', 92, 238);

    ctx.fillStyle = '#A59B8B';
    ctx.font = '12px "IBM Plex Mono", monospace';
    ctx.fillText('7 Eras Spanned · 81.6% Retention · 13.7 Days Audio', 92, 266);

    // 5. Four Core Studio Ledger Cards (2x2 Grid)
    const cards = [
      {
        label: 'TOTAL LISTENING TIME',
        val: `${stats.totalHours || 328.6} hrs`,
        sub: `~${stats.totalDays || 13.7} Days Continuous Play`,
        color: '#EAE4D9'
      },
      {
        label: 'VERIFIED PLAYBACK',
        val: `${(stats.totalPlays || 4909).toLocaleString()}`,
        sub: `${stats.totalSongs || 611} Tracks · ${stats.totalAlbums || 280} Albums`,
        color: '#C8934A'
      },
      {
        label: 'FLAGSHIP ARTIST',
        val: topArtist.name || 'Linkin Park',
        sub: `${topArtist.totalPlays || 444} Verified Plays (${topArtist.trackCount || 56} Tracks)`,
        color: '#E8443A'
      },
      {
        label: 'TOP SINGLE ON LOOP',
        val: `"${topTrack.title || 'Babydoll'}"`,
        sub: `${topTrack.plays || 146} Plays · ${topTrack.artist || 'Dominic Fike'}`,
        color: '#EAE4D9'
      }
    ];

    cards.forEach((c, idx) => {
      const col = idx % 2;
      const row = Math.floor(idx / 2);
      const cardX = 68 + col * 342;
      const cardY = 312 + row * 160;
      const cardW = 322;
      const cardH = 142;

      ctx.fillStyle = 'rgba(26, 23, 19, 0.7)';
      ctx.strokeStyle = 'rgba(234, 228, 217, 0.09)';
      ctx.beginPath();
      ctx.roundRect(cardX, cardY, cardW, cardH, 4);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#70695E';
      ctx.font = 'bold 9px "IBM Plex Mono", monospace';
      ctx.fillText(c.label, cardX + 20, cardY + 32);

      ctx.fillStyle = c.color;
      ctx.font = 'bold 28px "IBM Plex Mono", monospace';
      ctx.fillText(c.val, cardX + 20, cardY + 76);

      ctx.fillStyle = '#A59B8B';
      ctx.font = '11px "IBM Plex Mono", monospace';
      ctx.fillText(c.sub, cardX + 20, cardY + 112);
    });

    // 6. Chronological Spectrum Ribbon
    ctx.fillStyle = 'rgba(26, 23, 19, 0.7)';
    ctx.strokeStyle = 'rgba(234, 228, 217, 0.09)';
    ctx.beginPath();
    ctx.roundRect(68, 656, width - 136, 120, 4);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#70695E';
    ctx.font = 'bold 9px "IBM Plex Mono", monospace';
    ctx.fillText('CHRONOLOGY INDEX (1960s — 2020s)', 92, 686);

    const decades = [
      { name: "60s", plays: 24 },
      { name: "70s", plays: 142 },
      { name: "80s", plays: 480 },
      { name: "90s", plays: 310 },
      { name: "00s", plays: 1280 },
      { name: "10s", plays: 1650 },
      { name: "20s", plays: 1023 }
    ];

    const maxDecade = Math.max(...decades.map(d => d.plays));
    decades.forEach((d, i) => {
      const decX = 92 + i * 92;
      const decY = 712;
      const pct = (d.plays / maxDecade);
      const barH = Math.max(8, pct * 34);

      ctx.fillStyle = i >= 4 ? '#E8443A' : '#C8934A';
      ctx.fillRect(decX, decY + 34 - barH, 20, barH);

      ctx.fillStyle = '#A59B8B';
      ctx.font = '9px "IBM Plex Mono", monospace';
      ctx.fillText(d.name, decX + 2, decY + 48);
    });

    // 7. Top 5 Power Artists Strip
    ctx.fillStyle = 'rgba(26, 23, 19, 0.7)';
    ctx.strokeStyle = 'rgba(234, 228, 217, 0.09)';
    ctx.beginPath();
    ctx.roundRect(68, 798, width - 136, 150, 4);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#70695E';
    ctx.font = 'bold 9px "IBM Plex Mono", monospace';
    ctx.fillText('TOP ARCHIVED ARTISTS', 92, 826);

    const topArtists = (portfolio.allArtists || []).slice(0, 4);
    topArtists.forEach((art, aIdx) => {
      const rowY = 852 + aIdx * 24;
      ctx.fillStyle = '#C8934A';
      ctx.font = 'bold 11px "IBM Plex Mono", monospace';
      ctx.fillText(`0${aIdx + 1}`, 92, rowY);

      ctx.fillStyle = '#EAE4D9';
      ctx.font = '600 12px "IBM Plex Mono", monospace';
      ctx.fillText(art.name, 126, rowY);

      ctx.fillStyle = '#70695E';
      ctx.font = '11px "IBM Plex Mono", monospace';
      ctx.textAlign = 'right';
      ctx.fillText(`${art.totalPlays} plays`, width - 92, rowY);
      ctx.textAlign = 'left';
    });

    // 8. Studio Footer Stamp
    ctx.textAlign = 'center';
    ctx.fillStyle = '#70695E';
    ctx.font = '10px "IBM Plex Mono", monospace';
    ctx.fillText('SOUNDVAULT RECORDING LOG · MASTER COPIES · AMANKASHYAPP07.GITHUB.IO/SOUND-VAULT', width / 2, 1020);
  }

  // Reactive effect to render canvas whenever modal is opened
  $effect(() => {
    if (portfolio.isCapsuleModalOpen && canvasEl) {
      drawCapsuleCard();
    }
  });

  function downloadPNG() {
    if (!canvasEl) return;
    const link = document.createElement('a');
    link.download = `soundvault-capsule-${Date.now()}.png`;
    link.href = canvasEl.toDataURL('image/png');
    link.click();
    portfolio.showToast('Sound Capsule PNG downloaded');
  }

  async function copyToClipboard() {
    if (!canvasEl) return;
    try {
      canvasEl.toBlob(async (blob) => {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ]);
        isCopied = true;
        portfolio.showToast('Image copied to clipboard');
        setTimeout(() => isCopied = false, 2500);
      });
    } catch (e) {
      downloadPNG();
    }
  }
</script>

{#if portfolio.isCapsuleModalOpen}
  <div 
    class="capsule-backdrop" 
    onclick={(e) => { if (e.target === e.currentTarget) portfolio.closeCapsule(); }}
    onkeydown={(e) => { if (e.key === 'Escape') portfolio.closeCapsule(); }}
    tabindex="0"
    role="dialog"
    aria-modal="true"
  >
    <div class="capsule-modal-card surface-noise">
      
      <div class="capsule-header">
        <div class="capsule-title-wrap">
          <div class="capsule-icon-box">
            <Sparkles size={16} />
          </div>
          <div>
            <h2>Shareable Sound Capsule</h2>
            <span class="capsule-sub">High-resolution archival stats poster generated from your library</span>
          </div>
        </div>

        <button type="button" class="btn-close-capsule" onclick={() => portfolio.closeCapsule()} title="Close (Esc)">
          <X size={16} />
        </button>
      </div>

      <!-- Preview Canvas Stage -->
      <div class="capsule-stage-wrap">
        <canvas bind:this={canvasEl} class="capsule-canvas-preview"></canvas>
      </div>

      <!-- Action Buttons -->
      <div class="capsule-actions-row">
        <button type="button" class="btn-capsule-action primary" onclick={downloadPNG}>
          <Download size={14} />
          <span>Download High-Res PNG</span>
        </button>
        <button type="button" class="btn-capsule-action secondary" onclick={copyToClipboard}>
          {#if isCopied}
            <Check size={14} />
            <span>Copied to Clipboard!</span>
          {:else}
            <Share2 size={14} />
            <span>Copy Image</span>
          {/if}
        </button>
      </div>

    </div>
  </div>
{/if}

<style>
  .capsule-backdrop {
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

  .capsule-modal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    width: 100%;
    max-width: 480px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
    padding: 24px 28px;
    display: flex; flex-direction: column; gap: 16px;
    animation: scaleUp 0.2s var(--ease);
  }

  @keyframes scaleUp {
    from { transform: scale(0.96); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }

  .capsule-header {
    display: flex; align-items: center; justify-content: space-between;
  }
  .capsule-title-wrap {
    display: flex; align-items: center; gap: 12px;
  }
  .capsule-icon-box {
    width: 32px; height: 32px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--oxide); display: flex; align-items: center; justify-content: center;
  }
  .capsule-title-wrap h2 {
    font-family: var(--font-serif); font-size: 1.55rem; font-weight: 400;
    font-style: italic; color: var(--linen); letter-spacing: 0.01em; line-height: 1.15;
  }
  .capsule-sub {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-muted); display: block; margin-top: 2px;
    letter-spacing: 0.02em;
  }

  .btn-close-capsule {
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-muted); width: 28px; height: 28px;
    border-radius: 2px; display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.15s ease;
  }
  .btn-close-capsule:hover {
    color: var(--linen); border-color: var(--oxide);
  }

  .capsule-stage-wrap {
    display: flex; justify-content: center; align-items: center;
    background: #080706; border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 12px;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.6);
  }
  .capsule-canvas-preview {
    max-width: 100%; height: auto; max-height: 440px;
    border-radius: var(--r-sm);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8);
  }

  .capsule-actions-row {
    display: flex; gap: 10px;
  }
  .btn-capsule-action {
    flex: 1; height: 38px;
    border-radius: var(--r-sm); font-family: var(--font-mono);
    font-size: 0.74rem; font-weight: 600;
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    cursor: pointer; transition: all 0.15s ease;
    letter-spacing: 0.02em;
  }
  .btn-capsule-action.primary {
    background: var(--signal);
    border: 1px solid var(--signal);
    color: #fff;
  }
  .btn-capsule-action.primary:hover {
    background: #d4382e;
    transform: translateY(-1px);
  }
  .btn-capsule-action.secondary {
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--linen);
  }
  .btn-capsule-action.secondary:hover {
    background: var(--surface-3); border-color: var(--oxide);
  }
</style>
