/**
 * CivicPulse AI Operations Platform - Core Application Logic & Router Interactivity
 */

(function () {
  'use strict';

  // 1. Highlight Active Nav Item Based on Current Page
  function updateActiveNav() {
    const currentPath = window.location.pathname;
    const pageName = currentPath.substring(currentPath.lastIndexOf('/') + 1) || 'index.html';

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach((link) => {
      const href = link.getAttribute('href');
      const dataPage = link.getAttribute('data-page');

      // Check if matches pageName
      const isMatch = (href && href.startsWith(pageName)) ||
                      (pageName === '' && href === 'index.html') ||
                      (pageName === 'index.html' && dataPage === 'index') ||
                      (pageName.includes('incident') && dataPage === 'incident-intelligence') ||
                      (pageName.includes('resolution') && dataPage === 'resolution-verification') ||
                      (pageName.includes('transparency') && (dataPage === 'citizen-portal' || dataPage === 'transparency-and-impact'));

      if (isMatch && dataPage !== 'live-incidents' && dataPage !== 'impact-replay') {
        link.classList.add('bg-primary-container', 'text-on-primary-container', 'font-semibold');
        link.classList.remove('text-on-surface-variant');
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  // 2. Telemetry Sync Clock Simulation
  function startTelemetryTimer() {
    const syncElements = document.querySelectorAll('.telemetry-sync-time');
    let seconds = 12;

    setInterval(() => {
      seconds = (seconds + 1) % 45;
      syncElements.forEach(el => {
        el.textContent = `SYNC: ${seconds}s AGO`;
      });
    }, 1000);
  }

  // 3. Global Command Palette (⌘K / Ctrl+K)
  function initCommandPalette() {
    let paletteModal = document.getElementById('commandPaletteModal');
    if (!paletteModal) {
      paletteModal = document.createElement('div');
      paletteModal.id = 'commandPaletteModal';
      paletteModal.className = 'fixed inset-0 z-50 hidden flex items-start justify-center pt-24 px-4 bg-black/70 modal-backdrop';
      paletteModal.innerHTML = `
        <div class="w-full max-w-xl bg-surface-container-low border border-surface-container-high rounded-xl shadow-2xl overflow-hidden transition-all">
          <div class="flex items-center px-4 py-3 border-b border-surface-container-high">
            <span class="material-symbols-outlined text-primary text-[22px] mr-3">search</span>
            <input id="commandPaletteInput" type="text" placeholder="Search commands, pages, incident IDs (e.g. CP-8492)..." 
                   class="w-full bg-transparent text-on-surface placeholder:text-outline font-body-md focus:outline-none text-sm" />
            <span class="text-xs font-mono text-outline px-1.5 py-0.5 bg-surface-container rounded border border-surface-container-highest">ESC</span>
          </div>
          <div class="p-2 max-h-80 overflow-y-auto space-y-1" id="commandPaletteResults">
            <a href="index.html" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-on-surface hover:bg-surface-container transition-colors group">
              <span class="material-symbols-outlined text-primary text-[20px]">dashboard</span>
              <div class="flex-1">
                <div class="font-medium group-hover:text-primary">Command Center Overview</div>
                <div class="text-xs text-outline">Real-time municipal incident detection & triage dispatch</div>
              </div>
              <span class="text-[10px] font-mono text-outline bg-surface-container px-2 py-0.5 rounded">Alt + 1</span>
            </a>
            <a href="incident-intelligence.html" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-on-surface hover:bg-surface-container transition-colors group">
              <span class="material-symbols-outlined text-error text-[20px]">psychology</span>
              <div class="flex-1">
                <div class="font-medium group-hover:text-primary">Incident Intelligence Dossier (#CP-8492)</div>
                <div class="text-xs text-outline">Tier 1 Critical: Exposed High-Voltage Utility Cable</div>
              </div>
              <span class="text-[10px] font-mono text-outline bg-surface-container px-2 py-0.5 rounded">Alt + 2</span>
            </a>
            <a href="resolution-verification.html" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-on-surface hover:bg-surface-container transition-colors group">
              <span class="material-symbols-outlined text-tertiary text-[20px]">verified</span>
              <div class="flex-1">
                <div class="font-medium group-hover:text-primary">Resolution Verification Workspace (#CP-8461)</div>
                <div class="text-xs text-outline">Dual forensic audit, LiDAR alignment & before/after inspection</div>
              </div>
              <span class="text-[10px] font-mono text-outline bg-surface-container px-2 py-0.5 rounded">Alt + 3</span>
            </a>
            <a href="public-transparency.html" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-on-surface hover:bg-surface-container transition-colors group">
              <span class="material-symbols-outlined text-secondary text-[20px]">policy</span>
              <div class="flex-1">
                <div class="font-medium group-hover:text-primary">Civic Transparency & Public Trust Portal</div>
                <div class="text-xs text-outline">Tamper-evident public ledger, citizen metrics & open data API</div>
              </div>
              <span class="text-[10px] font-mono text-outline bg-surface-container px-2 py-0.5 rounded">Alt + 4</span>
            </a>
          </div>
        </div>
      `;
      document.body.appendChild(paletteModal);

      // Search filter logic inside modal
      const input = document.getElementById('commandPaletteInput');
      const resultsContainer = document.getElementById('commandPaletteResults');
      input.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        const items = resultsContainer.querySelectorAll('a');
        items.forEach(item => {
          const text = item.innerText.toLowerCase();
          item.style.display = text.includes(query) ? 'flex' : 'none';
        });
      });

      paletteModal.addEventListener('click', (e) => {
        if (e.target === paletteModal) {
          paletteModal.classList.add('hidden');
        }
      });
    }

    const openPalette = () => {
      paletteModal.classList.remove('hidden');
      const input = document.getElementById('commandPaletteInput');
      if (input) {
        input.value = '';
        input.focus();
        const items = document.querySelectorAll('#commandPaletteResults a');
        items.forEach(item => item.style.display = 'flex');
      }
    };

    const closePalette = () => {
      paletteModal.classList.add('hidden');
    };

    // Attach to search bars in header
    document.querySelectorAll('input[placeholder*="Search incidents"]').forEach(input => {
      input.addEventListener('focus', (e) => {
        e.target.blur();
        openPalette();
      });
    });

    // Keyboard trigger
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (paletteModal.classList.contains('hidden')) {
          openPalette();
        } else {
          closePalette();
        }
      }
      if (e.key === 'Escape' && !paletteModal.classList.contains('hidden')) {
        closePalette();
      }
      // Alt + 1/2/3/4 shortcuts
      if (e.altKey) {
        if (e.key === '1') window.location.href = 'index.html';
        if (e.key === '2') window.location.href = 'incident-intelligence.html';
        if (e.key === '3') window.location.href = 'resolution-verification.html';
        if (e.key === '4') window.location.href = 'public-transparency.html';
      }
    });
  }

  // 4. Notifications Dropdown Toggle
  function initNotifications() {
    const notifButtons = document.querySelectorAll('button[aria-label="Notifications"]');
    let drawer = document.getElementById('notificationsDrawer');
    if (!drawer) {
      drawer = document.createElement('div');
      drawer.id = 'notificationsDrawer';
      drawer.className = 'fixed right-4 top-16 w-80 sm:w-96 bg-surface-container-low border border-surface-container-high rounded-xl shadow-2xl z-50 hidden overflow-hidden';
      drawer.innerHTML = `
        <div class="p-3 bg-surface-container-lowest border-b border-surface-container-high flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="font-headline-sm text-sm font-bold text-on-surface">Operational Alerts</span>
            <span class="px-1.5 py-0.5 bg-error-container text-error text-[10px] font-mono rounded">3 NEW</span>
          </div>
          <button id="closeNotifBtn" class="text-outline hover:text-on-surface">
            <span class="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>
        <div class="divide-y divide-surface-container-high/60 max-h-96 overflow-y-auto">
          <a href="incident-intelligence.html" class="p-3 flex items-start gap-3 hover:bg-surface-container transition-colors block">
            <span class="w-2 h-2 rounded-full bg-error mt-1.5 shrink-0 animate-ping"></span>
            <div>
              <div class="text-xs font-semibold text-error uppercase font-label-caps">Tier 1 Critical Escalation</div>
              <div class="text-sm text-on-surface font-medium">Exposed High-Voltage Utility Cable (#CP-8492)</div>
              <div class="text-xs text-outline mt-0.5">Dispatched: Crew 04 en route • 4m ago</div>
            </div>
          </a>
          <a href="resolution-verification.html" class="p-3 flex items-start gap-3 hover:bg-surface-container transition-colors block">
            <span class="w-2 h-2 rounded-full bg-primary mt-1.5 shrink-0"></span>
            <div>
              <div class="text-xs font-semibold text-primary uppercase font-label-caps">Dual Verification Pending</div>
              <div class="text-sm text-on-surface font-medium">Main St Pothole & Culvert Repair (#CP-8461)</div>
              <div class="text-xs text-outline mt-0.5">Public Works Unit 02 uploaded repair telemetry</div>
            </div>
          </a>
          <a href="public-transparency.html" class="p-3 flex items-start gap-3 hover:bg-surface-container transition-colors block">
            <span class="w-2 h-2 rounded-full bg-tertiary mt-1.5 shrink-0"></span>
            <div>
              <div class="text-xs font-semibold text-tertiary uppercase font-label-caps">Public Ledger Synced</div>
              <div class="text-sm text-on-surface font-medium">Block #90428 verified across 12 civic validator nodes</div>
              <div class="text-xs text-outline mt-0.5">Open API v3.2 synchronized</div>
            </div>
          </a>
        </div>
        <div class="p-2 bg-surface-container-lowest text-center border-t border-surface-container-high">
          <a href="index.html" class="text-xs text-primary hover:underline font-label-caps uppercase">View Operational Command</a>
        </div>
      `;
      document.body.appendChild(drawer);

      document.getElementById('closeNotifBtn').addEventListener('click', () => {
        drawer.classList.add('hidden');
      });
    }

    notifButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        drawer.classList.toggle('hidden');
      });
    });

    document.addEventListener('click', (e) => {
      if (!drawer.contains(e.target)) {
        drawer.classList.add('hidden');
      }
    });
  }

  // 5. Global Toast Notification System
  window.CivicToast = {
    show: function (title, message, icon = 'info', type = 'primary') {
      let toastContainer = document.getElementById('civicToastContainer');
      if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'civicToastContainer';
        toastContainer.className = 'fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none';
        document.body.appendChild(toastContainer);
      }

      const toast = document.createElement('div');
      toast.className = 'pointer-events-auto bg-surface-container-high text-on-surface border border-primary/30 p-4 rounded-xl shadow-2xl max-w-sm flex items-start gap-3 transition-all transform duration-300 translate-y-2 opacity-0';

      const colorClass = type === 'tertiary' ? 'text-tertiary' :
                         type === 'error' ? 'text-error' :
                         type === 'secondary' ? 'text-secondary' : 'text-primary';

      toast.innerHTML = `
        <span class="material-symbols-outlined text-[22px] ${colorClass} shrink-0 mt-0.5">${icon}</span>
        <div class="flex-1">
          <h4 class="font-headline-sm text-sm font-bold text-on-surface">${title}</h4>
          <p class="font-body-sm text-on-surface-variant text-xs mt-0.5">${message}</p>
        </div>
        <button class="text-outline hover:text-on-surface p-1">
          <span class="material-symbols-outlined text-[16px]">close</span>
        </button>
      `;

      toastContainer.appendChild(toast);
      requestAnimationFrame(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
      });

      const close = () => {
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 300);
      };

      toast.querySelector('button').addEventListener('click', close);
      setTimeout(close, 4500);
    }
  };

  // Initialize on DOM Ready
  document.addEventListener('DOMContentLoaded', () => {
    updateActiveNav();
    startTelemetryTimer();
    initCommandPalette();
    initNotifications();

    // Wire global action buttons for feedback
    document.querySelectorAll('button').forEach(btn => {
      const text = btn.innerText || '';
      if (text.includes('Export') || text.includes('Dossier')) {
        btn.addEventListener('click', () => {
          CivicToast.show('Telemetry Dossier Exported', 'JSON and cryptographic Merkle proof saved to local workspace.', 'file_download', 'primary');
        });
      }
    });
  });

})();
