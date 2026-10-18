#!/usr/bin/env python3
"""Generates the animated sci-fi SVGs in assets/ used by README.md.

Icon tiles come from skillicons.dev (MIT); pass the folder they were downloaded
into as the first argument, e.g.  python3 scripts/build_assets.py /tmp/icons
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
ICONS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "scripts", "icons")

BG = "#05070d"
PANEL = "#0a0f1c"
CYAN = "#00f0ff"
MAGENTA = "#ff2bd6"
VIOLET = "#8b5cf6"
LIME = "#39ff88"
DIM = "#5b6b8c"
TEXT = "#c9d1d9"

SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def write(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg.strip() + "\n")
    print("wrote", name, len(svg), "bytes")


def corner_brackets(x, y, w, h, size=22, color=CYAN, width=2.5):
    p = []
    for cx, cy, dx, dy in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        p.append(f"M{cx + dx * size},{cy} H{cx} V{cy + dy * size}")
    return f'<path d="{" ".join(p)}" fill="none" stroke="{color}" stroke-width="{width}"/>'


# ---------------------------------------------------------------- header ----
def header():
    W, H = 1200, 360
    horizon = 250
    vx = W / 2
    # perspective floor: radiating verticals + horizontal lines flowing toward the viewer
    verticals = "".join(
        f'<line x1="{vx + i * 18}" y1="{horizon}" x2="{vx + i * 140}" y2="{H}"/>' for i in range(-12, 13)
    )
    flowing = "".join(
        f'<line x1="0" x2="{W}" y1="{horizon}" y2="{horizon}">'
        f'<animate attributeName="y1" values="{horizon};{H}" dur="3s" begin="{-i * 0.5}s" repeatCount="indefinite" calcMode="spline" keySplines="0.55 0 1 0.45"/>'
        f'<animate attributeName="y2" values="{horizon};{H}" dur="3s" begin="{-i * 0.5}s" repeatCount="indefinite" calcMode="spline" keySplines="0.55 0 1 0.45"/>'
        f'<animate attributeName="stroke-opacity" values="0;1" dur="3s" begin="{-i * 0.5}s" repeatCount="indefinite"/>'
        f"</line>"
        for i in range(6)
    )
    # deterministic star field
    stars = []
    seed = 7
    for i in range(70):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        x = seed % W
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        y = seed % (horizon - 20)
        r = 0.6 + (i % 3) * 0.5
        d = 2 + (i % 5)
        stars.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" style="animation:twinkle {d}s ease-in-out {-(i % 7) * 0.6}s infinite"/>'
        )
    stars = "".join(stars)

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Mashrur Ahmed, Game Developer">
<title>MASHRUR AHMED // GAME DEVELOPER</title>
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#03040a"/><stop offset="0.62" stop-color="#0b0b2a"/><stop offset="0.7" stop-color="#1a0b33"/><stop offset="1" stop-color="{BG}"/>
  </linearGradient>
  <linearGradient id="name" x1="0" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.35" stop-color="{VIOLET}"/><stop offset="0.65" stop-color="{MAGENTA}"/><stop offset="1" stop-color="{CYAN}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1200 0;0 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="floorFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.25" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="floorMask"><rect x="0" y="{horizon}" width="{W}" height="{H - horizon}" fill="url(#floorFade)"/></mask>
  <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{MAGENTA}" stop-opacity="0.55"/><stop offset="0.6" stop-color="{VIOLET}" stop-opacity="0.15"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0.18"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softglow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="sliceA"><rect x="0" y="118" width="{W}" height="16"><animate attributeName="y" values="118;150;96;170;118" dur="0.6s" repeatCount="indefinite"/></rect></clipPath>
  <clipPath id="sliceB"><rect x="0" y="160" width="{W}" height="10"><animate attributeName="y" values="160;108;176;130;160" dur="0.5s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<style>
  @keyframes twinkle {{ 0%,100% {{ opacity:.15 }} 50% {{ opacity:1 }} }}
  @keyframes glitch {{ 0%,90%,100% {{ opacity:0 }} 91%,94% {{ opacity:1; transform:translateX(-6px) }} 92%,96% {{ opacity:1; transform:translateX(5px) }} }}
  @keyframes blink {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.15 }} }}
  @keyframes spin {{ to {{ transform:rotate(360deg) }} }}
  @keyframes spinr {{ to {{ transform:rotate(-360deg) }} }}
  @keyframes sweep {{ 0% {{ transform:translateY(-120px) }} 100% {{ transform:translateY({H}px) }} }}
  @keyframes rise {{ 0% {{ opacity:0; transform:translateY(14px) }} 100% {{ opacity:1; transform:translateY(0) }} }}
  @keyframes dash {{ to {{ stroke-dashoffset:-400 }} }}
  .glA {{ animation:glitch 5s steps(1) infinite; }}
  .glB {{ animation:glitch 5s steps(1) .12s infinite; }}
  .blink {{ animation:blink 1.4s ease-in-out infinite; }}
  .ring1 {{ transform-origin:150px 130px; animation:spin 18s linear infinite; }}
  .ring2 {{ transform-origin:150px 130px; animation:spinr 11s linear infinite; }}
  .ring3 {{ transform-origin:1050px 130px; animation:spinr 22s linear infinite; }}
  .ring4 {{ transform-origin:1050px 130px; animation:spin 9s linear infinite; }}
  .scan {{ animation:sweep 5s linear infinite; }}
  .sub {{ opacity:0; animation:rise .8s ease-out .5s forwards; }}
  .tags {{ opacity:0; animation:rise .8s ease-out 1s forwards; }}
  .trace {{ stroke-dasharray:6 14; animation:dash 6s linear infinite; }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars}
  <circle cx="{vx}" cy="{horizon}" r="210" fill="url(#sun)"/>
  <g stroke="{MAGENTA}" stroke-opacity="0.55" stroke-width="1.2" mask="url(#floorMask)">{verticals}</g>
  <g stroke="{CYAN}" stroke-width="1.2" mask="url(#floorMask)">{flowing}</g>
  <line x1="0" y1="{horizon}" x2="{W}" y2="{horizon}" stroke="{MAGENTA}" stroke-width="2" filter="url(#softglow)"/>

  <!-- HUD reticles -->
  <g fill="none" stroke="{CYAN}" stroke-opacity="0.45">
    <circle class="ring1" cx="150" cy="130" r="70" stroke-width="2" stroke-dasharray="40 12 4 12"/>
    <circle class="ring2" cx="150" cy="130" r="54" stroke-width="1" stroke-dasharray="2 6"/>
    <path class="ring2" d="M150 48 V64 M150 196 V212 M68 130 H84 M216 130 H232" stroke-width="2"/>
  </g>
  <g fill="none" stroke="{MAGENTA}" stroke-opacity="0.45">
    <circle class="ring3" cx="1050" cy="130" r="70" stroke-width="2" stroke-dasharray="90 20 10 20"/>
    <circle class="ring4" cx="1050" cy="130" r="50" stroke-width="1.5" stroke-dasharray="12 8"/>
    <circle cx="1050" cy="130" r="4" fill="{MAGENTA}" class="blink"/>
  </g>
  <text x="150" y="226" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{CYAN}" fill-opacity="0.7" letter-spacing="2">LOCK://ENGINE</text>
  <text x="1050" y="226" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MAGENTA}" fill-opacity="0.7" letter-spacing="2">TGT://PLAYER_1</text>

  <!-- top status bar -->
  <g font-family="{MONO}" font-size="12" letter-spacing="2" fill="{DIM}">
    <text x="34" y="34">SYS://MASHRUR_AHMED.EXE</text>
    <text x="{W / 2}" y="34" text-anchor="middle">CLASS: GAME_DEVELOPER</text>
    <text x="{W - 34}" y="34" text-anchor="end">STATUS: <tspan fill="{LIME}">ONLINE</tspan></text>
  </g>
  <circle cx="{W - 140}" cy="30" r="4" fill="{LIME}" class="blink"/>
  <line x1="34" y1="46" x2="{W - 34}" y2="46" stroke="{CYAN}" stroke-opacity="0.35" class="trace"/>

  <!-- name with glitch slices -->
  <g font-family="{SANS}" font-weight="800" font-size="76" letter-spacing="10" text-anchor="middle">
    <text x="{W / 2}" y="160" fill="url(#name)" filter="url(#glow)">MASHRUR AHMED</text>
    <text x="{W / 2}" y="160" fill="{CYAN}" clip-path="url(#sliceA)" class="glA">MASHRUR AHMED</text>
    <text x="{W / 2}" y="160" fill="{MAGENTA}" clip-path="url(#sliceB)" class="glB">MASHRUR AHMED</text>
  </g>
  <g class="sub">
    <text x="{W / 2}" y="200" text-anchor="middle" font-family="{MONO}" font-size="20" letter-spacing="8" fill="{TEXT}">[ GAME DEVELOPER ]</text>
  </g>
  <g class="tags" font-family="{MONO}" font-size="14" letter-spacing="4" text-anchor="middle">
    <text x="{W / 2}" y="232"><tspan fill="{CYAN}">UNITY</tspan><tspan fill="{DIM}">  //  </tspan><tspan fill="{VIOLET}">UNREAL</tspan><tspan fill="{DIM}">  //  </tspan><tspan fill="{MAGENTA}">ROBLOX</tspan><tspan fill="{DIM}">  //  </tspan><tspan fill="{LIME}">GODOT</tspan></text>
  </g>

  <rect class="scan" x="0" y="0" width="{W}" height="120" fill="url(#scan)"/>
  {corner_brackets(14, 14, W - 28, H - 28, 30, CYAN, 3)}
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="{CYAN}" stroke-opacity="0.25"/>
</svg>
"""


