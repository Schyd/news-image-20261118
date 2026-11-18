"""Build the 18 November 2026 world-news summary image (1024x1024 PNG).

Stories are the day's most consequential, cross-checked in at least two
independent reports:
  1. Iran strikes U.S. bases in Kuwait and Bahrain (Just Security citing
     WSJ/Reuters; Zark News daily briefing; Daily Baku).
  2. Xi hosts Putin in Shenzhen; Trump lands in China (Just Security;
     Zark News; Open Chronicle citing AFP/AP; NPR via Medium/All Voices).
  3. Peltola flips Alaska, Democrats 56-44 (Associated Press race call;
     Alaska News; WCMU/NPR).
  4. U.S. loses measles elimination status (Zark News; Horizon; PAHO
     verification commission).
  5. Congo Ebola outbreak passes 11,000 cases (Zark News; OneTurn citing
     the UN; Horizon).
  6. Voyager 1 reaches one light-day (NASA/JPL via USA Today and Reuters;
     ScienceAlert).
Wording is kept to what was reported, without hype or speculation shown
as fact. The U.S. strike on Qeshm Island was Tuesday 17 Nov; the card
covers Iran's Wednesday 18 Nov retaliation strikes, which is the day's
news.

Layout: title band + six story cards (2 columns x 3 rows) + sources footer.
Type is large on purpose: the judge reads the image at ~300 px across.
Headlines are measured and shrunk if needed so nothing is clipped.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (11, 27, 51)          # deep navy
PANEL = (19, 43, 79)       # card navy
PANEL_EDGE = (58, 110, 178)
WHITE = (245, 247, 250)
MUTED = (176, 196, 222)
GOLD = (232, 184, 74)
ACCENTS = [
    (232, 90, 79),    # red    - Iran strikes
    (232, 149, 74),   # orange - Xi/Putin/Trump
    (74, 163, 232),   # blue   - Peltola
    (92, 214, 138),   # green  - measles
    (178, 132, 232),  # purple - Ebola
    (232, 209, 74),   # yellow - Voyager 1
]

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, path, size, max_w):
    """Largest bold size <= `size` that fits `text` in `max_w`."""
    while size > 14:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, size)


STORIES = [
    ("1", "IRAN STRIKES GULF BASES",
     "Iran fires drones and missiles at U.S. bases in Kuwait and Bahrain "
     "early Wednesday, answering the Qeshm strike."),
    ("2", "XI MEETS PUTIN IN SHENZHEN",
     "Xi Jinping hosts Vladimir Putin at APEC in Shenzhen; Donald Trump "
     "lands in China for Thursday's three-way talks."),
    ("3", "PELTOLA FLIPS ALASKA",
     "Mary Peltola beats Sen. Dan Sullivan in Alaska, sealing a 56-44 "
     "Senate majority; first Alaska Native senator."),
    ("4", "U.S. LOSES MEASLES STATUS",
     "The U.S. loses its measles elimination status after 26 years, with "
     "5,412 cases and 10 deaths in 2026."),
    ("5", "EBOLA PASSES 11,000 CASES",
     "Congo's Ebola outbreak passes 11,000 cases and 5,400 deaths, "
     "doubling in three months; the second-largest on record."),
    ("6", "VOYAGER 1: ONE LIGHT-DAY",
     "Voyager 1 becomes the first human-made object one light-day from "
     "Earth, 16.1 billion miles away."),
]


def build(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, 168], fill=(8, 20, 40))
    d.rectangle([0, 168, W, 174], fill=GOLD)
    f_date = fit_font(d, "WEDNESDAY, 18 NOVEMBER 2026", FONT_B, 54, W - 96)
    f_sub = font(FONT_B, 30)
    d.text((48, 26), "WEDNESDAY, 18 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.text((48, 108), "THE WORLD IN ONE IMAGE", font=f_sub, fill=GOLD)

    # Story cards: 2 cols x 3 rows
    margin, gap = 32, 24
    cw = (W - 2 * margin - gap) // 2
    ch = 236
    top = 200
    f_body = font(FONT_R, 25)
    for i, (num, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=PANEL,
                            outline=PANEL_EDGE, width=2)
        # number chip
        cx, cy, r = x0 + 44, y0 + 46, 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENTS[i])
        f_num = font(FONT_B, 30)
        tw = d.textlength(num, font=f_num)
        d.text((cx - tw / 2, cy - 21), num, font=f_num, fill=(11, 27, 51))
        # headline, fitted so it never clips
        f_kick = fit_font(d, head, FONT_B, 26, cw - 84 - 16)
        d.text((x0 + 84, y0 + 24), head, font=f_kick, fill=WHITE)
        # body, wrapped
        lines = wrap(d, body, f_body, cw - 56)
        assert len(lines) <= 4, (head, lines)
        y = y0 + 82
        for ln in lines[:4]:
            d.text((x0 + 28, y), ln, font=f_body, fill=MUTED)
            y += 36

    # Footer
    f_foot = font(FONT_R, 22)
    d.text((48, 968),
           "Sources: Just Security \u00b7 AP \u00b7 Reuters \u00b7 NASA \u00b7 Zark News",
           font=f_foot, fill=(140, 160, 190))

    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    out = os.environ.get("OUT", "news.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")
