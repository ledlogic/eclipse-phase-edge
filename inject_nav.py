"""
inject_nav.py
-------------
For each session HTML file listed in ep-campaign.json:
  1. Standardizes <title>, .header-tag, and .header-sub text.
  2. Injects a <nav> bar with Prev / Session list / Next links
     driven entirely from ep-campaign.json — no hrefs are hardcoded
     in the HTML files themselves.
  3. Injects the nav loader <script> block before </body>.

Run from the directory containing ep-campaign.json and the HTML files.
To update links: edit ep-campaign.json only, then re-run this script.

Companion files (run separately):
  ep-muse.js      — shared muse name system, localStorage cross-page persistence
  inject_muse.py  — applies muse cue badges to session files
"""

import json, re, sys
from pathlib import Path

# ── Load manifest ────────────────────────────────────────────────────────────
manifest = json.loads(Path("ep-campaign.json").read_text())
sessions = manifest["sessions"]

# Only sessions that have an actual file
with_file = [s for s in sessions if s["file"]]

NAV_STYLE = ""  # CSS lives in ep-campaign.css

FLASH_SCRIPT = """<script>/* ep: flash prevention — must stay in <head> */
(function(){if(localStorage.getItem('ep-day-mode')==='true'){var s=document.createElement('style');s.id='ep-day-flash';s.textContent='body{--void:#f0f2f5!important;--deep:#e8ecf4!important;--panel:#e0e5ef!important;--border:#c0cad8!important;--accent:#b06000!important;--accent2:#007a6b!important;--warn:#8a5a00!important;--muted:#5a6878!important;--text:#1a2530!important;--textbright:#080f18!important;background:#f0f2f5!important;color:#1a2530!important;}';document.head.appendChild(s);}}());
</script>"""

NAV_SCRIPT_TEMPLATE = """
<script id="ep-nav-loader">
// ── Eclipse Phase Session Navigation ────────────────────────────────────────
// Manifest is embedded at inject time from ep-campaign.json.
// To change links: edit ep-campaign.json, then re-run inject_nav.py.
// Navigation uses jQuery click handlers (data-href) for server compatibility.
(function () {
  const manifest = %%MANIFEST%%;

  const nav      = document.getElementById('ep-session-nav');
  if (!nav) return;

  const sessions = manifest.sessions;
  const thisFile = nav.dataset.currentFile;
  const withFile = sessions.filter(s => s.file);

  const fileIdx  = withFile.findIndex(s => s.file === thisFile);
  const prevSess = fileIdx > 0 ? withFile[fileIdx - 1] : null;
  const nextSess = fileIdx < withFile.length - 1 ? withFile[fileIdx + 1] : null;

  let html = '<span class="ep-nav-home ep-nav-go" data-href="index.html" title="Edge of the Light — Campaign Index">◈ INDEX</span>';
  html += '<span class="ep-nav-sep">|</span>';
  html += '<span class="ep-nav-label">SESSIONS</span>';
  html += '<span class="ep-nav-sep">|</span>';

  if (prevSess) {
    html += `<span class="ep-nav-arrow ep-nav-go" data-href="${prevSess.file}" title="Session ${prevSess.number}: ${prevSess.title}">◀ ${prevSess.number}</span>`;
  } else {
    html += `<span class="ep-nav-arrow ep-disabled">◀</span>`;
  }

  html += '<div class="ep-nav-links">';
  sessions.forEach(s => {
    const isCurrent = s.file === thisFile;
    const noFile    = !s.file;
    const cls   = isCurrent ? 'ep-nav-link ep-current' : noFile ? 'ep-nav-link ep-no-file' : 'ep-nav-link ep-nav-go';
    const dhref = s.file ? ` data-href="${s.file}"` : '';
    const label = s.number + ' — ' + s.title.toUpperCase();
    const tip   = s.location ? `${s.title} · ${s.location}` : s.title;
    html += `<span class="${cls}"${dhref} title="${tip}">${label}</span>`;
  });
  html += '</div>';

  if (nextSess) {
    html += `<span class="ep-nav-arrow ep-nav-go" data-href="${nextSess.file}" title="Session ${nextSess.number}: ${nextSess.title}">${nextSess.number} ▶</span>`;
  } else {
    html += `<span class="ep-nav-arrow ep-disabled">▶</span>`;
  }

  nav.innerHTML = html;

  // ── jQuery click delegation ──────────────────────────────────────────────
  $(document).on('click', '.ep-nav-go[data-href]', function () {
    window.location.href = $(this).data('href');
  });
})();
</script>
"""

