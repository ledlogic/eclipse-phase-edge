"""
externalize_muse.py
-------------------
For every session HTML file:
  1. Extracts the cueAssignments array from the inline ep-muse-system script
     (or the older inline muse block inside session-03's main <script>).
  2. Replaces the entire inline block with:
       <script>const cueAssignments = [...];</script>
       <script src="ep-muse.js"></script>
  3. Replaces any remaining sessionStorage refs with localStorage in inline scripts.

Run from the directory containing the HTML files and ep-muse.js.
"""

import json, re
from pathlib import Path

SESSION_FILES = [
    'session-01-better-on-the-inside.html',
    'session-02-binge.html',
    'session-03-dead-drop-vesta.html',
    'session-04-unbodied-gutenberg.html',
    'session-05-cold-station.html',
    'session-06-signal-zero.html',
    'session-07-cry-for-help.html',
    'session-08-requiem-for-orcus.html',
    'session-09-still-life-with-teeth.html',
]

EXTERNAL_BLOCK = '<script src="ep-muse.js"></script>'

def extract_cue_assignments(html):
    """Return the cueAssignments array literal string, or None if not found."""
    m = re.search(r'const cueAssignments\s*=\s*(\[.*?\]);', html, re.DOTALL)
    return m.group(1).strip() if m else None

def remove_inline_muse_scripts(html):
    """
    Remove:
    - <script id="ep-muse-system">…</script>
    - <script>const cueAssignments = …; … loadMuseNames …</script>  (session-03 style)
    - Standalone <script src="ep-muse.js"></script> (idempotent re-runs)
    """
    # Remove labelled block
    html = re.sub(
        r'\s*<script id="ep-muse-system">.*?</script>',
        '', html, flags=re.DOTALL
    )
    # Remove any existing external ref (idempotent)
    html = html.replace('\n' + EXTERNAL_BLOCK, '')
    html = html.replace(EXTERNAL_BLOCK, '')

    # Remove the large inline muse block in session-03's main <script>
    # Pattern: starts at "// ── Muse Name System" inside a <script> tag
    # and ends at "document.addEventListener('DOMContentLoaded', loadMuseNames);"
    html = re.sub(
        r'\n// ── Muse Name System ──+.*?document\.addEventListener\(\'DOMContentLoaded\', loadMuseNames\);\n',
        '\n',
        html, flags=re.DOTALL
    )

    # Also strip standalone <script> blocks that contain ONLY the muse system
    # (the ones inject_muse_v2.py created)
    # These look like: <script>\nconst MUSE_COLORS…\n</script>
    html = re.sub(
        r'<script>\s*\n// ── Muse Name System.*?</script>\s*\n',
        '', html, flags=re.DOTALL
    )

    return html

def fix_storage(html):
    """Replace any leftover sessionStorage refs in inline scripts with localStorage."""
    # Only touch inline <script> blocks, not attribute values
    def replace_in_script(m):
        return m.group(0).replace('sessionStorage', 'localStorage')

    return re.sub(r'<script[^>]*>.*?</script>', replace_in_script, html, flags=re.DOTALL)

def process_file(fname):
    path = Path(fname)
    if not path.exists():
        print(f'  SKIP (not found): {fname}')
        return

    html = path.read_text(encoding='utf-8')

    # 1. Extract the cueAssignments before we remove anything
    cue_arr = extract_cue_assignments(html)

    # 2. Strip all inline muse blocks
    html = remove_inline_muse_scripts(html)

    # 3. Fix any leftover sessionStorage
    html = fix_storage(html)

    # 4. Build the replacement snippet
    if cue_arr:
        inline_cue = f'<script>const cueAssignments = {cue_arr};</script>'
    else:
        # No cueAssignments found — use a simple default
        inline_cue = '<script>const cueAssignments = [0, 1, 2, 3];</script>'
        print(f'  NOTE: no cueAssignments found in {fname}, using default')

    replacement = inline_cue + '\n' + EXTERNAL_BLOCK

    # 5. Inject before </body>
    if '</body>' in html:
        html = html.replace('</body>', replacement + '\n</body>', 1)
    else:
        html += '\n' + replacement

    path.write_text(html, encoding='utf-8')
    print(f'  OK: {fname}  cues={cue_arr[:60] if cue_arr else "default"}…')


print(f'Processing {len(SESSION_FILES)} session files…')
for f in SESSION_FILES:
    process_file(f)
print('Done.')
