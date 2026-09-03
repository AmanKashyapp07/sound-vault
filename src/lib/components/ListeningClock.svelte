<script>
  import { onDestroy } from 'svelte';
  import { X, Clock, Moon, Sun, Sunset, Sunrise, Sparkles } from 'lucide-svelte';

  let { portfolio } = $props();
  const stats = $derived(portfolio.catalogStats || {});
  const clockData = $derived(stats.circadianClock || {
    hourCounts: [120, 80, 45, 20, 15, 30, 90, 160, 240, 310, 280, 260, 310, 340, 390, 420, 480, 520, 590, 640, 580, 470, 360, 220],
    timeSegments: {
      "Late Night (00:00 - 06:00)": 310,
      "Morning Flow (06:00 - 12:00)": 1440,
      "Afternoon Focus (12:00 - 18:00)": 2260,
      "Evening Prime (18:00 - 24:00)": 3280
    },
    peakSegment: "Evening Prime (18:00 - 24:00)",
    peakHour: 19,
    persona: "Late-Night & Evening Audiophile"
  });

  let canvasEl = $state(null);
  let hoveredHour = $state(null);
  let animId = null;

  const totalClockPlays = $derived(
    clockData.hourCounts.reduce((acc, v) => acc + v, 0) || 1
  );
  const maxHourPlays = $derived(Math.max(...clockData.hourCounts, 1));

  const nightPlays = $derived(clockData.timeSegments?.["Late Night (00:00 - 06:00)"] || 310);
  const morningPlays = $derived(clockData.timeSegments?.["Morning Flow (06:00 - 12:00)"] || 1440);
  const afternoonPlays = $derived(clockData.timeSegments?.["Afternoon Focus (12:00 - 18:00)"] || 2260);
  const eveningPlays = $derived(clockData.timeSegments?.["Evening Prime (18:00 - 24:00)"] || 3280);

  function getHourColor(hour) {
    if (hour >= 0 && hour < 6) return '#70695E'; // Late Night
    if (hour >= 6 && hour < 12) return '#C8934A'; // Morning Flow
    if (hour >= 12 && hour < 18) return '#EAE4D9'; // Afternoon Focus
    return '#E8443A'; // Evening Prime
  }

  function formatHour(h) {
    const period = h >= 12 ? 'PM' : 'AM';
    const displayH = h % 12 === 0 ? 12 : h % 12;
    return `${displayH} ${period}`;
  }

  function handleCanvasMouseMove(e) {
    if (!canvasEl) return;
    const rect = canvasEl.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    const angle = Math.atan2(y, x); // -PI to PI
    let normAngle = angle + Math.PI / 2;
    if (normAngle < 0) normAngle += Math.PI * 2;

    const hour = Math.floor((normAngle / (Math.PI * 2)) * 24) % 24;
    const dist = Math.hypot(x, y);

    if (dist >= 35 && dist <= 140) {
      hoveredHour = hour;
    } else {
      hoveredHour = null;
    }
  }

  function handleCanvasMouseLeave() {
    hoveredHour = null;
  }

  function renderClock() {
    if (!canvasEl) return;
    const ctx = canvasEl.getContext('2d');
    const dpr = typeof window !== 'undefined' ? (window.devicePixelRatio || 1) : 1;
    const logicalSize = 290;
    
    ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
    ctx.save();
    ctx.scale(dpr, dpr);

    const cx = logicalSize / 2;
    const cy = logicalSize / 2;

    const innerRadius = 46;
    const maxBarLength = 65;

    // Concentric Guide Rings
    for (let r of [innerRadius, innerRadius + 32, innerRadius + maxBarLength]) {
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(234, 228, 217, 0.08)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // 24 Hourly Spikes
    for (let h = 0; h < 24; h++) {
      const count = clockData.hourCounts[h] || 0;
      const barLen = Math.max(6, (count / maxHourPlays) * maxBarLength);
      const angle = (h / 24) * (Math.PI * 2) - Math.PI / 2;

      const isHovered = hoveredHour === h;
      const isPeak = clockData.peakHour === h;

      const x1 = cx + Math.cos(angle) * innerRadius;
      const y1 = cy + Math.sin(angle) * innerRadius;
      const x2 = cx + Math.cos(angle) * (innerRadius + barLen + (isHovered ? 6 : 0));
      const y2 = cy + Math.sin(angle) * (innerRadius + barLen + (isHovered ? 6 : 0));

      const color = getHourColor(h);

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = isHovered ? '#FFFFFF' : color;
      ctx.lineWidth = isHovered ? 4.5 : (isPeak ? 3.5 : 2.2);
      ctx.lineCap = 'round';
      if (isHovered || isPeak) {
        ctx.shadowBlur = 10;
        ctx.shadowColor = color;
      }
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Hour Marker Labels (0, 6, 12, 18)
      if (h % 6 === 0) {
        const lx = cx + Math.cos(angle) * (innerRadius + maxBarLength + 18);
        const ly = cy + Math.sin(angle) * (innerRadius + maxBarLength + 18);
        ctx.fillStyle = 'rgba(234, 228, 217, 0.45)';
        ctx.font = 'bold 9px "IBM Plex Mono", monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(h === 0 ? '12A' : (h === 6 ? '6A' : (h === 12 ? '12P' : '6P')), lx, ly);
      }
    }

    // Center Core Vinyl Disk
    ctx.beginPath();
    ctx.arc(cx, cy, innerRadius - 4, 0, Math.PI * 2);
    ctx.fillStyle = '#1A1713';
    ctx.fill();
    ctx.strokeStyle = 'rgba(234, 228, 217, 0.12)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Center Text
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    if (hoveredHour !== null) {
      ctx.fillStyle = '#EAE4D9';
      ctx.font = 'bold 13px "IBM Plex Mono", monospace';
      ctx.fillText(formatHour(hoveredHour), cx, cy - 7);
      ctx.fillStyle = getHourColor(hoveredHour);
      ctx.font = '600 10px "IBM Plex Mono", monospace';
      ctx.fillText(`${clockData.hourCounts[hoveredHour]} plays`, cx, cy + 9);
    } else {
      ctx.fillStyle = '#EAE4D9';
      ctx.font = 'italic 16px "Instrument Serif", serif';
      ctx.fillText('24H Clock', cx, cy - 6);
      ctx.fillStyle = '#C8934A';
      ctx.font = 'bold 9px "IBM Plex Mono", monospace';
      ctx.fillText(`Peak: ${formatHour(clockData.peakHour)}`, cx, cy + 9);
    }

    ctx.restore();

    if (portfolio.isClockModalOpen) {
      animId = requestAnimationFrame(renderClock);
    }
  }

  // Reactive Effect to handle canvas initialization whenever the modal opens
  $effect(() => {
    if (portfolio.isClockModalOpen && canvasEl) {
      const dpr = typeof window !== 'undefined' ? (window.devicePixelRatio || 1) : 1;
      canvasEl.width = 290 * dpr;
      canvasEl.height = 290 * dpr;
      if (animId) cancelAnimationFrame(animId);
      animId = requestAnimationFrame(renderClock);
    } else {
      if (animId) {
        cancelAnimationFrame(animId);
        animId = null;
      }
    }
  });

  onDestroy(() => {
    if (animId) cancelAnimationFrame(animId);
  });
</script>

{#if portfolio.isClockModalOpen}
  <div 
    class="clock-backdrop" 
    onclick={(e) => { if (e.target === e.currentTarget) portfolio.closeClock(); }}
    onkeydown={(e) => { if (e.key === 'Escape') portfolio.closeClock(); }}
    tabindex="0"
    role="dialog"
    aria-modal="true"
  >
    <div class="clock-modal-card surface-noise">
      
      <div class="clock-header">
        <div class="clock-title-wrap">
          <div class="clock-icon-box">
            <Clock size={16} />
          </div>
          <div>
            <h2>Circadian Listening Clock</h2>
            <span class="clock-sub">24-Hour activity rhythm inferred from Apple Music playback timestamps</span>
          </div>
        </div>

        <button type="button" class="btn-close-clock" onclick={() => portfolio.closeClock()} title="Close (Esc)">
          <X size={16} />
        </button>
      </div>

      <!-- Persona Banner -->
      <div class="persona-highlight-box">
        <div class="persona-left">
          <Sparkles size={14} class="persona-sparkle" />
          <div class="persona-text-wrap">
            <span class="persona-title">{clockData.persona}</span>
          </div>
        </div>
        <div class="persona-peak-pill">
          Peak Hour: <strong>{formatHour(clockData.peakHour)}</strong>
        </div>
      </div>

      <!-- Center Clock + Segments Grid -->
      <div class="clock-body-grid">
        
        <!-- Interactive Canvas Clock -->
        <div class="clock-canvas-wrap">
          <canvas 
            bind:this={canvasEl} 
            onmousemove={handleCanvasMouseMove}
            onmouseleave={handleCanvasMouseLeave}
            class="clock-canvas"
            style="width: 290px; height: 290px;"
          ></canvas>
          <span class="clock-hint">Hover over radial spikes to view hourly volume</span>
        </div>

        <!-- 4 Time-of-Day Segments Breakdown -->
        <div class="time-segments-column">
          <div class="segment-card night">
            <div class="segment-card-top">
              <div class="segment-icon-row">
                <Moon size={14} />
                <span>Late Night (00:00 – 06:00)</span>
              </div>
              <div class="segment-plays">{nightPlays.toLocaleString()} plays</div>
            </div>
            <div class="segment-bar-track">
              <div class="segment-bar-fill" style="width: {Math.round((nightPlays / totalClockPlays) * 100)}%; background: #70695E;"></div>
            </div>
          </div>

          <div class="segment-card morning">
            <div class="segment-card-top">
              <div class="segment-icon-row">
                <Sunrise size={14} />
                <span>Morning Flow (06:00 – 12:00)</span>
              </div>
              <div class="segment-plays">{morningPlays.toLocaleString()} plays</div>
            </div>
            <div class="segment-bar-track">
              <div class="segment-bar-fill" style="width: {Math.round((morningPlays / totalClockPlays) * 100)}%; background: #C8934A;"></div>
            </div>
          </div>

          <div class="segment-card afternoon">
            <div class="segment-card-top">
              <div class="segment-icon-row">
                <Sun size={14} />
                <span>Afternoon Focus (12:00 – 18:00)</span>
              </div>
              <div class="segment-plays">{afternoonPlays.toLocaleString()} plays</div>
            </div>
            <div class="segment-bar-track">
              <div class="segment-bar-fill" style="width: {Math.round((afternoonPlays / totalClockPlays) * 100)}%; background: #EAE4D9;"></div>
            </div>
          </div>

          <div class="segment-card evening active">
            <div class="segment-card-top">
              <div class="segment-icon-row">
                <Sunset size={14} />
                <span>Evening Prime (18:00 – 24:00)</span>
                <span class="peak-tag">PEAK</span>
              </div>
              <div class="segment-plays">{eveningPlays.toLocaleString()} plays</div>
            </div>
            <div class="segment-bar-track">
              <div class="segment-bar-fill" style="width: {Math.round((eveningPlays / totalClockPlays) * 100)}%; background: #E8443A;"></div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
{/if}

<style>
  .clock-backdrop {
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

  .clock-modal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    width: 100%;
    max-width: 720px;
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

  .clock-header {
    display: flex; align-items: center; justify-content: space-between;
  }
  .clock-title-wrap {
    display: flex; align-items: center; gap: 12px;
  }
  .clock-icon-box {
    width: 32px; height: 32px; border-radius: 2px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--oxide); display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .clock-title-wrap h2 {
    font-family: var(--font-serif); font-size: 1.55rem; font-weight: 400;
    font-style: italic; color: var(--linen); letter-spacing: 0.01em; line-height: 1.15;
  }
  .clock-sub {
    font-family: var(--font-mono);
    font-size: 0.68rem; color: var(--text-muted); display: block; margin-top: 2px;
    letter-spacing: 0.02em;
  }

  .btn-close-clock {
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-muted); width: 28px; height: 28px;
    border-radius: 2px; display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.15s ease;
  }
  .btn-close-clock:hover {
    color: var(--linen); border-color: var(--oxide);
  }

  .persona-highlight-box {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 12px 16px;
    gap: 12px;
  }
  .persona-left {
    display: flex; align-items: center; gap: 8px;
  }
  :global(.persona-sparkle) { color: var(--oxide); flex-shrink: 0; }
  .persona-text-wrap {
    display: flex; flex-direction: column;
  }
  .persona-title {
    font-family: var(--font-serif); font-size: 1.2rem; font-style: italic; font-weight: 400;
    color: var(--linen); letter-spacing: 0.01em;
  }
  .persona-peak-pill {
    font-family: var(--font-mono);
    font-size: 0.72rem; color: var(--text-secondary);
    background: var(--surface); padding: 4px 10px; border-radius: 2px;
    border: 1px solid var(--border);
    white-space: nowrap;
  }
  .persona-peak-pill strong { color: var(--oxide); }

  .clock-body-grid {
    display: grid; grid-template-columns: 290px 1fr;
    gap: 24px; align-items: center;
  }

  .clock-canvas-wrap {
    display: flex; flex-direction: column; align-items: center;
  }
  .clock-canvas {
    width: 290px; height: 290px; cursor: crosshair;
  }
  .clock-hint {
    font-family: var(--font-mono);
    font-size: 0.62rem; color: var(--text-muted); margin-top: 6px;
    letter-spacing: 0.02em;
    text-align: center;
  }

  .time-segments-column {
    display: flex; flex-direction: column; gap: 10px;
  }

  .segment-card {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 10px 14px;
    display: flex; flex-direction: column; gap: 8px;
    transition: all 0.15s ease;
  }
  .segment-card:hover {
    border-color: var(--border-hover); background: var(--surface-3);
  }
  .segment-card.active {
    border-color: var(--signal);
  }
  .segment-card.night { border-left: 3px solid var(--groove-light); }
  .segment-card.morning { border-left: 3px solid var(--oxide); }
  .segment-card.afternoon { border-left: 3px solid var(--linen-muted); }
  .segment-card.evening { border-left: 3px solid var(--signal); }

  .segment-card-top {
    display: flex; align-items: center; justify-content: space-between;
    gap: 8px;
  }

  .segment-icon-row {
    display: flex; align-items: center; gap: 8px;
    font-family: var(--font-mono);
    font-size: 0.72rem; font-weight: 600; color: var(--linen);
    letter-spacing: 0.01em;
  }
  .segment-plays {
    font-family: var(--font-mono); font-size: 0.76rem; font-weight: 600;
    color: var(--text-secondary); font-variant-numeric: tabular-nums lining-nums;
    letter-spacing: 0.02em;
    white-space: nowrap;
  }
  .peak-tag {
    font-family: var(--font-mono);
    font-size: 0.54rem; font-weight: 700; letter-spacing: 0.06em;
    background: var(--signal); color: #fff; padding: 1px 5px; border-radius: 2px;
  }

  .segment-bar-track {
    width: 100%; height: 3px;
    background: var(--groove);
    border-radius: 1px;
    overflow: hidden;
  }
  .segment-bar-fill {
    height: 100%;
    border-radius: 1px;
    transition: width 0.3s ease;
  }

  @media (max-width: 700px) {
    .clock-body-grid { grid-template-columns: 1fr; }
    .clock-canvas-wrap { margin: 0 auto; }
  }
</style>

