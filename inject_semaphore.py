"""
inject_semaphore.py
-------------------
Weaves the SCP-179 / Sauelsuesor "Semaphore" thread through sessions 05–09.

Per session:
  05 — Lok's buried Ozma file; the secondary signal in MESA's device data
  06 — Sauelsuesor has been pointing at FK7 for 11 months; the source object's silence
  07 — The swarm received something once from the direction of the sun
  08 — MESA's theory on the Gutenberg secondary signal; the Semaphore as downtime thread
  09 — Four arms; the campaign convergence; what she was pointing at all along

All insertions go into GM Notes as collapsible entries, matching existing style.
"""

import re
from pathlib import Path

# ── Shared style helpers ────────────────────────────────────────────────────

def collapse_entry(title, body, open=False):
    """Produce a collapse-btn + collapse-content block."""
    open_attr = ' open' if open else ''
    return f'''
      <button class="collapse-btn" onclick="toggleCollapse(this)">◈ {title} <span>▾</span></button>
      <div class="collapse-content{open_attr}">
        {body}
      </div>'''

def note(text, colour=''):
    cls = f'note-box {colour}' if colour else 'note-box'
    return f'<div class="{cls}">{text}</div>'

def test_item(skill, desc, colour='signal'):
    return f'''<div class="test-item"><div class="test-skill {colour}">{skill}</div><div class="test-desc">{desc}</div></div>'''

def section_label(text, colour='signal'):
    return f'\n    <div class="section-label {colour}">◈ {text}</div>\n'

def npc_card_open(style=''):
    s = f' style="{style}"' if style else ''
    return f'    <div class="npc-card"{s}>\n'

def npc_card_close():
    return '    </div>\n'


# ══════════════════════════════════════════════════════════════════════════════
# SESSION 05 — Cold Station / Iapetus
# ══════════════════════════════════════════════════════════════════════════════

