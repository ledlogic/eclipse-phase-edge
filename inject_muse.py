"""
inject_muse_v2.py
-----------------
Applies the session-03 muse name system to sessions 01, 02, 04, 05, 06, 07, 08.

Approach:
- Add .muse-label CSS to every target session
- Add muse name inputs UI wherever there is a "MUSE INTEL CUES" section
- Convert note-box muse cues (sessions 04, 05) to dialogue-line + muse-label format
- Leave NPC dialogue labels (dl-label with character names) as-is
- Inject muse JS into every target session
"""

import re
from pathlib import Path

TARGETS = [
    'session-01-better-on-the-inside.html',
    'session-02-binge.html',
    'session-04-unbodied-gutenberg.html',
    'session-05-cold-station.html',
    'session-06-signal-zero.html',
    'session-07-cry-for-help.html',
    'session-08-requiem-for-orcus.html',
]

MUSE_CSS = '''
  /* ── Muse label interactive badges ── */
  .muse-label {
    cursor: pointer;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 2px 7px;
    border: 1px solid;
    border-radius: 2px;
    white-space: nowrap;
    user-select: none;
    transition: opacity 0.15s, background 0.15s;
    display: inline-block;
    min-width: 60px;
    text-align: center;
  }
  .muse-label:hover { opacity: 0.72; }
  .muse-label:active { opacity: 0.5; }'''

MUSE_SETUP_DIV = '''    <div id="muse-setup" style="border:1px solid rgba(0,201,177,0.3); background:rgba(0,201,177,0.04); padding:0.7rem 0.8rem; margin-bottom:0.8rem;">
      <div style="font-family:'Share Tech Mono',monospace; font-size:12px; color:var(--accent2); letter-spacing:2px; margin-bottom:0.5rem;">◈ ENTER MUSE NAMES — CUES WILL UPDATE AS YOU TYPE</div>
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:0.5rem; margin-bottom:0.4rem;">
        <div>
          <div style="font-family:'Share Tech Mono',monospace; font-size:10px; color:#f5a623; margin-bottom:0.2rem;">SENTINEL 01</div>
          <input id="muse-1" type="text" placeholder="Muse name…" autocomplete="off"
            style="font-family:'Share Tech Mono',monospace; font-size:13px; color:#f5a623; background:rgba(245,166,35,0.06); border:1px solid rgba(245,166,35,0.3); border-bottom:2px solid #f5a623; padding:0.3rem 0.5rem; width:100%; outline:none; box-sizing:border-box; letter-spacing:1px;"
            oninput="updateMuses()">
        </div>
        <div>
          <div style="font-family:'Share Tech Mono',monospace; font-size:10px; color:#00c9b1; margin-bottom:0.2rem;">SENTINEL 02</div>
          <input id="muse-2" type="text" placeholder="Muse name…" autocomplete="off"
            style="font-family:'Share Tech Mono',monospace; font-size:13px; color:#00c9b1; background:rgba(0,201,177,0.06); border:1px solid rgba(0,201,177,0.3); border-bottom:2px solid #00c9b1; padding:0.3rem 0.5rem; width:100%; outline:none; box-sizing:border-box; letter-spacing:1px;"
            oninput="updateMuses()">
        </div>
        <div>
          <div style="font-family:'Share Tech Mono',monospace; font-size:10px; color:#8c52ff; margin-bottom:0.2rem;">SENTINEL 03</div>
          <input id="muse-3" type="text" placeholder="Muse name…" autocomplete="off"
            style="font-family:'Share Tech Mono',monospace; font-size:13px; color:#8c52ff; background:rgba(140,82,255,0.06); border:1px solid rgba(140,82,255,0.3); border-bottom:2px solid #8c52ff; padding:0.3rem 0.5rem; width:100%; outline:none; box-sizing:border-box; letter-spacing:1px;"
            oninput="updateMuses()">
        </div>
        <div>
          <div style="font-family:'Share Tech Mono',monospace; font-size:10px; color:#ffc107; margin-bottom:0.2rem;">SENTINEL 04</div>
          <input id="muse-4" type="text" placeholder="Muse name…" autocomplete="off"
            style="font-family:'Share Tech Mono',monospace; font-size:13px; color:#ffc107; background:rgba(255,193,7,0.06); border:1px solid rgba(255,193,7,0.3); border-bottom:2px solid #ffc107; padding:0.3rem 0.5rem; width:100%; outline:none; box-sizing:border-box; letter-spacing:1px;"
            oninput="updateMuses()">
        </div>
      </div>
      <div style="font-size:0.75rem; color:var(--muted); font-family:'Share Tech Mono',monospace;">Click any muse label in the cues below to cycle which sentinel's muse speaks that line. Names save to browser storage.</div>
    </div>
    <div style="font-size:0.85rem; color:var(--text); line-height:1.5; margin-bottom:0.7rem;">Muses deliver intel privately — in a character's inner ear, as a soft overlay, or a quiet ping. Click any muse label to reassign it to a different sentinel.</div>'''

