/**
 * CivicPulse AI Operations Platform - 3-Minute Executive Judge Demo Tour
 *
 * Designed specifically for hackathon judges & academic evaluators:
 * - 5-stage automated/manual guided walkthrough across all platform capabilities
 * - Cross-page navigation via URL state persistence (?tour=1..5)
 * - Spotlight glow highlighting active architectural modules
 * - Keyboard shortcuts (Alt + J to trigger, ArrowRight/ArrowLeft to navigate, ESC to exit)
 * - Auto-play progress bar with pause/resume controls
 */

(function () {
  'use strict';

  const TOUR_STEPS = [
    {
      page: 'index.html',
      title: 'Real-Time Telemetry & Autonomous AI Triage',
      badge: 'STAGE 1 OF 5 • INGESTION & TRIAGE',
      targetSelector: '#triageSectionHeader',
      fallbackSelector: 'main',
      description: 'Ingests multi-source municipal sensor feeds and crowdsourced citizen reports in real-time. Features automated spatial deduplication, urgency SLA countdowns, and composite AI priority ranking (1–100).',
      highlights: [
        'Live Incident Cockpit: Real-time hazard counters & SLA timers',
        'Composite AI Priority Scoring: Safety (40%), Community (25%), Wait Duration (15%), Corroboration (20%)',
        'One-Click Autonomous Dispatch Recommendations'
      ],
      nextLabel: 'Explore Tactical GIS Map ➔'
    },
    {
      page: 'index.html',
      title: 'Geospatial Tactical Command & Fleet Tracking',
      badge: 'STAGE 2 OF 5 • GEOSPATIAL FLEET DISPATCH',
      targetSelector: '#tacticalMapContainer',
      fallbackSelector: '#triageSectionHeader',
      description: 'Interactive high-density vector map of District 04. Overlays active hazard clusters, proximity blast radii, and live emergency utility squad trajectories with real-time GPS pings.',
      highlights: [
        'Live Unit Tracking: Emergency Utility Squad #04 en route (4 min ETA)',
        'Spatio-Temporal Clustering: Merges corroborating citizen pings into unified records',
        'Multi-hazard Layer Overlays: Electrical, Roadway, Hydro, and Environmental'
      ],
      nextLabel: 'View Incident Intelligence Dossier ➔'
    },
    {
      page: 'incident-intelligence.html',
      title: 'Multimodal Forensics & AI Explainability Matrix',
      badge: 'STAGE 3 OF 5 • MULTIMODAL FORENSICS',
      targetSelector: '#forensicViewportContainer',
      fallbackSelector: 'main',
      description: 'Deep investigative dossier for Incident #CP-8492. Integrates sub-pixel camera photogrammetry, thermal HUD targeting, camera EXIF GNSS geoverification, and mathematical explainability breakdown.',
      highlights: [
        'Live 480V Arcing Conductor Detection: Automated bounding box HUD overlay',
        'Camera EXIF GNSS Verification: Eliminates false reports and spoofed coordinates',
        'Field Procedure Checklist: Tracks live isolation and street-level safety perimeter actions'
      ],
      nextLabel: 'Inspect Resolution Verification ➔'
    },
    {
      page: 'resolution-verification.html',
      title: 'Dual Photogrammetry & LiDAR Elevation Heatmap',
      badge: 'STAGE 4 OF 5 • STATUTORY AUDIT & SIGN-OFF',
      targetSelector: '#sliderComparisonContainer',
      fallbackSelector: 'main',
      description: 'Statutory verification workspace for completed public repairs. Compare before and after captures using the interactive slider, inspect subsurface elevation heatmaps, and execute immutable officer decisions.',
      highlights: [
        'Interactive Comparison Slider: Mouse, touch, and keyboard accessible',
        'Metric LiDAR Elevation Grid: Restores flush surface grade over culvert frames',
        'Officer Action Deck: Signs off completion and cryptographically unlocks contractor payout'
      ],
      nextLabel: 'Verify Civic Transparency & Ledger ➔'
    },
    {
      page: 'public-transparency.html',
      title: 'Civic Trust Portal & Open Cryptographic Datasets',
      badge: 'STAGE 5 OF 5 • OPEN GOVERNANCE & LEDGER',
      targetSelector: '#transparencyMetricsGrid',
      fallbackSelector: 'main',
      description: 'Public civic accountability portal delivering citizen trust metrics, live resolution stream with photographic proof, Merkle-linked audit blocks, and machine-readable open datasets.',
      highlights: [
        'Cryptographic Merkle Proofs: Block consensus synced across 12 validator nodes',
        '30-Day Resolution Velocity: Municipal SLA performance tracking curves',
        'Open Civic Data APIs: Instant export to GeoJSON (RFC 7946) and CSV ledger'
      ],
      nextLabel: 'Complete Tour & Return to Command 🏁'
    }
  ];

  let currentStepIndex = 0;
  let tourModal = null;
  let activeHighlightEl = null;
  let autoPlayTimer = null;
  let autoPlaySeconds = 30;
  let autoPlayRemaining = 30;
  let isAutoPlayPaused = false;

  /**
   * Helper to detect current page basename
   */
  function getCurrentPageName() {
    const path = window.location.pathname;
    return path.substring(path.lastIndexOf('/') + 1) || 'index.html';
  }

  /**
   * Create or retrieve Tour Modal DOM element
   */
  function getOrCreateTourModal() {
    if (tourModal) return tourModal;

    tourModal = document.createElement('div');
    tourModal.id = 'executiveTourModal';
    tourModal.setAttribute('role', 'dialog');
    tourModal.setAttribute('aria-modal', 'true');
    tourModal.setAttribute('aria-label', '3-Minute Executive Judge Demo Tour');
    tourModal.className = 'fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] w-[95%] max-w-2xl bg-surface-container-lowest/95 backdrop-blur-xl border-2 border-primary/60 rounded-2xl shadow-[0_10px_40px_rgba(0,0,0,0.8)] p-5 text-on-surface transition-all transform duration-300';

    tourModal.innerHTML = `
      <div class="flex items-center justify-between pb-3 border-b border-surface-container-high/60 gap-3">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-primary animate-ping" aria-hidden="true"></span>
          <span id="tourBadge" class="font-label-caps text-[11px] text-primary tracking-widest uppercase font-bold"></span>
        </div>
        <div class="flex items-center gap-2">
          <button id="tourAutoPlayToggle" class="px-2 py-0.5 rounded text-[11px] font-mono bg-surface-container-high hover:bg-surface-bright text-on-surface-variant flex items-center gap-1 transition-colors" title="Toggle Auto-Advance">
            <span class="material-symbols-outlined text-[14px]">pause</span>
            <span id="tourTimerLabel">30s</span>
          </button>
          <button id="tourCloseBtn" class="p-1 rounded text-outline hover:text-on-surface hover:bg-surface-container-high transition-colors" aria-label="Exit Demo Tour">
            <span class="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>
      </div>

      <!-- Auto Play Progress Bar -->
      <div class="w-full bg-surface-container-highest h-1 rounded-full mt-2 overflow-hidden">
        <div id="tourProgressBar" class="bg-gradient-to-r from-primary via-tertiary to-primary h-full transition-all duration-1000" style="width: 100%;"></div>
      </div>

      <div class="py-3">
        <h3 id="tourTitle" class="font-headline-sm text-base sm:text-lg font-bold text-on-surface text-primary mb-1"></h3>
        <p id="tourDescription" class="font-body-sm text-xs sm:text-sm text-on-surface-variant mb-3 leading-relaxed"></p>
        <ul id="tourHighlights" class="space-y-1.5 bg-surface-container/60 p-3 rounded-lg border border-surface-container-high/40 text-xs sm:text-sm font-medium"></ul>
      </div>

      <div class="flex items-center justify-between pt-3 border-t border-surface-container-high/60 gap-3">
        <button id="tourPrevBtn" class="px-3 py-1.5 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-semibold flex items-center gap-1 transition-all disabled:opacity-40 disabled:cursor-not-allowed">
          <span class="material-symbols-outlined text-[16px]">arrow_back</span>
          <span>Previous</span>
        </button>

        <div class="flex items-center gap-1.5" id="tourStepIndicators"></div>

        <button id="tourNextBtn" class="px-4 py-1.5 rounded-lg bg-primary hover:bg-primary-fixed text-on-primary text-xs sm:text-sm font-bold flex items-center gap-1.5 transition-all shadow-md active:scale-95">
          <span id="tourNextLabel">Next Step</span>
          <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
        </button>
      </div>
    `;

    document.body.appendChild(tourModal);

    // Wire controls
    document.getElementById('tourCloseBtn').addEventListener('click', stopTour);
    document.getElementById('tourPrevBtn').addEventListener('click', () => navigateStep(currentStepIndex - 1));
    document.getElementById('tourNextBtn').addEventListener('click', () => {
      if (currentStepIndex >= TOUR_STEPS.length - 1) {
        completeTour();
      } else {
        navigateStep(currentStepIndex + 1);
      }
    });

    const autoToggle = document.getElementById('tourAutoPlayToggle');
    autoToggle.addEventListener('click', () => {
      isAutoPlayPaused = !isAutoPlayPaused;
      autoToggle.querySelector('.material-symbols-outlined').textContent = isAutoPlayPaused ? 'play_arrow' : 'pause';
      autoToggle.classList.toggle('text-primary', !isAutoPlayPaused);
    });

    return tourModal;
  }

  /**
   * Apply glowing spotlight outline around target architectural component
   */
  function highlightComponent(selector, fallback) {
    if (activeHighlightEl) {
      activeHighlightEl.classList.remove('ring-4', 'ring-primary', 'ring-offset-4', 'ring-offset-surface', 'shadow-[0_0_30px_rgba(76,215,246,0.6)]');
    }

    let target = document.querySelector(selector) || document.querySelector(fallback);
    if (target) {
      target.classList.add('ring-4', 'ring-primary', 'ring-offset-4', 'ring-offset-surface', 'shadow-[0_0_30px_rgba(76,215,246,0.6)]', 'transition-all', 'duration-500');
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      activeHighlightEl = target;
    }
  }

  /**
   * Render active step content
   */
  function renderActiveStep() {
    const step = TOUR_STEPS[currentStepIndex];
    const modal = getOrCreateTourModal();

    modal.classList.remove('hidden');

    document.getElementById('tourBadge').textContent = step.badge;
    document.getElementById('tourTitle').textContent = step.title;
    document.getElementById('tourDescription').textContent = step.description;

    const list = document.getElementById('tourHighlights');
    list.innerHTML = step.highlights.map(h => `
      <li class="flex items-start gap-2 text-on-surface">
        <span class="material-symbols-outlined text-primary text-[16px] shrink-0 mt-0.5">check_circle</span>
        <span>${h}</span>
      </li>
    `).join('');

    document.getElementById('tourNextLabel').textContent = step.nextLabel;
    document.getElementById('tourPrevBtn').disabled = currentStepIndex === 0;

    // Render dot indicators
    const dotsContainer = document.getElementById('tourStepIndicators');
    dotsContainer.innerHTML = TOUR_STEPS.map((s, idx) => `
      <button class="w-2.5 h-2.5 rounded-full transition-all ${idx === currentStepIndex ? 'bg-primary w-6' : 'bg-surface-container-highest hover:bg-outline'}" 
              title="Jump to Stage ${idx + 1}" data-step="${idx}" aria-label="Go to stage ${idx + 1}"></button>
    `).join('');

    dotsContainer.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const targetIdx = parseInt(btn.getAttribute('data-step'), 10);
        navigateStep(targetIdx);
      });
    });

    highlightComponent(step.targetSelector, step.fallbackSelector);
    startTimerCountdown();
  }

  /**
   * Auto-advance countdown timer
   */
  function startTimerCountdown() {
    clearInterval(autoPlayTimer);
    autoPlayRemaining = autoPlaySeconds;
    const bar = document.getElementById('tourProgressBar');
    const label = document.getElementById('tourTimerLabel');

    autoPlayTimer = setInterval(() => {
      if (isAutoPlayPaused) return;

      autoPlayRemaining -= 1;
      if (label) label.textContent = `${autoPlayRemaining}s`;
      if (bar) bar.style.width = `${(autoPlayRemaining / autoPlaySeconds) * 100}%`;

      if (autoPlayRemaining <= 0) {
        clearInterval(autoPlayTimer);
        if (currentStepIndex < TOUR_STEPS.length - 1) {
          navigateStep(currentStepIndex + 1);
        } else {
          completeTour();
        }
      }
    }, 1000);
  }

  /**
   * Navigate to a step (handles same page or cross-page transition)
   */
  function navigateStep(targetIndex) {
    if (targetIndex < 0 || targetIndex >= TOUR_STEPS.length) return;

    const targetStep = TOUR_STEPS[targetIndex];
    const currentPage = getCurrentPageName();

    currentStepIndex = targetIndex;
    sessionStorage.setItem('civicpulse_tour_active', 'true');
    sessionStorage.setItem('civicpulse_tour_step', targetIndex.toString());

    if (currentPage !== targetStep.page) {
      window.location.href = `${targetStep.page}?tour=${targetIndex}`;
    } else {
      renderActiveStep();
    }
  }

  /**
   * Stop tour and clean up state
   */
  function stopTour() {
    clearInterval(autoPlayTimer);
    sessionStorage.removeItem('civicpulse_tour_active');
    sessionStorage.removeItem('civicpulse_tour_step');
    if (tourModal) tourModal.classList.add('hidden');
    if (activeHighlightEl) {
      activeHighlightEl.classList.remove('ring-4', 'ring-primary', 'ring-offset-4', 'ring-offset-surface', 'shadow-[0_0_30px_rgba(76,215,246,0.6)]');
    }
    if (window.CivicToast) {
      window.CivicToast.show('Demo Tour Concluded', 'Feel free to explore live views anytime or restart via header button.', 'info', 'primary');
    }
  }

  /**
   * Complete final stage
   */
  function completeTour() {
    stopTour();
    if (window.CivicToast) {
      window.CivicToast.show('Executive Tour Complete 🏆', 'All 5 municipal operations modules verified.', 'verified', 'tertiary');
    }
    // Return to main command center
    setTimeout(() => {
      if (getCurrentPageName() !== 'index.html') {
        window.location.href = 'index.html';
      }
    }, 1200);
  }

  /**
   * Start or resume tour
   */
  function startTour(initialIndex = 0) {
    currentStepIndex = initialIndex;
    const step = TOUR_STEPS[currentStepIndex];
    const currentPage = getCurrentPageName();

    sessionStorage.setItem('civicpulse_tour_active', 'true');
    sessionStorage.setItem('civicpulse_tour_step', currentStepIndex.toString());

    if (currentPage !== step.page) {
      window.location.href = `${step.page}?tour=${currentStepIndex}`;
    } else {
      renderActiveStep();
    }
  }

  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', () => {
    // 1. Wire all "Judge Demo Tour" buttons across headers
    document.querySelectorAll('.btn-judge-tour').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        startTour(0);
      });
    });

    // 2. Global shortcut Alt + J or Ctrl + Shift + J
    window.addEventListener('keydown', (e) => {
      if ((e.altKey && (e.key === 'j' || e.key === 'J')) || (e.ctrlKey && e.shiftKey && (e.key === 'j' || e.key === 'J'))) {
        e.preventDefault();
        startTour(0);
      }
      if (e.key === 'Escape' && tourModal && !tourModal.classList.contains('hidden')) {
        stopTour();
      }
      if (tourModal && !tourModal.classList.contains('hidden')) {
        if (e.key === 'ArrowRight') navigateStep(currentStepIndex + 1);
        if (e.key === 'ArrowLeft') navigateStep(currentStepIndex - 1);
      }
    });

    // 3. Resume tour if active in session or query param
    const urlParams = new URLSearchParams(window.location.search);
    const tourParam = urlParams.get('tour');
    const isSessionActive = sessionStorage.getItem('civicpulse_tour_active') === 'true';

    if (tourParam !== null) {
      const stepIdx = parseInt(tourParam, 10);
      if (!isNaN(stepIdx) && stepIdx >= 0 && stepIdx < TOUR_STEPS.length) {
        startTour(stepIdx);
      }
    } else if (isSessionActive) {
      const stepIdx = parseInt(sessionStorage.getItem('civicpulse_tour_step') || '0', 10);
      if (!isNaN(stepIdx) && stepIdx >= 0 && stepIdx < TOUR_STEPS.length) {
        renderActiveStep();
      }
    }
  });

  // Expose global controller
  window.CivicPulseTour = {
    start: startTour,
    stop: stopTour,
    next: () => navigateStep(currentStepIndex + 1),
    prev: () => navigateStep(currentStepIndex - 1)
  };

})();
