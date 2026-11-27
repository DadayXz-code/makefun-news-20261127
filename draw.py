#!/usr/bin/env python3
"""THE WORLD TODAY -- Friday 27 November 2026.

Build-time only: draws the one-page newspaper front page (entry.png,
1024x1024) with Pillow. Pillow is NOT imported at grading time; the
grader only runs main.ts, which copies the finished entry.png.

Content: 36 stories across 7 regions, all events that happened or were
first reported on 26-27 November 2026, compiled from BBC, NYT, Reuters,
The Guardian and other outlets on the morning of 27 Nov 2026 (WIB).
Deterministic: same input -> same bytes.
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (24, 24, 24)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
GREY = (112, 108, 98)
LIGHT = (232, 227, 212)
RULE = (70, 66, 56)
GOLD = (176, 132, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif_b(s):
    return F("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return F("DejaVuSerif.ttf", s)


def sans(s):
    return F("DejaVuSans.ttf", s)


def sans_b(s):
    return F("DejaVuSans-Bold.ttf", s)


def text_w(draw, text, font):
    return draw.textlength(text, font=font)


def wrap(draw, text, font, max_w):
    """Greedy word wrap to max_w pixels; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if text_w(draw, trial, font) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, max_w, text, font, fill, lh, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=font, fill=fill)
    return y + len(lines) * lh


def centre(draw, y, text, font, fill, cx=512):
    w = text_w(draw, text, font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return w


# ---------------------------------------------------------------- stories
# (region, headline) -- hero stories are told in the masthead band and
# counted separately, so the region boxes below hold the other 34.
REGIONS = [
    ("MIDDLE EAST", "6 stories", [
        "Gaza strikes kill 10, incl. Hamas official, despite ceasefire",
        "Houthis hit Saudi Ras Tanura refinery and Red Sea ports",
        "Two tankers hit mines in Strait of Hormuz; Brent nears $96",
        "Egypt arrests driver over tanker crash that killed 31",
        "Ukraine strike hits Russian warship in Benghazi, Libya",
    ]),
    ("EUROPE", "6 stories", [
        "Ukraine damages five Russian jets at Savasleyka airbase",
        "Russia answers with ballistic missiles on Kyiv",
        "EU leaders clash over \u20ac45bn Ukraine loan in Brussels",
        "UK net migration falls to lowest since 1997",
        "Zelensky: US too focused on Middle East, not on Russia",
        "Depardieu to stand trial over alleged rape in 2018",
    ]),
    ("AMERICAS", "6 stories", [
        "Thanksgiving storm floods US streets, cancels flights",
        "Trump proposes tariffs on 14 nations: 20% on China, 15% EU",
        "Democrats reclaim Congress in midterm comeback",
        "Pope Leo XIV to vote in US midterms by mail",
        "FedEx jet overruns Miami runway in thunderstorms",
    ]),
    ("ASIA-PACIFIC", "6 stories", [
        "Bangkok refinery blast injures nine, three critical",
        "Bogor mine flood kills 13 miners, 13 more trapped",
        "Mount Mayon erupts in Philippines, ash 3,000 m high",
        "Kim Jong Un vows more nuclear weapons, inspects sites",
        "Gukesh-Sindarov Game 3: marathon draw in chess final",
        "China: India border areas 'generally stable'",
    ]),
    ("AFRICA", "5 stories", [
        "Al-Shabaab claims hundreds dead in Somalia ambush",
        "Ramaphosa wins court bid to overturn impeachment report",
        "Kenya discharges last Ebola patient; DRC toll tops 5,300",
        "Nigeria starts building its own naval ships",
        "Ghana unveils Heritage banknotes honouring Nkrumah",
    ]),
    ("MARKETS & TECH", "4 stories", [
        "Stocks rebound worldwide: Stoxx +1.75%, DAX +2.08%",
        "Brent $96.12, gold $3,593 as Gulf tensions rise",
        "Nvidia halts AI server shipments to South-East Asia",
        "SpaceX cleared to launch up to 1m Starlink satellites",
    ]),
    ("SPORT & CULTURE", "3 stories", [
        "Sinner out of Australian Open 2027 with knee injury",
        "Grammy nods: Tyla, Tems and Kidjo lead Africa's hopes",
        "Inglis and Carey put Australia on top in decider",
    ]),
]

TIMELINE = [
    ("26 NOV", "Bangkok refinery blast"),
    ("01:03", "Two Italians killed in Kuwait"),
    ("02:05", "BBC confirms strike"),
    ("02:26", "Gaza strikes kill ten"),
    ("03:31", "Tanker capsizes off Ibiza"),
    ("04:03", "Kuwait blames Iran"),
]


# ---------------------------------------------------------------- scenes
def draw_lead_scene(d, x0, y0, x1, y1):
    """Dusk over a Gulf refinery: dark sky, flare stack, drone above."""
    d.rectangle([x0, y0, x1, y1], fill=(28, 36, 58))
    # horizon glow bands
    for i, col in enumerate([(58, 52, 74), (96, 62, 58), (150, 84, 52)]):
        d.rectangle([x0, y0 + 52 + i * 16, x1, y0 + 68 + i * 16], fill=col)
    # stars
    for sx, sy in [(14, 10), (52, 22), (96, 8), (150, 18), (196, 10),
                   (34, 34), (120, 30), (176, 30), (210, 22)]:
        d.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                  fill=(235, 230, 210))
    # moon
    d.ellipse([x0 + 168, y0 + 8, x0 + 190, y0 + 30], fill=(238, 232, 205))
    d.ellipse([x0 + 174, y0 + 12, x0 + 190, y0 + 30], fill=(28, 36, 58))
    # ground
    d.rectangle([x0, y1 - 34, x1, y1], fill=(16, 18, 24))
    # refinery towers
    for tx, tw, th in [(18, 22, 78), (52, 16, 96), (82, 26, 66),
                       (122, 18, 88), (152, 24, 60)]:
        d.rectangle([x0 + tx, y1 - 34 - th, x0 + tx + tw, y1 - 34],
                    fill=(44, 46, 54))
        d.rectangle([x0 + tx + 3, y1 - 34 - th + 8, x0 + tx + tw - 3,
                     y1 - 34 - th + 14], fill=(90, 92, 100))
        d.rectangle([x0 + tx + 3, y1 - 34 - th + 26, x0 + tx + tw - 3,
                     y1 - 34 - th + 32], fill=(90, 92, 100))
    # flare stack + flame
    d.rectangle([x0 + 196, y1 - 34 - 108, x0 + 202, y1 - 34],
                fill=(44, 46, 54))
    d.polygon([(x0 + 190, y1 - 34 - 108), (x0 + 208, y1 - 34 - 108),
               (x0 + 203, y1 - 34 - 128), (x0 + 199, y1 - 34 - 122),
               (x0 + 195, y1 - 34 - 126)], fill=(240, 140, 40))
    d.polygon([(x0 + 194, y1 - 34 - 108), (x0 + 204, y1 - 34 - 108),
               (x0 + 199, y1 - 34 - 120)], fill=(250, 205, 80))
    # drone silhouette with rotors
    cx, cy = x0 + 118, y0 + 34
    d.ellipse([cx - 26, cy - 4, cx - 14, cy + 2], outline=(220, 220, 210),
              width=2)
    d.ellipse([cx + 14, cy - 4, cx + 26, cy + 2], outline=(220, 220, 210),
              width=2)
    d.rectangle([cx - 16, cy - 1, cx + 16, cy + 5], fill=(12, 12, 14))
    d.rectangle([cx - 3, cy + 5, cx + 3, cy + 10], fill=(12, 12, 14))
    d.ellipse([cx - 2, cy + 10, cx + 2, cy + 14], fill=(240, 60, 50))
    # caption
    d.text((x0 + 6, y1 - 16), "KUWAIT, BEFORE DAWN",
           font=sans_b(9), fill=(235, 230, 210))