MUSE_JS_TEMPLATE = '''
<script id="ep-muse-system">
// ── Muse Name System ────────────────────────────────────────────────────────
const MUSE_COLORS   = ['#f5a623','#00c9b1','#8c52ff','#ffc107'];
const MUSE_BG       = ['rgba(245,166,35,0.12)','rgba(0,201,177,0.12)','rgba(140,82,255,0.12)','rgba(255,193,7,0.12)'];
const MUSE_STORAGE  = ['ep_muse_1','ep_muse_2','ep_muse_3','ep_muse_4'];

const cueAssignments = %%CUE_ASSIGNMENTS%%;

function getMuseName(idx) {
  const el = document.getElementById('muse-' + (idx + 1));
  return el && el.value.trim() ? el.value.trim() : 'S0' + (idx + 1);
}

function updateMuses() {
  for (let i = 0; i < 4; i++) {
    const el = document.getElementById('muse-' + (i + 1));
    if (el) { try { sessionStorage.setItem(MUSE_STORAGE[i], el.value); } catch(e) {} }
  }
  document.querySelectorAll('.muse-label[data-cue]').forEach(el => {
    const cue = parseInt(el.dataset.cue);
    const si  = cueAssignments[cue];
    const name = getMuseName(si);
    const t = el.textContent;
    const suffix = t.includes(' — ') ? t.slice(t.indexOf(' — ')) : '';
    el.textContent = name + suffix;
    el.style.color       = MUSE_COLORS[si];
    el.style.background  = MUSE_BG[si];
    el.style.borderColor = MUSE_COLORS[si];
    el.title = 'Click to cycle sentinel';
  });
}

function cycleMuse(el) {
  const cue = parseInt(el.dataset.cue);
  cueAssignments[cue] = (cueAssignments[cue] + 1) % 4;
  updateMuses();
}

function loadMuseNames() {
  for (let i = 0; i < 4; i++) {
    const el = document.getElementById('muse-' + (i + 1));
    if (el) { try { const s = sessionStorage.getItem(MUSE_STORAGE[i]); if (s) el.value = s; } catch(e) {} }
  }
  updateMuses();
}

document.addEventListener('DOMContentLoaded', loadMuseNames);
</script>'''


COLORS = ['#f5a623','#00c9b1','#8c52ff','#ffc107']
BG     = ['rgba(245,166,35,0.12)','rgba(0,201,177,0.12)','rgba(140,82,255,0.12)','rgba(255,193,7,0.12)']

def make_muse_label(cue_idx, suffix='◈'):
    si = cue_idx % 4
    return (f'<span class="muse-label dl-label" data-cue="{cue_idx}" '
            f'onclick="cycleMuse(this)" '
            f'style="color:{COLORS[si]};border-color:{COLORS[si]};background:{BG[si]};">'
            f'{suffix}</span>')


def convert_notebox_to_dialogue(html, muse_section_start, muse_section_end, cue_counter):
    """
    Within the muse cues section, convert note-box divs that contain quoted text
    into dialogue-line divs with muse-label badges.
    Pattern: <div class="note-box ...">TEXT</div>  →  dialogue-line + muse-label
    """
    section = html[muse_section_start:muse_section_end]
    
    # Match note-box divs that contain muse cue text (quoted strings)
    notebox_pat = re.compile(
        r'<div class="note-box([^"]*)">(.*?)</div>',
        re.DOTALL
    )
    
    def replace_notebox(m):
        box_class = m.group(1).strip()
        content = m.group(2).strip()
        
        # Only convert if content looks like a muse cue (starts with quote or is a sentence)
        # Skip if it's a GM NOTE
        if 'GM NOTE' in content or content.startswith('<strong>') or 'note' in box_class.lower():
            return m.group(0)
        
        # Extract the quote text if wrapped in quotes
        idx = cue_counter[0]
        cue_counter[0] += 1
        label = make_muse_label(idx)
        
        return (f'<div class="dialogue-line">\n'
                f'      {label}\n'
                f'      <span class="dl-text"><em>{content}</em></span>\n'
                f'    </div>')
    
    new_section = notebox_pat.sub(replace_notebox, section)
    return html[:muse_section_start] + new_section + html[muse_section_end:]