# -------------------------------------------------------------- terminal ----
def terminal():
    W = 1200
    lines = [
        [("$ ", LIME), ("./boot --profile mashrur", TEXT)],
        [("[ OK ] ", LIME), ("Loading class module ........ ", DIM), ("GAME_DEVELOPER.sys", CYAN)],
        [("[ OK ] ", LIME), ("Engines online ............. ", DIM), ("Unity · Unreal · Roblox Studio · Godot", TEXT)],
        [("[ OK ] ", LIME), ("Languages linked ........... ", DIM), ("C# · C++ · Luau · Python · JS", TEXT)],
        [("[ OK ] ", LIME), ("Build targets .............. ", DIM), ("Android · iOS · PC · WebGL", TEXT)],
        [("[ OK ] ", LIME), ("Multiplayer netcode ........ ", DIM), ("synced", MAGENTA)],
        [("> ", MAGENTA), ("Building worlds people actually want to play in.", CYAN)],
    ]
    fs, cw, lh = 17, 10.25, 30  # monospace advance ≈ 0.6em
    top, left = 78, 36
    H = top + len(lines) * lh + 30
    T = 14.0  # loop length (s)
    t = 0.4
    pieces, styles = [], []
    for i, segs in enumerate(lines):
        n = sum(len(s) for s, _ in segs)
        dur = max(0.35, n * 0.028) if i in (0, len(lines) - 1) else 0.45
        start, end = t, t + dur
        t = end + (0.5 if i == 0 else 0.22)
        a, b = start / T * 100, end / T * 100
        y = top + i * lh
        width = n * cw + 24
        tsp = "".join(f'<tspan fill="{c}">{s.replace("&", "&amp;")}</tspan>' for s, c in segs)
        pieces.append(
            f'<text x="{left}" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">{tsp}</text>'
            f'<rect class="c{i}" x="{left - 4}" y="{y - fs}" width="{width}" height="{lh}" fill="{PANEL}"/>'
        )
        steps = max(1, n // 2)
        styles.append(
            f"@keyframes k{i} {{ 0%,{a:.2f}% {{ transform:translateX(0) }} {b:.2f}%,100% {{ transform:translateX({width:.0f}px) }} }}"
            f".c{i} {{ animation:k{i} {T}s steps({steps}) infinite; }}"
        )
    last_y = top + (len(lines) - 1) * lh
    last_w = sum(len(s) for s, _ in lines[-1]) * cw
    cursor_on = t / T * 100
    styles.append(
        f"@keyframes cur {{ 0%,{cursor_on:.2f}% {{ opacity:0 }} {cursor_on + 0.01:.2f}%,100% {{ opacity:1 }} }}"
        f"@keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}"
        f"@keyframes fade {{ 0%,94% {{ opacity:1 }} 97% {{ opacity:0 }} 100% {{ opacity:1 }} }}"
        f".cursor {{ animation:cur {T}s linear infinite; }} .cursor rect {{ animation:blink 1s steps(1) infinite; }}"
        f".body {{ animation:fade {T}s linear infinite; }}"
        f"@keyframes dash {{ to {{ stroke-dashoffset:-300 }} }} .trace {{ stroke-dasharray:4 10; animation:dash 8s linear infinite; }}"
    )
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Boot sequence: Unity, Unreal, Roblox Studio and Godot game developer">
<title>boot --profile mashrur</title>
<style>{"".join(styles)}</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{PANEL}" stroke="{CYAN}" stroke-opacity="0.35"/>
<rect x="1" y="1" width="{W - 2}" height="40" rx="14" fill="#0e1528"/>
<rect x="1" y="28" width="{W - 2}" height="13" fill="#0e1528"/>
<line x1="1" y1="41" x2="{W - 1}" y2="41" stroke="{CYAN}" stroke-opacity="0.35" class="trace"/>
<circle cx="26" cy="21" r="6" fill="#ff5f57"/><circle cx="46" cy="21" r="6" fill="#febc2e"/><circle cx="66" cy="21" r="6" fill="#28c840"/>
<text x="{W / 2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{DIM}" letter-spacing="1">mashrur@forge: ~/worlds — zsh</text>
<text x="{W - 24}" y="26" text-anchor="end" font-family="{MONO}" font-size="12" fill="{CYAN}" fill-opacity="0.7">● LIVE</text>
<g class="body">
{"".join(pieces)}
<g class="cursor"><rect x="{left + last_w + 4}" y="{last_y - fs + 2}" width="10" height="{fs + 2}" fill="{CYAN}"/></g>
</g>
{corner_brackets(8, 8, W - 16, H - 16, 16, MAGENTA, 2)}
</svg>
"""


# --------------------------------------------------------- section titles ---
def section(num, title, tag):
    W, H = 1200, 64
    tw = len(title) * 17.5 + 4  # rough width of the title at 26px w/ spacing
    x0 = 112 + tw + 20
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title.replace('_', ' ').title()}">
<title>{num} // {title}</title>
<defs>
  <linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0.1"/></linearGradient>
  <filter id="g" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  @keyframes run {{ 0% {{ transform:translateX(0); opacity:0 }} 10% {{ opacity:1 }} 90% {{ opacity:1 }} 100% {{ transform:translateX({W - 150 - x0}px); opacity:0 }} }}
  @keyframes blink {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.2 }} }}
  @keyframes in {{ from {{ opacity:0; transform:translateX(-12px) }} to {{ opacity:1; transform:translateX(0) }} }}
  .pulse {{ animation:run 3.2s cubic-bezier(.6,0,.4,1) infinite; }}
  .blink {{ animation:blink 1.2s ease-in-out infinite; }}
  .in {{ animation:in .7s ease-out both; }}
</style>
<g class="in">
  <path d="M8 14 L40 14 L56 32 L40 50 L8 50 L24 32 Z" fill="{MAGENTA}" fill-opacity="0.15" stroke="{MAGENTA}" stroke-width="1.5"/>
  <text x="32" y="38" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{MAGENTA}">{num}</text>
  <text x="72" y="41" font-family="{MONO}" font-size="20" fill="{DIM}">//</text>
  <text x="112" y="42" font-family="{SANS}" font-size="26" font-weight="800" letter-spacing="3" fill="{CYAN}" filter="url(#g)">{title}</text>
</g>
<line x1="{x0}" y1="32" x2="{W - 140}" y2="32" stroke="url(#ln)" stroke-width="1.5"/>
<circle class="pulse" cx="{x0}" cy="32" r="3.5" fill="{CYAN}" filter="url(#g)"/>
<text x="{W - 8}" y="37" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{LIME}" class="blink">[ {tag} ]</text>
</svg>
"""


# --------------------------------------------------------------- loadout ----
ROBLOX_TILE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
    '<rect width="256" height="256" fill="#242938" rx="60"/>'
    '<g transform="rotate(-15 128 128)"><path fill="#FFFFFF" fill-rule="evenodd" '
    'd="M58 58 H198 V198 H58 Z M106 106 V150 H150 V106 Z"/></g></svg>'
)


