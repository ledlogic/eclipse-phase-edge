/* ep-daymode.js — Eclipse Phase campaign day/dark mode toggle + status chip
   Loaded at the bottom of <body> — DOM and jQuery are both available.
   A small inline <script> in <head> handles flash prevention before render. */

var EP_DAY_KEY = 'ep-day-mode';

// ── Day mode toggle ──────────────────────────────────────────────────────────

function epApplyDayMode(on) {
  $('body').toggleClass('day-mode', on);
  $('#day-toggle-btn').text(on ? '◈ DARK MODE' : '◈ DAY MODE');
}

epApplyDayMode(localStorage.getItem(EP_DAY_KEY) === 'true');
$('#ep-day-flash').remove();

$('#day-toggle-btn').on('click', function () {
  var on = !$('body').hasClass('day-mode');
  epApplyDayMode(on);
  localStorage.setItem(EP_DAY_KEY, on);
});

// ── Status chip injection ────────────────────────────────────────────────────
// Reads the current session status from the manifest embedded in the
// ep-nav-loader script block and injects a STATUS chip into .stats-bar
// if one is not already present. Hand-authored chips are always respected.
//   complete → green · STATUS: COMPLETE
//   current  → warn  · STATUS: CURRENT
//   upcoming → muted · STATUS: UPCOMING

var statsBar = document.querySelector('.stats-bar');
if (statsBar) {
  var existingStatus = $('.stats-bar .stat-chip').toArray().some(function (el) {
    return el.textContent.indexOf('STATUS:') !== -1;
  });

  if (!existingStatus) {
    var nav = document.getElementById('ep-session-nav');
    var loaderScript = document.getElementById('ep-nav-loader');

    if (nav && loaderScript) {
      var thisFile = nav.dataset.currentFile;
      var match = loaderScript.textContent.match(/const manifest\s*=\s*(\{[\s\S]*?\});\s*\n/);

      if (thisFile && match) {
        try {
          var manifest = JSON.parse(match[1]);
          var session = (manifest.sessions || []).find(function (s) {
            return s.file === thisFile;
          });

          var statusMap = {
            complete: { cls: 'green', label: 'STATUS: COMPLETE' },
            current:  { cls: 'warn',  label: 'STATUS: CURRENT'  },
            upcoming: { cls: '',      label: 'STATUS: UPCOMING'  }
          };

          if (session && statusMap[session.status]) {
            var cfg = statusMap[session.status];
            var chip = $('<span>')
              .addClass(cfg.cls ? 'stat-chip ' + cfg.cls : 'stat-chip')
              .text(cfg.label);
            $('.stats-bar .stat-chip').first().after(chip);
          }
        } catch (e) { /* malformed manifest — skip silently */ }
      }
    }
  }
}