def inject_muse(filepath):
    path = Path(filepath)
    html = path.read_text(encoding='utf-8')

    # Skip if already processed
    if 'ep-muse-system' in html:
        print(f"  SKIP (already processed): {path.name}")
        return

    # ── 1. Add .muse-label CSS ───────────────────────────────────────────────
    if '.muse-label' not in html:
        html = html.replace(
            '@media print { #ep-session-nav { display: none !important; } }',
            '@media print { #ep-session-nav { display: none !important; } }' + MUSE_CSS
        )

    # ── 2. Find MUSE INTEL CUES section ─────────────────────────────────────
    cue_counter = [0]
    muse_label_pos = html.find('◈ MUSE INTEL CUES')
    
    if muse_label_pos >= 0:
        # Find the containing section-label div and the npc-card/brief-panel after it
        # Insert muse-setup div right before the section-label
        # Back up to the start of the <div class="section-label..."> tag
        section_start = html.rfind('<div', 0, muse_label_pos)
        html = html[:section_start] + MUSE_SETUP_DIV + '\n    ' + html[section_start:]
        muse_label_pos = html.find('◈ MUSE INTEL CUES')  # re-find after insert

        # Find the end of the muse intel section
        # Look for the next sibling section-label (not muse)
        section_after = html.find('section-label', muse_label_pos + 50)
        if section_after > 0:
            muse_end = html.rfind('<div', muse_label_pos + 50, section_after)
        else:
            muse_end = len(html) - 5000  # leave footer area
        
        # For sessions with note-box style cues (04, 05), convert them
        fname = path.name
        if fname in ('session-04-unbodied-gutenberg.html', 'session-05-cold-station.html'):
            html = convert_notebox_to_dialogue(html, muse_label_pos, muse_end, cue_counter)
        
        # Convert any ◈-prefixed dl-label spans in the section
        muse_label_pos = html.find('◈ MUSE INTEL CUES')  # re-find again
        section_after = html.find('section-label', muse_label_pos + 50)
        if section_after > 0:
            muse_end_2 = html.rfind('<div', muse_label_pos + 50, section_after)
        else:
            muse_end_2 = len(html) - 5000

        muse_section_html = html[muse_label_pos:muse_end_2]
        
        dl_pat = re.compile(r'<span class="([^"]*dl-label[^"]*)"([^>]*)>(◈[^<]*)</span>')
        
        def conv_dl(m):
            content = m.group(3)
            idx = cue_counter[0]
            cue_counter[0] += 1
            si = idx % 4
            return (f'<span class="muse-label dl-label" data-cue="{idx}" '
                    f'onclick="cycleMuse(this)" '
                    f'style="color:{COLORS[si]};border-color:{COLORS[si]};background:{BG[si]};">'
                    f'{content}</span>')
        
        new_muse = dl_pat.sub(conv_dl, muse_section_html)
        html = html[:muse_label_pos] + new_muse + html[muse_end_2:]

    total_cues = cue_counter[0]
    
    # ── 3. Build cueAssignments ──────────────────────────────────────────────
    if total_cues == 0:
        # Minimal placeholder for sessions without muse cues
        cue_arr = '[0, 1, 2, 3]'
    else:
        assignments = [i % 4 for i in range(total_cues)]
        groups = []
        for i in range(0, len(assignments), 4):
            groups.append(', '.join(str(x) for x in assignments[i:i+4]))
        cue_arr = '[' + ',  '.join(groups) + ']'
    
    muse_js = MUSE_JS_TEMPLATE.replace('%%CUE_ASSIGNMENTS%%', cue_arr)
    
    # ── 4. Remove stale version if any ──────────────────────────────────────
    html = re.sub(r'<script id="ep-muse-system">.*?</script>\s*', '', html, flags=re.DOTALL)
    
    # ── 5. Inject before </body> ─────────────────────────────────────────────
    html = html.replace('</body>', muse_js + '\n</body>', 1)
    
    path.write_text(html, encoding='utf-8')
    print(f"  OK: {path.name} ({total_cues} cue(s))")


print("Injecting muse system (v2)...")
for f in TARGETS:
    inject_muse(f'/home/claude/{f}')
print("Done.")