def load_icon(name, uid):
    if name == "roblox":
        inner = ROBLOX_TILE
    else:
        raw = open(os.path.join(ICONS, f"{name}.svg")).read()
        m = re.search(r"<g[^>]*>\s*(<svg.*</svg>)\s*</g>", raw, re.S)
        inner = m.group(1)
    # namespace ids so gradients from different tiles never collide
    inner = re.sub(r'id="([^"]+)"', lambda m: f'id="{uid}-{m.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{uid}-{m.group(1)})", inner)
    inner = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{uid}-{m.group(1)}"', inner)
    return inner


def loadout():
    rows = [
        ("ENGINES", "primary", CYAN, [("unity", "Unity"), ("unreal", "Unreal"), ("roblox", "Roblox"), ("godot", "Godot")]),
        ("CODE", "linked", VIOLET, [("cs", "C#"), ("cpp", "C++"), ("lua", "Luau"), ("py", "Python"), ("java", "Java"),
                                     ("js", "JS"), ("html", "HTML"), ("css", "CSS")]),
        ("TOOLS", "equipped", MAGENTA, [("blender", "Blender"), ("ps", "Photoshop"), ("figma", "Figma"), ("visualstudio", "VS"),
                                        ("vscode", "VS Code"), ("git", "Git"), ("github", "GitHub"), ("firebase", "Firebase")]),
        ("TARGETS", "deploy", LIME, [("androidstudio", "Android"), ("apple", "iOS"), ("windows", "PC"), ("html", "WebGL")]),
    ]
    W = 1200
    icon, step, rowh, labelw, top = 60, 108, 118, 230, 36
    H = top + len(rows) * rowh + 14
    body, styles = [], []
    k = 0
    for r, (cat, sub, color, items) in enumerate(rows):
        y = top + r * rowh
        body.append(
            f'<g transform="translate(36 {y + 18})">'
            f'<rect width="4" height="44" fill="{color}"/>'
            f'<text x="18" y="20" font-family="{SANS}" font-size="20" font-weight="800" letter-spacing="4" fill="{color}">{cat}</text>'
            f'<text x="18" y="42" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{DIM}">STATUS: {sub.upper()}</text>'
            f"</g>"
        )
        for j, (name, label) in enumerate(items):
            x = labelw + j * step
            delay = 0.15 + k * 0.06
            k += 1
            frame = corner_brackets(x - 8, y - 2, icon + 16, icon + 16, 10, color, 1.5) if r == 0 else ""
            body.append(
                f'<g class="tile" style="animation-delay:{delay:.2f}s">'
                f"{frame}"
                f'<svg x="{x}" y="{y + 6}" width="{icon}" height="{icon}" viewBox="0 0 256 256">{load_icon(name, f"i{k}")}</svg>'
                f'<text x="{x + icon / 2}" y="{y + icon + 34}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{TEXT}" letter-spacing="1">{label}</text>'
                f"</g>"
            )
        if r < len(rows) - 1:
            body.append(f'<line x1="36" x2="{W - 36}" y1="{y + rowh - 4}" y2="{y + rowh - 4}" stroke="{DIM}" stroke-opacity="0.25" stroke-dasharray="2 6"/>')
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech loadout: Unity, Unreal, Roblox, Godot, C#, C++, Luau, Python, Java, JavaScript, Blender, Photoshop, Figma, Git, Firebase">
<title>LOADOUT</title>
<defs>
  <linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}" stop-opacity="0.12"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0 H0 V24" fill="none" stroke="{CYAN}" stroke-opacity="0.05"/></pattern>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<style>
  @keyframes pop {{ from {{ opacity:0; transform:translateY(10px) }} to {{ opacity:1; transform:translateY(0) }} }}
  @keyframes sweep {{ from {{ transform:translateX(-300px) }} to {{ transform:translateX({W + 300}px) }} }}
  .tile {{ opacity:0; animation:pop .5s ease-out forwards; }}
  .sweep {{ animation:sweep 4.5s linear infinite; }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{PANEL}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  {"".join(body)}
  <rect class="sweep" x="0" y="0" width="260" height="{H}" fill="url(#sw)"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{CYAN}" stroke-opacity="0.3"/>
{corner_brackets(8, 8, W - 16, H - 16, 18, CYAN, 2)}
</svg>
"""


# ---------------------------------------------------------------- footer ----
def footer():
    W, H = 1200, 120
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="End of transmission">
<title>END OF TRANSMISSION</title>
<defs>
  <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{MAGENTA}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/></linearGradient>
  <filter id="g" x="-20%" y="-100%" width="140%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  @keyframes wave {{ 0%,100% {{ transform:scaleY(.25) }} 50% {{ transform:scaleY(1) }} }}
  @keyframes blink {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.25 }} }}
  .bar {{ transform-box:fill-box; transform-origin:center; animation:wave 1.2s ease-in-out infinite; }}
  .blink {{ animation:blink 1.6s ease-in-out infinite; }}
</style>
<line x1="60" y1="30" x2="{W - 60}" y2="30" stroke="url(#l)" stroke-width="2" filter="url(#g)"/>
<g fill="{CYAN}">{"".join(f'<rect class="bar" x="{W / 2 - 120 + i * 10}" y="44" width="5" height="30" rx="2" style="animation-delay:{-((i * 37) % 11) / 10:.1f}s;fill:{CYAN if i % 3 else MAGENTA}"/>' for i in range(24))}</g>
<text x="{W / 2}" y="104" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="6" fill="{DIM}" class="blink">END OF TRANSMISSION</text>
</svg>
"""


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write("header.svg", header())
    write("terminal.svg", terminal())
    write("loadout.svg", loadout())
    write("footer.svg", footer())
    for num, title, tag, fname in [
        ("01", "MISSION_LOG", "ACTIVE", "sec-about.svg"),
        ("02", "DEPLOYED_PROJECTS", "LIVE", "sec-projects.svg"),
        ("03", "LOADOUT", "EQUIPPED", "sec-loadout.svg"),
        ("04", "TELEMETRY", "STREAMING", "sec-telemetry.svg"),
        ("05", "UPLINK", "OPEN", "sec-uplink.svg"),
    ]:
        write(fname, section(num, title, tag))