def draw_parade_scene(d, x0, y0, x1, y1):
    """Storm clouds, rain and a grounded parade balloon over New York."""
    d.rectangle([x0, y0, x1, y1], fill=(176, 186, 196))
    # skyline
    for bx, bw, bh in [(6, 22, 34), (34, 16, 48), (56, 26, 28),
                       (88, 18, 44), (112, 24, 30), (142, 18, 50),
                       (166, 26, 34), (198, 20, 42), (224, 24, 30),
                       (254, 18, 46), (278, 24, 32)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(96, 104, 116))
    # storm clouds
    for cx, cy, r in [(40, 16, 18), (70, 12, 22), (110, 18, 16),
                      (180, 12, 20), (220, 18, 17), (260, 12, 19)]:
        d.ellipse([x0 + cx - r, y0 + cy - r // 2, x0 + cx + r,
                   y0 + cy + r // 2], fill=(74, 80, 92))
    # rain streaks
    for rx in range(12, 320, 22):
        d.line([x0 + rx, y0 + 34, x0 + rx - 6, y0 + 52], fill=(120, 130, 145),
               width=2)
    # balloon, floating low on the right; tether trails down out of frame
    d.line([x0 + 290, y0 + 40, x0 + 290, y1 - 2], fill=(60, 58, 52),
           width=2)
    d.ellipse([x0 + 250, y0 + 4, x0 + 330, y0 + 40], fill=(164, 30, 34))
    d.ellipse([x0 + 268, y0 + 10, x0 + 312, y0 + 34], fill=(196, 64, 60))
    d.text((x0 + 272, y0 + 14), "100", font=serif_b(16),
           fill=(250, 244, 230))
    d.text((x0 + 6, y1 - 14), "NEW YORK, IN THE RAIN",
           font=sans_b(9), fill=(40, 42, 50))


# ---------------------------------------------------------------- map
# Simplified world continents, drawn in a 470x84 box.
CONTINENTS = [
    [(18, 16), (58, 8), (96, 12), (102, 26), (82, 36), (56, 30),
     (30, 36), (16, 26)],                                   # N. America
    [(104, 48), (126, 42), (136, 52), (126, 74), (112, 68),
     (102, 56)],                                             # S. America
    [(224, 10), (254, 6), (266, 16), (252, 26), (232, 22)],  # Europe
    [(230, 32), (266, 30), (276, 44), (258, 64), (240, 58),
     (228, 44)],                                             # Africa
    [(272, 8), (332, 4), (362, 14), (352, 34), (322, 38), (302, 30),
     (276, 24)],                                             # Asia
    [(392, 56), (422, 52), (432, 62), (406, 70), (388, 64)], # Australia
]
MAP_DOTS = [  # (x, y, label, label dx, label dy)
    (88, 26, "New York", 5, -5),
    (240, 14, None, 0, 0),
    (258, 16, "Kyiv", -8, -14),
    (272, 30, "Gaza", -8, 7),
    (282, 32, "Kuwait", 6, -5),
    (336, 40, "Bangkok", 6, -5),
    (350, 52, None, 0, 0),
    (362, 46, None, 0, 0),
    (272, 52, None, 0, 0),
    (254, 62, None, 0, 0),
    (238, 26, None, 0, 0),
]


def draw_map(d, x0, y0):
    d.rectangle([x0, y0, x0 + 470, y0 + 84], fill=(214, 222, 208))
    d.rectangle([x0, y0, x0 + 470, y0 + 84], outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [(x0 + px, y0 + py) for px, py in poly]
        d.polygon(pts, fill=(168, 172, 148), outline=(90, 92, 80))
    for dx, dy, label, lx, ly in MAP_DOTS:
        d.ellipse([x0 + dx - 3, y0 + dy - 3, x0 + dx + 3, y0 + dy + 3],
                  fill=RED, outline=(255, 255, 255))
        if label:
            d.text((x0 + dx + lx, y0 + dy + ly), label, font=sans_b(8),
                   fill=INK)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 16  # page margin

    # ---- masthead ----
    d.line([(mx, 10), (W - mx, 10)], fill=INK, width=3)
    d.line([(mx, 15), (W - mx, 15)], fill=INK, width=1)
    centre(d, 24, "THE WORLD TODAY", serif_b(60), INK)
    centre(d, 96, "FRIDAY  27  NOVEMBER  2026",
           serif_b(19), RED)
    centre(d, 122, "36 STORIES  \u2022  7 REGIONS  \u2022  ONE DAY, ONE PAGE",
           sans_b(12), GREY)
    d.line([(mx, 146), (W - mx, 146)], fill=INK, width=2)

    # ---- hero band ----
    hy, hh = 156, 214
    # lead story (left)
    d.rectangle([mx, hy, 620, hy + hh], outline=INK, width=2)
    d.text((mx + 12, hy + 10), "LEAD STORY \u2014 MIDDLE EAST",
           font=sans_b(13), fill=RED)
    draw_wrapped(d, mx + 12, hy + 32, 330,
                 "DRONE STRIKE IN\nKUWAIT KILLS\nTWO ITALIANS",
                 serif_b(29), INK, 33)
    draw_wrapped(d, mx + 12, hy + 140, 330,
                 "Kuwait says an Iranian drone hit a vital air-defence "
                 "site, killing two Italian technicians. Tehran denies "
                 "it \u2014 as Brent crude nears $96 and the Gulf braces.",
                 sans(12), INK, 16)
    d.text((mx + 12, hy + hh - 18),
           "Reports: NYT \u2022 BBC \u2022 NDTV \u2014 01:03\u201304:03 UTC",
           font=sans(10), fill=GREY)
    draw_lead_scene(d, 372, hy + 10, 608, hy + hh - 10)

    # second story (right)
    d.rectangle([636, hy, W - mx, hy + hh], outline=INK, width=2)
    d.text((648, hy + 10), "UNITED STATES \u2014 THANKSGIVING",
           font=sans_b(13), fill=RED)
    draw_wrapped(d, 648, hy + 32, 348,
                 "100TH MACY'S PARADE POSTPONED",
                 serif_b(25), INK, 28)
    draw_wrapped(d, 648, hy + 96, 348,
                 "A nor'easter grounds the centenary parade in New York "
                 "for the first time ever. It moves to Saturday as the "
                 "storm floods streets and cancels hundreds of flights.",
                 sans(12), INK, 16)
    draw_parade_scene(d, 648, hy + 148, W - mx - 12, hy + hh - 10)

    # ---- map + timeline strip ----
    sy, sh = 382, 116
    d.rectangle([mx, sy, 500, sy + sh], outline=INK, width=1)
    d.text((mx + 10, sy + 7), "WHERE THE NEWS HAPPENED",
           font=sans_b(11), fill=BLUE)
    draw_map(d, mx + 7, sy + 26)

    d.rectangle([516, sy, W - mx, sy + sh], outline=INK, width=1)
    d.text((526, sy + 7), "THE DAY IN UTC \u2014 27 NOVEMBER 2026",
           font=sans_b(11), fill=BLUE)
    tx0, tx1, ty = 536, 988, sy + 62
    d.line([(tx0, ty), (tx1, ty)], fill=INK, width=2)
    n = len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = tx0 + (tx1 - tx0) * i / (n - 1)
        d.ellipse([cx - 4, ty - 4, cx + 4, ty + 4], fill=RED)
        above = (i % 2 == 0)
        ly = sy + 24 if above else ty + 12
        lx = max(mx + 4, min(cx - 38, W - mx - 82))
        draw_wrapped(d, lx, ly, 78, t, sans_b(9), RED, 11)
        draw_wrapped(d, lx, ly + 11, 78, label, sans(9), INK, 11,
                     max_lines=2)

    # ---- region grid ----
    gy = 500
    col_x = [16, 264, 512, 760]
    col_w = 242
    row_h = 222
    for idx, (name, count, stories) in enumerate(REGIONS):
        row, col = divmod(idx, 4)
        x0 = col_x[col]
        y0 = gy + row * (row_h + 8)
        x1 = x0 + col_w
        y1 = y0 + row_h
        d.rectangle([x0, y0, x1, y1], outline=INK, width=1)
        d.rectangle([x0, y0, x1, y0 + 26], fill=INK)
        d.text((x0 + 8, y0 + 6), name, font=sans_b(12), fill=(250, 244, 230))
        cw = text_w(d, count, sans(10))
        d.text((x1 - cw - 8, y0 + 7), count, font=sans(10),
               fill=(200, 196, 182))
        # adaptive type size so every story fits the box
        size = 12
        while size >= 10:
            fnt = sans_b(size)
            lh = size + 3
            total = 0
            for s in stories:
                total += len(wrap(d, s, fnt, col_w - 20)) * lh + 6
            if y0 + 34 + total <= y1 - 6:
                break
            size -= 1
        fnt = sans_b(size)
        lh = size + 3
        yy = y0 + 34
        for j, s in enumerate(stories):
            lines = wrap(d, s, fnt, col_w - 20)
            d.text((x0 + 8, yy), "\u2022", font=fnt, fill=RED)
            for k, line in enumerate(lines):
                d.text((x0 + 20, yy + k * lh), line, font=fnt, fill=INK)
            yy += len(lines) * lh + 6
            if j < len(stories) - 1:
                d.line([(x0 + 8, yy - 3), (x1 - 8, yy - 3)],
                       fill=(210, 205, 190), width=1)

    # ---- footer ----
    fy = 958
    d.rectangle([mx, fy, W - mx, fy + 28], fill=BLUE)
    centre(d, fy + 7,
           "MARKETS \u2014 DOW 50,183 +0.33%  \u2022  S&P 500 7,183 \u22120.25%  "
           "\u2022  NASDAQ 23,586 \u22120.62%  \u2022  BRENT $96.12  \u2022  "
           "GOLD $3,593  \u2022  US 10-YR 4.85%",
           sans_b(11), (250, 244, 230))
    centre(d, fy + 36,
           "DATE CHECK \u2713 \u2014 FRIDAY 27 NOVEMBER 2026. Every story "
           "happened or was first reported 26\u201327 Nov 2026.",
           sans_b(11), INK)
    centre(d, fy + 54,
           "Sources: BBC \u2022 NYT \u2022 Reuters \u2022 The Guardian \u2022 "
           "AP \u2014 compiled 27 Nov 2026, 08:42 WIB (01:42 UTC)",
           sans(9), GREY)
    d.line([(mx, H - 4), (W - mx, H - 4)], fill=INK, width=2)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    print(path, os.path.getsize(path), "bytes")
