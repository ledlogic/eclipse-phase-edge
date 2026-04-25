// ── Eclipse Phase — Shared Muse Name System ─────────────────────────────────
// ep-muse.js  •  place alongside the session HTML files
//
// Each session HTML page declares its own cueAssignments array in a small
// inline <script> BEFORE loading this file, e.g.:
//
//   <script>const cueAssignments = [0,1,2,3, 0,1,2,3, 0,1];</script>
//   <script src="ep-muse.js"></script>
//
// Muse names are stored in localStorage so they persist across all pages
// served from the same origin (same local folder or web server).
// ─────────────────────────────────────────────────────────────────────────────

const MUSE_COLORS  = ['#f5a623', '#00c9b1', '#8c52ff', '#ffc107'];
const MUSE_BG      = [
  'rgba(245,166,35,0.12)',
  'rgba(0,201,177,0.12)',
  'rgba(140,82,255,0.12)',
  'rgba(255,193,7,0.12)',
];
const MUSE_STORAGE = ['ep_muse_1', 'ep_muse_2', 'ep_muse_3', 'ep_muse_4'];

// cueAssignments must be declared by each page before this script loads.
// Provide a fallback in case a page forgets.
if (typeof cueAssignments === 'undefined') {
  // eslint-disable-next-line no-var
  var cueAssignments = [0, 1, 2, 3];
}

function getMuseName(idx) {
  const el = document.getElementById('muse-' + (idx + 1));
  return el && el.value.trim() ? el.value.trim() : 'S0' + (idx + 1);
}

function updateMuses() {
  // Persist to localStorage so names survive page navigation
  for (let i = 0; i < 4; i++) {
    const el = document.getElementById('muse-' + (i + 1));
    if (el) {
      try { localStorage.setItem(MUSE_STORAGE[i], el.value); } catch (e) {}
    }
  }

  // Update every badge on this page
  document.querySelectorAll('.muse-label[data-cue]').forEach(el => {
    const cue = parseInt(el.dataset.cue, 10);
    if (isNaN(cue) || cue >= cueAssignments.length) return;
    const si   = cueAssignments[cue];
    const name = getMuseName(si);
    const text = el.textContent;
    const suffix = text.includes(' — ') ? text.slice(text.indexOf(' — ')) : '';
    el.textContent    = name + suffix;
    el.style.color        = MUSE_COLORS[si];
    el.style.background   = MUSE_BG[si];
    el.style.borderColor  = MUSE_COLORS[si];
    el.title = 'Click to reassign to next sentinel';
  });
}

function cycleMuse(el) {
  const cue = parseInt(el.dataset.cue, 10);
  if (isNaN(cue)) return;
  cueAssignments[cue] = (cueAssignments[cue] + 1) % 4;
  updateMuses();
}

function loadMuseNames() {
  for (let i = 0; i < 4; i++) {
    const el = document.getElementById('muse-' + (i + 1));
    if (el) {
      try {
        const saved = localStorage.getItem(MUSE_STORAGE[i]);
        if (saved !== null) el.value = saved;
      } catch (e) {}
    }
  }
  updateMuses();
}

document.addEventListener('DOMContentLoaded', loadMuseNames);
