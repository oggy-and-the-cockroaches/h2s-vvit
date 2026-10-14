/**
 * CivicPulse AI Operations Platform - Resolution Verification Forensic Controls
 *
 * Implements:
 * - Accessible before/after comparison slider with mouse, touch, and keyboard (ArrowLeft/ArrowRight) controls
 * - Photogrammetric LiDAR metric grid and depth heatmap overlay toggles
 * - Synchronized pan-and-zoom inspection with zoom reset
 * - Officer sign-off decision action deck with accessible status announcements
 */

document.addEventListener('DOMContentLoaded', () => {
  const sliderContainer = document.getElementById('sliderComparisonContainer');
  const splitContainer = document.getElementById('splitComparisonContainer');
  const viewSliderBtn = document.getElementById('viewSliderBtn');
  const viewSplitBtn = document.getElementById('viewSplitBtn');

  // 1. Toggle Split vs Slider Mode
  if (viewSliderBtn && viewSplitBtn && sliderContainer && splitContainer) {
    viewSliderBtn.addEventListener('click', () => {
      splitContainer.classList.add('hidden');
      sliderContainer.classList.remove('hidden');
      viewSliderBtn.className = "flex items-center gap-1.5 px-space-sm py-1.5 rounded bg-primary text-on-primary font-telemetry-meta text-telemetry-meta font-bold transition-all shadow-sm";
      viewSplitBtn.className = "flex items-center gap-1.5 px-space-sm py-1.5 rounded text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high font-telemetry-meta text-telemetry-meta transition-all";
      viewSliderBtn.setAttribute('aria-pressed', 'true');
      viewSplitBtn.setAttribute('aria-pressed', 'false');
    });

    viewSplitBtn.addEventListener('click', () => {
      sliderContainer.classList.add('hidden');
      splitContainer.classList.remove('hidden');
      viewSplitBtn.className = "flex items-center gap-1.5 px-space-sm py-1.5 rounded bg-primary text-on-primary font-telemetry-meta text-telemetry-meta font-bold transition-all shadow-sm";
      viewSliderBtn.className = "flex items-center gap-1.5 px-space-sm py-1.5 rounded text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high font-telemetry-meta text-telemetry-meta transition-all";
      viewSplitBtn.setAttribute('aria-pressed', 'true');
      viewSliderBtn.setAttribute('aria-pressed', 'false');
    });
  }

  // 2. Interactive Slider Dragging & Full Keyboard Accessibility (WCAG 2.1 AA)
  const handle = document.getElementById('sliderHandle');
  const clipLayer = document.getElementById('sliderClipLayer');
  let isDragging = false;
  let currentPercent = 50;

  const setSliderPosition = (percent) => {
    currentPercent = Math.max(2, Math.min(98, percent));
    if (handle) {
      handle.style.left = currentPercent + '%';
      handle.setAttribute('aria-valuenow', Math.round(currentPercent).toString());
    }
    if (clipLayer) {
      clipLayer.style.width = currentPercent + '%';
    }
  };

  if (handle && sliderContainer && clipLayer) {
    // Configure ARIA slider semantics for screen reader & keyboard navigation
    handle.setAttribute('role', 'slider');
    handle.setAttribute('tabindex', '0');
    handle.setAttribute('aria-label', 'Comparison before and after slider');
    handle.setAttribute('aria-valuemin', '0');
    handle.setAttribute('aria-valuemax', '100');
    handle.setAttribute('aria-valuenow', '50');

    // Keyboard support: Arrow keys adjust position by 5%
    handle.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
        e.preventDefault();
        setSliderPosition(currentPercent - 5);
      } else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
        e.preventDefault();
        setSliderPosition(currentPercent + 5);
      } else if (e.key === 'Home') {
        e.preventDefault();
        setSliderPosition(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        setSliderPosition(100);
      }
    });

    const onMove = (e) => {
      if (!isDragging) return;
      const rect = sliderContainer.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const percent = ((clientX - rect.left) / rect.width) * 100;
      setSliderPosition(percent);
    };

    const stopDrag = () => { isDragging = false; };

    handle.addEventListener('mousedown', () => { isDragging = true; });
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', stopDrag);

    handle.addEventListener('touchstart', () => { isDragging = true; }, { passive: true });
    window.addEventListener('touchmove', onMove, { passive: true });
    window.addEventListener('touchend', stopDrag);
  }

  // 3. Grid Overlay Toggle
  const toggleGridBtn = document.getElementById('toggleGridBtn');
  const gridLeft = document.getElementById('metricGridLeft');
  const gridRight = document.getElementById('metricGridRight');
  let gridVisible = true;

  if (toggleGridBtn && gridLeft && gridRight) {
    toggleGridBtn.setAttribute('aria-pressed', 'true');
    toggleGridBtn.addEventListener('click', () => {
      gridVisible = !gridVisible;
      gridLeft.style.display = gridVisible ? 'block' : 'none';
      gridRight.style.display = gridVisible ? 'block' : 'none';
      toggleGridBtn.classList.toggle('text-primary');
      toggleGridBtn.setAttribute('aria-pressed', gridVisible.toString());
      if (window.CivicToast) {
        window.CivicToast.show('LiDAR Metric Grid', gridVisible ? 'Photogrammetry overlay enabled' : 'Overlay hidden', 'grid_4x4', 'secondary');
      }
    });
  }

  // 4. Depth Gauge Heatmap Toggle
  const toggleDepthBtn = document.getElementById('toggleDepthBtn');
  const depthLeft = document.getElementById('depthHeatmapLeft');
  const depthRight = document.getElementById('depthHeatmapRight');
  let depthVisible = true;

  if (toggleDepthBtn && depthLeft && depthRight) {
    toggleDepthBtn.setAttribute('aria-pressed', 'true');
    toggleDepthBtn.addEventListener('click', () => {
      depthVisible = !depthVisible;
      depthLeft.style.display = depthVisible ? 'flex' : 'none';
      depthRight.style.display = depthVisible ? 'flex' : 'none';
      toggleDepthBtn.classList.toggle('text-tertiary');
      toggleDepthBtn.setAttribute('aria-pressed', depthVisible.toString());
      if (window.CivicToast) {
        window.CivicToast.show('Subsurface Heatmap', depthVisible ? 'Depression depth contour enabled' : 'Depression contour hidden', 'layers', 'tertiary');
      }
    });
  }

  // 5. Synchronized Pan-and-Zoom simulation
  const beforeImg = document.getElementById('beforeImg');
  const afterImg = document.getElementById('afterImg');
  const zoomResetBtn = document.getElementById('zoomResetBtn');
  const zoomLevelDisplay = document.getElementById('zoomLevelDisplay');
  let zoomLevel = 1.0;

  const applyZoom = (scale) => {
    zoomLevel = scale;
    if (beforeImg) beforeImg.style.transform = `scale(${zoomLevel})`;
    if (afterImg) afterImg.style.transform = `scale(${zoomLevel})`;
    if (zoomLevelDisplay) zoomLevelDisplay.innerText = Math.round(zoomLevel * 100) + '%';
  };

  if (beforeImg && afterImg) {
    [beforeImg, afterImg].forEach(img => {
      img.parentElement.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 0.15 : -0.15;
        const newZoom = Math.min(Math.max(1.0, zoomLevel + delta), 2.5);
        applyZoom(newZoom);
      }, { passive: false });
    });
  }

  if (zoomResetBtn) {
    zoomResetBtn.addEventListener('click', () => {
      applyZoom(1.0);
    });
  }

  // 6. Officer Decision Sign-off Actions
  const feedbackBanner = document.getElementById('feedbackBanner');
  const feedbackTitle = document.getElementById('feedbackTitle');
  const feedbackDesc = document.getElementById('feedbackDesc');
  const feedbackIcon = document.getElementById('feedbackIcon');
  const closeFeedbackBtn = document.getElementById('closeFeedbackBtn');

  const showBanner = (title, desc, iconName, iconColorClass) => {
    if (!feedbackBanner) return;
    feedbackTitle.innerText = title;
    feedbackDesc.innerText = desc;
    feedbackIcon.innerText = iconName;
    feedbackIcon.className = `material-symbols-outlined text-[24px] shrink-0 ${iconColorClass}`;
    feedbackBanner.classList.remove('hidden');
    feedbackBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  if (closeFeedbackBtn) {
    closeFeedbackBtn.addEventListener('click', () => {
      feedbackBanner.classList.add('hidden');
    });
  }

  const btnApprove = document.getElementById('btnApprove');
  const btnRequestProof = document.getElementById('btnRequestProof');
  const btnScheduleInspect = document.getElementById('btnScheduleInspect');
  const btnReject = document.getElementById('btnReject');

  if (btnApprove) {
    btnApprove.addEventListener('click', () => {
      showBanner(
        'Resolution Approved & Cryptographically Signed',
        'Signed by Dir. E. Vance. Merkle block #90429 committed to immutable civic ledger. Contractor invoice unlocked.',
        'verified',
        'text-tertiary'
      );
      if (window.CivicToast) {
        window.CivicToast.show('Resolution Approved', 'Incident #CP-8461 marked verified & closed.', 'verified', 'tertiary');
      }
    });
  }

  if (btnRequestProof) {
    btnRequestProof.addEventListener('click', () => {
      showBanner(
        'Transverse Evidence Request Dispatched',
        'Lead M. Henderson notified. Transverse angle photogrammetry requested within 2 hours.',
        'add_a_photo',
        'text-primary'
      );
      if (window.CivicToast) {
        window.CivicToast.show('Evidence Requested', 'Crew Lead notified for additional photos.', 'add_a_photo', 'primary');
      }
    });
  }

  if (btnScheduleInspect) {
    btnScheduleInspect.addEventListener('click', () => {
      showBanner(
        '14-Day Post-Repair Audit Scheduled',
        'Autonomous mobile LiDAR inspection drone route logged for 14 calendar days from completion.',
        'event_repeat',
        'text-secondary'
      );
      if (window.CivicToast) {
        window.CivicToast.show('Audit Scheduled', 'Post-repair LiDAR scan slated for Day 14.', 'event_repeat', 'secondary');
      }
    });
  }

  if (btnReject) {
    btnReject.addEventListener('click', () => {
      showBanner(
        'Repair Non-Conformance Notice Issued',
        'Work order reissued to Public Works Unit 02. SLA counter reset with mandatory 24h remediation target.',
        'cancel',
        'text-error'
      );
      if (window.CivicToast) {
        window.CivicToast.show('Repair Rejected', 'Non-conformance filed with Public Works.', 'cancel', 'error');
      }
    });
  }
});