BOTTOM_SCRIPTS = (
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>\n'
    '<script src="ep-daymode.js"></script>\n'
)

def inject_file(session):
    path = Path(session["file"])
    if not path.exists():
        print(f"  SKIP (not found): {path}")
        return

    html = path.read_text(encoding="utf-8")

    # ── 1. Standardize <title> ───────────────────────────────────────────────
    new_title = f"{session['title'].upper()} | Eclipse Phase — Session {session['number']} GM Reference"
    html = re.sub(r"<title>[^<]*</title>", f"<title>{new_title}</title>", html, count=1)

    # ── 2. Standardize .header-tag text ─────────────────────────────────────
    if session.get("header_tag"):
        html = re.sub(
            r'(<div class="header-tag">)[^<]*(</div>)',
            rf'\g<1>{session["header_tag"]}\g<2>',
            html, count=1
        )

    # ── 3. Standardize .header-sub text ─────────────────────────────────────
    if session.get("header_sub"):
        html = re.sub(
            r'(<div class="header-sub">)[^<]*(</div>)',
            rf'\g<1>{session["header_sub"]}\g<2>',
            html, count=1
        )

    # ── 4. Remove any previously injected nav (idempotent re-runs) ──────────
    html = re.sub(r'<style id="ep-nav-style">.*?</style>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<nav id="ep-session-nav"[^>]*>.*?</nav>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<script id="ep-nav-loader">.*?</script>\s*', '', html, flags=re.DOTALL)

    # ── 4b. Remove any jQuery / ep-daymode from <head> (they go at bottom) ──
    JQUERY = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>'
    DAYMODE = '<script src="ep-daymode.js"></script>'
    for tag in (JQUERY, DAYMODE):
        html = html.replace(tag + '\n', '').replace(tag, '')

    # Ensure flash-prevention inline script is in <head> (idempotent)
    html = re.sub(r'<script>\s*/\* ep: flash prevention.*?</script>\s*', '', html, flags=re.DOTALL)
    html = html.replace('</head>', FLASH_SCRIPT + '\n</head>', 1)


    # ── 5. Inject nav style + bar after <body> (or before <header>) ─────────
    nav_bar = f'<nav id="ep-session-nav" data-current-file="{session["file"]}"></nav>\n'
    insert_before = re.search(r'<header[\s>]', html)
    if insert_before:
        pos = insert_before.start()
        html = html[:pos] + NAV_STYLE + nav_bar + html[pos:]
    else:
        # fallback: right after <body>
        html = re.sub(r'(<body[^>]*>)', rf'\1\n{NAV_STYLE}{nav_bar}', html, count=1)

    # ── 6. Inject jQuery + ep-daymode + nav script before </body> ──────────
    manifest_json = json.dumps(manifest, ensure_ascii=False)
    nav_script = NAV_SCRIPT_TEMPLATE.replace("%%MANIFEST%%", manifest_json)
    bottom = BOTTOM_SCRIPTS + nav_script
    html = html.replace("</body>", bottom + "\n</body>", 1)

    path.write_text(html, encoding="utf-8")
    print(f"  OK: {path}")


# ── Main ─────────────────────────────────────────────────────────────────────
print(f"Processing {len(with_file)} session files...")
for s in with_file:
    inject_file(s)
print("Done.")