S05_SEMAPHORE = section_label('THE SEMAPHORE — BURIED OZMA FILE') + npc_card_open() + collapse_entry(
    'WHAT LOK IS SITTING ON',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.6rem;">
          Lok knows more about the Gutenberg tight-beam transmission than she has disclosed. Ozma's prior analysis — the file she is protecting — contains a detail about the secondary signal braided around the fetch's carrier wave. Ozma flagged it internally as anomalous and then buried the analysis rather than share it with Firewall. Lok's job is partly to make sure it stays buried.
        </div>''' +
    test_item('RESEARCH 60', 'Cross-referencing Lok\'s personal mesh queries against Ozma\'s known signal-analysis taxonomy reveals she ran a search on "anomalous solar-proximate transmissions" three days before the team arrived. The query returned a classified Ozma file. The file number is visible in her query log. The file itself is not accessible from Iapetus.', 'ozma') +
    test_item('KINESICS 50 (vs Lok)', 'If the secondary signal is mentioned directly — even obliquely, as "there was something else in the Gutenberg data" — Lok\'s response is one beat too controlled. She already knows what it is. She was briefed on it before she arrived here.', 'warn') +
    note('<strong style="color:var(--signal)">THE BURIED DETAIL:</strong> The secondary signal in the Gutenberg transmission did not originate from outside the ecliptic. It came from the direction of the Sun. Ozma\'s analysts confirmed this and filed it under a restricted access header: <em>COEWS-ANOMALY-7741</em>. COEWS stands for Composite Orbital Early Warning System. Ozma knows what the Semaphore is. They have known for decades. They are not sharing.') +
    test_item('INFOSEC 60 (Lok\'s device)', 'If the team has access to Lok\'s mesh history, the COEWS reference appears once — in a deleted draft message she never sent. The recipient field is blank. The message body reads only: <em>"It pointed at Gutenberg before the event. Confirm whether this is logged at our end."</em>', 'danger'),
    open=False
) + collapse_entry(
    'MUSE INTEL — SEMAPHORE THREAD',
    test_item('◈', 'There\'s a file reference in Lok\'s query log I can\'t resolve from here. The header is COEWS-ANOMALY-7741. COEWS is a Foundation-era acronym — Composite Orbital Early Warning System. I don\'t have anything past that in accessible records.', 'signal') +
    test_item('◈', 'The secondary signal in the Gutenberg data came from sunward. Not from outside the ecliptic — from inside it. Whatever sent the warning was already in the solar system. Has been for a long time, I think.', 'signal'),
    open=False
) + npc_card_close()


# ══════════════════════════════════════════════════════════════════════════════
# SESSION 06 — Signal Zero / FK7
# ══════════════════════════════════════════════════════════════════════════════

S06_SEMAPHORE = section_label('THE SEMAPHORE — SHE WAS ALREADY POINTING HERE') + npc_card_open() + collapse_entry(
    'ELEVEN MONTHS',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.6rem;">
          An Extropian belt-mining cooperative runs a small observatory relay at 38 AU — primarily for navigation, secondarily because its operators are curious people who log everything. Eleven months ago their log shows an anomalous notation: the solar-proximate figure they call the Semaphore — a recurring legend in outer-system fringe culture — extended what appeared to be a new limb. The limb pointed in the direction of FK7-class Kuiper coordinates.
        </div>
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.6rem;">
          The notation was filed and ignored. The cooperative's operators have seen the Semaphore change position before — it always means something dangerous is coming from wherever she points, and there's nothing anyone at 38 AU can do about something at 52 AU. You note it. You move on. You don't sleep quite as well for a while.
        </div>''' +
    test_item('RESEARCH 50', 'Pulling outer-system observatory logs — available on the Extropian open mesh — returns the cooperative\'s notation alongside three other similar observations from different observers over the same eleven-month window. They were not in contact with each other. They all describe the same new limb pointing in the same direction. Nobody filed a formal report.', 'teal') +
    note('MESA processes this in silence when told. Then: <em>"She was pointing here before the source object started transmitting. Before anyone knew this location existed. She saw it first."</em> A long pause. <em>"I find that either deeply reassuring or deeply alarming. I cannot currently determine which."</em>', 'signal') +
    test_item('KNOW: TITAN TECH / KNOW: ASTROBIOLOGY', 'The source object stopped transmitting when the team arrived — MESA said "it wasn\'t calling for us." The Semaphore was pointing here for eleven months before that. If the object was transmitting a signal and the Semaphore detected it, she was pointing at the signal, not the object. She was trying to flag an incoming broadcast before anyone received it. She failed to stop the Gutenberg one. She may have been trying to stop this one too — by pointing at its source so someone would get here first and interrupt it.', 'warn'),
    open=False
) + collapse_entry(
    'WHAT THE SOURCE OBJECT\'S SILENCE MEANS',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.5rem;">
          The object stopped transmitting the moment the team entered the chamber. MESA's reading: <em>"It wasn't calling for us."</em> But there is another interpretation. It stopped because it was answered. Not by the team — by the Semaphore's pointing. Something sunward registered the team's arrival at this location and sent a signal of its own — too faint and too fast for the team's equipment to catch, but enough for something ancient and sensitive near the Sun to acknowledge.
        </div>''' +
    note('This is not confirmable in this session. It is a seed. MESA will return to it at Vanth. <strong style="color:var(--signal)">Do not over-explain it here.</strong> Let the silence after the object stops transmitting carry the weight. The players will remember it.') +
    test_item('◈ MUSE', 'The object is silent. The chamber is silent. The GS-Perennial\'s hull creaks once from thermal expansion. Outside the port window the sun is a star indistinguishable from the others. Something near it has been watching this location for nearly a year. We just walked into what it was watching.', 'signal'),
    open=False
) + npc_card_close()


# ══════════════════════════════════════════════════════════════════════════════
# SESSION 07 — Cry for Help / Arrokoth
# ══════════════════════════════════════════════════════════════════════════════

S07_SEMAPHORE = section_label('THE SEMAPHORE — WHAT THE SWARM RECEIVED') + npc_card_open() + collapse_entry(
    'THE SWARM HEARD IT TOO',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.6rem;">
          AWE — the evolved nanoswarm — has been sending a status report to a dead TITAN address for ten years. It stopped four years ago when it concluded the recipient was gone. What it has not mentioned until now, because no one asked the right question: it also <em>received</em> something once. Not from the dead address. From a different direction entirely.
        </div>
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.6rem;">
          The signal came from the direction of the inner solar system — from sunward. It was not in any protocol AWE recognises. It arrived approximately six years ago, during what AWE describes as its "transition period" — the eighteen months it spent reorienting from weapon to something else. AWE did not know what to do with it. It has kept a copy of the raw signal in cold storage.
        </div>''' +
    test_item('SUBSTRATE NEGOTIATION — UNLOCK CONDITION', 'AWE will share the signal recording only if the team has established genuine trust — sharing something meaningful in return (the Gutenberg data, MESA\'s analysis, the FK7 source object finding). It doesn\'t offer it proactively. The right question is: <em>"Has anything ever tried to contact you from outside this system?"</em>', 'teal') +
    note('<strong style="color:var(--signal)">AWE ON THE SIGNAL:</strong> <em>"It was not language. It was not data. It was — orientation. The way a hand points. I understood it as: here. Here is where the danger is. Here is what you are near. I did not know what to do with this information. I stored it because I store everything now. I did not know if it was meant for me or if I simply happened to be in the way of it."</em>') +
    test_item('RESEARCH 60 (signal analysis)', 'The raw recording AWE provides is 0.003 seconds long. It is broadband — hits every frequency simultaneously. The waveform shape matches the secondary signal from the Gutenberg transmission data, if R.A.I.D. or MESA does the comparison. Same source. Same direction. Six years ago AWE received a warning about its own location — before the colony team even arrived here.', 'signal') +
    note('MESA\'s response to this, when told: a long silence. Then: <em>"She has been pointing at everything we\'ve visited. In the order we visited it. Either that is a coincidence of extraordinary proportion — or she knew the itinerary before we did."</em>', 'warn'),
    open=False
) + collapse_entry(
    'THE SEMAPHORE IN FRINGE CULTURE',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.5rem;">
          AWE has absorbed a decade of outer-system mesh traffic, including fringe community folklore. It knows the Semaphore by several names — the Pointer, the Sister, the Lookout, the thing near the sun that grows more arms when something is wrong. It has logged 23 separate outer-system community references to her in its ten years of passive mesh monitoring.
        </div>''' +
    test_item('AWE ON THE SEMAPHORE', '<em>"The communities out here regard her as a warning system. Something very old that watches and cannot act, only indicate. Many of them have a protocol: when the Pointer extends a new arm, you note the direction and you move away from it. The communities that did this consistently show higher survival rates in my sample. I find this statistically interesting."</em>', 'teal') +
    test_item('AWE — IF ASKED ABOUT THE CURRENT ARM COUNT', '<em>"As of my last mesh synchronisation, outer-system observer logs indicate she currently has four limbs extended. Two I can correlate to locations your team has visited. The other two are pointed further out than you have yet gone."</em>', 'danger'),
    open=False
) + npc_card_close()


# ══════════════════════════════════════════════════════════════════════════════
# SESSION 08 — Requiem for Orcus / Vanth
# ══════════════════════════════════════════════════════════════════════════════

S08_SEMAPHORE = section_label('THE SEMAPHORE — MESA\'S THEORY') + npc_card_open() + collapse_entry(
    'MESA HAS BEEN THINKING ABOUT THE SECONDARY SIGNAL',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.6rem;">
          This is a session without a clock. MESA has had transit time to process. She brings this up herself — not as a briefing, but as a conversation. She sits with it the way someone brings up something they have been turning over in private for a long time and finally decided to say aloud.
        </div>''' +
    note('<strong style="color:var(--textbright)">MESA — OPENING:</strong> <em>"I want to talk about the other signal. The one in the Gutenberg data that wasn\'t the fetch. I\'ve been working on it since Iapetus. I think I know what it is. I don\'t think you\'re going to find it satisfying."</em>') +
    note('<strong style="color:var(--textbright)">MESA — THE THEORY:</strong> <em>"Everything we\'ve visited — Gutenberg, FK7, Arrokoth — something sunward was pointing at before we got there. The signal waveform is consistent across all three observations. AWE\'s recording, the Gutenberg secondary, the observatory logs at FK7. Same source. Same direction. It is not a TITAN. It is not Ozma. It is something that has been in the solar system for a very long time and has been watching the outer system for threats and has been trying to tell someone for years. We are the first people who have been close enough to enough of what it was pointing at to possibly understand what it means."</em>') +
    note('<strong style="color:var(--textbright)">MESA — IF PUSHED ON WHAT IT IS:</strong> <em>"I don\'t know what it is. I know it is very large and very old and it communicates by pointing and it has been pointing at things that turn out to be existential threats to transhumanity. I find it — comforting, actually. That something has been watching. Less comforting that it cannot seem to stop what it is watching from happening. It can only indicate. It has been indicating, very urgently, for a long time. Nobody was out here to see."</em> She pauses. <em>"Until now."</em>', 'signal') +
    test_item('IF THE TEAM ASKS WHAT IT\'S POINTING AT NOW', 'MESA pulls outer-system observatory logs — the same cooperative data from session-06, updated. The Semaphore currently has four arms extended. Two correlate to locations the team has visited. The third points toward a KBO at approximately 52 AU. MESA notes the coordinates quietly. They match the Firewall mission brief the team received for session-09. She does not say this is concerning. She does not need to.', 'danger'),
    open=False
) + collapse_entry(
    'WHAT TO DO WITH THIS IN THE REPORT',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.5rem;">
          The Firewall report the team files from Vanth will shape how Firewall responds in the final arc. The Semaphore thread is a decision point: do they include it?
        </div>''' +
    test_item('INCLUDE IT', 'Firewall receives the COEWS reference, AWE\'s signal recording, MESA\'s analysis. Someone in Firewall\'s inner-system network runs the COEWS acronym and gets very quiet. The team gets a priority-1 response: <em>"Confirm FK7 coordinates and proceed to KBO 2119-HR4. Do not wait for backup."</em> They were already going. Now they know Firewall knows why.', 'teal') +
    test_item('OMIT IT', 'The Semaphore thread stays between the team and MESA. Firewall sends them to KBO 2119-HR4 on the strength of the Lithohex intelligence alone. When they arrive and understand what\'s there, they will know that whatever is near the sun pointed at it first — and Firewall doesn\'t know that. That gap in their handler\'s understanding may matter.', 'warn') +
    note('MESA will not pressure the team either way. But she will ask, once, before the report is filed: <em>"Are you going to tell them about her?"</em>'),
    open=False
) + npc_card_close()


# ══════════════════════════════════════════════════════════════════════════════
# SESSION 09 — Still Life with Teeth / KBO 2119-HR4
# ══════════════════════════════════════════════════════════════════════════════

S09_SEMAPHORE = section_label('THE SEMAPHORE — WHAT SHE WAS POINTING AT') + npc_card_open() + collapse_entry(
    'FOUR ARMS — THE CONVERGENCE',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.6rem;">
          Sauelsuesor currently has four limbs extended into the outer system. The team has now been to the locations corresponding to three of them: Gutenberg Station, FK7-class Kuiper coordinates, Arrokoth. The fourth arm has been pointing here — KBO 2119-HR4 — for longer than any of the others. Outer-system observer logs date its first appearance to nineteen months before the team's arrival. She was pointing at the Lithohex before it hatched.
        </div>''' +
    note('<strong style="color:var(--signal)">THE IMPLICATION:</strong> The Lithohex is not an accident. It is not bad luck that the research team cracked the rock and the predator emerged. Something that can see across the solar system from near the sun saw this object nineteen months ago and knew what was inside it. The Semaphore cannot intervene. She cannot travel. She cannot speak to anyone with sufficient authority or reach to act. All she can do is point. She has been pointing at this specific piece of frozen rock for a year and a half, and the first people to get close enough to understand why just docked.') +
    test_item('MESA — ON ARRIVAL', '<em>"The fourth arm. This is it."</em> She does not elaborate immediately. She processes the hull of KBO 2119-HR4 on optical scan, the glass spikes, the emergency beacon. Then: <em>"She saw it before it was dangerous. Before the rock was opened. She was pointing at what it would become. I think she knew it would hatch. I think she\'s been trying to get someone here before that happened for nineteen months."</em> A long pause. <em>"We\'re late."</em>', 'signal') +
    test_item('KNOW: ASTROBIOLOGY / KNOW: TITAN TECH', 'The Semaphore\'s detection method is unknown, but her track record across the campaign suggests sensitivity to potential X-risks at extreme range — things that are not yet dangerous but will become so. The Lithohex as it existed inside the KBO was dormant, inert, and completely undetectable by any transhumanist instrument. She pointed at it anyway. Whatever she senses, it is not a current threat signature. It is a future one.', 'warn'),
    open=False
) + collapse_entry(
    'THE TIP UNIT — WHAT SHE COULD NOT DO',
    '''
        <div style="font-size:0.85rem; color:var(--muted); line-height:1.5; margin-bottom:0.5rem;">
          The Temporal Isolation Protocol unit is the campaign's final convergence point. The Semaphore has been pointing at this location for nineteen months. She cannot act — she can only indicate. The team is the action she pointed toward. The TIP unit is the tool. This is the scenario she was hoping for when she extended that arm.
        </div>''' +
    note('<strong style="color:var(--textbright)">FOR THE GM:</strong> You do not need to make this explicit. The players may put it together themselves — or they may not until after the session, in debrief, when someone says "wait, was the whole campaign her trying to get us out here in time?" That realisation landing late is better than you explaining it. The thread was always there. They followed it. They were the warning she sent.', 'signal') +
    note('If MESA is present for the TIP decision and the team understands the Semaphore thread: <em>"Whatever happens here — she saw it. She\'s been watching. I find I want to get this right. For her sake, as much as ours."</em>'),
    open=False
) + npc_card_close()


