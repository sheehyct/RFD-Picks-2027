#!/usr/bin/env python3
"""Build personal.html: a copy of index.html with calendar holidays added.

index.html is a generated bundle, so this patches the page template inside it
rather than editing by hand. Run from the repo root after index.html changes:

    python3 tools/build-personal.py

Every patch must match exactly once; if index.html changed shape the script
stops with the name of the patch that no longer fits.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_LINE = '  <script type="__bundler/template">'

# 2027 calendar holidays, keyed MM-DD. 'F' = federal holiday, 'O' = other.
# Edit this list to taste and rebuild.
HOLIDAYS = [
    ("01-01", "F", "New Year's Day"),
    ("01-18", "F", "Martin Luther King Jr. Day"),
    ("02-14", "O", "Valentine's Day"),
    ("02-15", "F", "Presidents' Day"),
    ("03-28", "O", "Easter"),
    ("05-09", "O", "Mother's Day"),
    ("05-31", "F", "Memorial Day"),
    ("06-19", "F", "Juneteenth"),
    ("06-20", "O", "Father's Day"),
    ("07-04", "F", "Independence Day"),
    ("09-06", "F", "Labor Day"),
    ("10-11", "F", "Columbus Day"),
    ("10-31", "O", "Halloween"),
    ("11-11", "F", "Veterans Day"),
    ("11-25", "F", "Thanksgiving"),
    ("12-24", "O", "Christmas Eve"),
    ("12-25", "F", "Christmas Day"),
    ("12-31", "O", "New Year's Eve"),
]

HOL_JS = "  HOL = " + json.dumps({k: [t, n] for k, t, n in HOLIDAYS}) + ";\n"

# (name, old, new) applied to the page template.
PATCHES = [
    ("title",
     "<title>RFD 2027 Pick Planner</title>",
     "<title>RFD 2027 Pick Planner (Personal)</title>"),
    ("home-screen name",
     'name="apple-mobile-web-app-title" content="Picks 2027"',
     'name="apple-mobile-web-app-title" content="My Picks 2027"'),
    ("manifest link",
     "link('manifest', 'manifest.webmanifest')",
     "link('manifest', 'personal.webmanifest')"),
    ("holiday data",
     "  KEY = 'rfd-pick-planner-2027-v1';\n",
     HOL_JS + "  KEY = 'rfd-pick-planner-2027-v1';\n"),
    # Star next to the day number.
    ("cell markup",
     """<span style="font-family:'Barlow Condensed',sans-serif;font-size:15px;font-weight:{{ d.weight }}">{{ d.day }}</span>""",
     """<span style="display:flex;align-items:flex-start;gap:1px"><span style="font-family:'Barlow Condensed',sans-serif;font-size:15px;font-weight:{{ d.weight }}">{{ d.day }}</span><span style="font-size:10px;line-height:1.1">{{ d.hol }}</span></span>"""),
    ("cell values",
     "day: d, letter: showLetters ? letter : '', bg,",
     "day: d, hol: H ? (H[0] === 'F' ? '★' : '☆') : '', letter: showLetters ? letter : '', bg,"),
    ("cell lookup",
     "const k = this.key(m, d), duty = letter === shift,",
     "const k = this.key(m, d), H = this.HOL[k], duty = letter === shift,"),
    ("cell tooltip",
     "title: this.fmt(k) + ' · ' + letter + ' shift' +",
     "title: this.fmt(k) + (H ? ' · ' + H[1] : '') + ' · ' + letter + ' shift' +"),
    ("blank cell",
     "const blank = { day: '', letter: '',",
     "const blank = { day: '', hol: '', letter: '',"),
    # Holiday list under each month.
    ("month values",
     "name: this.MN[m], duty: s.split('').filter(c => c === shift).length,",
     "name: this.MN[m], duty: s.split('').filter(c => c === shift).length,\n"
     "        hols: Object.keys(this.HOL).filter(k => +k.slice(0, 2) === m + 1).sort().map(k => {\n"
     "          const d = +k.slice(3), l = s[d - 1], on = l === shift, H = this.HOL[k];\n"
     "          return { mark: H[0] === 'F' ? '★' : '☆', when: this.WD[new Date(2027, m, d).getDay()] + ' ' + d, name: H[1],\n"
     "            who: on ? 'On duty' : l + ' shift', fg: on ? INK : '#55534f', weight: on ? 700 : 400 };\n"
     "        }),"),
    ("month markup",
     """              </sc-for>
            </div>
          </section>""",
     """              </sc-for>
            </div>
            <div style="margin-top:8px;font-size:12px;line-height:1.5">
              <sc-for list="{{ m.hols }}" as="h" hint-placeholder-count="0">
                <div style="display:flex;gap:6px;color:{{ h.fg }};font-weight:{{ h.weight }}">
                  <span style="flex:none;width:12px">{{ h.mark }}</span>
                  <span style="flex:none;width:44px;font-variant-numeric:tabular-nums">{{ h.when }}</span>
                  <span style="flex:1;min-width:0">{{ h.name }}</span>
                  <span style="flex:none">{{ h.who }}</span>
                </div>
              </sc-for>
            </div>
          </section>"""),
    ("legend",
     "Mandatory OT (your group)</span>\n",
     "Mandatory OT (your group)</span>\n"
     """        <span style="display:flex;align-items:center;gap:6px"><span style="font-size:14px;color:#1b2230">★</span>Federal holiday</span>\n"""
     """        <span style="display:flex;align-items:center;gap:6px"><span style="font-size:14px;color:#1b2230">☆</span>Other holiday</span>\n"""),
    ("footer",
     "Enter approved leave in ESO. <a",
     "Enter approved leave in ESO. Personal version with calendar holidays. <a"),
]


def main():
    lines = (ROOT / "index.html").read_text(encoding="utf-8").split("\n")
    at = lines.index(TEMPLATE_LINE) + 1
    template = json.loads(lines[at])

    for name, old, new in PATCHES:
        if template.count(old) != 1:
            raise SystemExit(f"patch '{name}' matched {template.count(old)} times, expected 1")
        template = template.replace(old, new)

    lines[at] = json.dumps(template).replace("</", "<\\u002F")
    html = "\n".join(lines)
    outer = "<title>RFD 2027 Pick Planner</title>"
    if html.count(outer) != 1:
        raise SystemExit("outer <title> not found")
    html = html.replace(outer, "<title>RFD 2027 Pick Planner (Personal)</title>")
    (ROOT / "personal.html").write_text(html, encoding="utf-8")

    manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    manifest.update(id="personal.html", start_url="personal.html",
                    name="RFD 2027 Pick Planner (Personal)", short_name="My Picks 2027")
    (ROOT / "personal.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("wrote personal.html and personal.webmanifest")


if __name__ == "__main__":
    main()