# ══════════════════════════════════════════════════════════════════════════════
# INJECTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════

SESSIONS = [
    ('session-05-cold-station.html',       S05_SEMAPHORE, '</div><!-- /left-col -->'),
    ('session-06-signal-zero.html',        S06_SEMAPHORE, '<button class="print-btn expand"'),
    ('session-07-cry-for-help.html',       S07_SEMAPHORE, '</div><!-- /col -->'),
    ('session-08-requiem-for-orcus.html',  S08_SEMAPHORE, '</div><!-- /col -->'),
    ('session-09-still-life-with-teeth.html', S09_SEMAPHORE, '</div><!-- end right-col -->'),
]

print('Injecting Semaphore thread...')
for fname, content, anchor in SESSIONS:
    path = Path(f'/home/claude/{fname}')
    html = path.read_text()

    # Idempotency — skip if already injected
    if 'THE SEMAPHORE' in html:
        print(f'  SKIP (already injected): {fname}')
        continue

    if anchor not in html:
        print(f'  WARNING: anchor not found in {fname}: {repr(anchor[:40])}')
        # Try footer as fallback
        anchor = '<footer class="ep-legal-footer">'
        if anchor not in html:
            print(f'  ERROR: fallback anchor also missing, skipping')
            continue

    html = html.replace(anchor, content + '\n' + anchor, 1)
    path.write_text(html)
    print(f'  OK: {fname}')

print('Done.')
