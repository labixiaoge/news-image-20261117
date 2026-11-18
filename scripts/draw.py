#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Reproducible: run `python3 scripts/draw.py` from the repo root and it
writes entry.png next to main.ts. Every headline and caption is drawn
with PIL vector text (DejaVu Sans) so nothing is garbled.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (22, 35, 63)
GOLD = (212, 175, 55)
PAPER = (247, 243, 232)
INK = (24, 28, 36)
GREY = (90, 96, 104)
RED = (178, 34, 34)
SKY = (191, 212, 230)
SEA = (46, 107, 138)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def hero_scene(d):
    """Kerch Bridge over water, middle span collapsed, smoke rising."""
    d.rectangle([24, 172, 1000, 392], fill=SKY)
    # distant shore
    d.rectangle([24, 330, 1000, 392], fill=(120, 150, 170))
    # sea
    d.rectangle([24, 392 - 62, 1000, 392], fill=SEA)
    d.line([24, 352, 1000, 352], fill=(255, 255, 255), width=2)
    # bridge deck: left intact, right intact, middle fallen
    d.rectangle([24, 300, 430, 318], fill=(70, 74, 80))
    d.rectangle([594, 300, 1000, 318], fill=(70, 74, 80))
    # fallen span, tilted down into the water
    d.polygon([(430, 300), (594, 300), (560, 372), (470, 372)],
              fill=(96, 100, 108))
    # pylons
    d.rectangle([120, 210, 138, 300], fill=(52, 56, 64))
    d.rectangle([880, 210, 898, 300], fill=(52, 56, 64))
    d.line([129, 210, 24, 300], fill=(52, 56, 64), width=3)
    d.line([129, 210, 430, 300], fill=(52, 56, 64), width=3)
    d.line([889, 210, 594, 300], fill=(52, 56, 64), width=3)
    d.line([889, 210, 1000, 300], fill=(52, 56, 64), width=3)
    # gap marker: broken ends
    d.polygon([(430, 300), (448, 300), (448, 318), (430, 318)],
              fill=(178, 34, 34))
    d.polygon([(576, 300), (594, 300), (594, 318), (576, 318)],
              fill=(178, 34, 34))
    # flames at the break
    for cx, cy, r in [(500, 330, 26), (530, 344, 20), (478, 348, 16)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 120, 30))
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                  fill=(245, 200, 60))
    # smoke puffs
    for cx, cy, r in [(500, 250, 34), (545, 225, 28), (462, 228, 26),
                      (520, 195, 22), (480, 192, 18)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(105, 108, 115))
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                  fill=(140, 143, 150))
    # splash where the span hit the water
    for cx, cy, r in [(500, 368, 18), (530, 372, 12), (470, 372, 12)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                  fill=(220, 235, 242))
    d.text((36, 182), "1  UKRAINE", font=font(BOLD, 20), fill=NAVY)


def tanker_scene(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 228, 238))
    d.rectangle([x0, y0 + h - 42, x0 + w, y0 + h], fill=(46, 107, 138))
    # tanker hull
    d.polygon([(x0 + 14, y0 + h - 62), (x0 + w - 14, y0 + h - 62),
               (x0 + w - 34, y0 + h - 38), (x0 + 34, y0 + h - 38)],
              fill=(120, 30, 30))
    d.rectangle([x0 + 30, y0 + h - 88, x0 + 70, y0 + h - 62],
                fill=(240, 240, 240))
    d.rectangle([x0 + 78, y0 + h - 80, x0 + 118, y0 + h - 62],
                fill=(200, 200, 200))
    # fire + smoke
    d.ellipse([x0 + w - 78, y0 + 34, x0 + w - 38, y0 + 74],
              fill=(232, 120, 30))
    d.ellipse([x0 + w - 68, y0 + 44, x0 + w - 48, y0 + 64],
              fill=(245, 200, 60))
    for cx, cy, r in [(x0 + w - 58, y0 + 18, 16), (x0 + w - 78, y0 + 8, 12),
                      (x0 + w - 40, y0 + 6, 10)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(105, 108, 115))
    # second tanker, small, in the distance
    d.rectangle([x0 + 16, y0 + h - 56, x0 + 84, y0 + h - 44],
                fill=(70, 74, 80))
    d.text((x0 + 10, y0 + 6), "2  MIDDLE EAST", font=font(BOLD, 18),
           fill=NAVY)


def flags_scene(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 238, 244))
    # three flag poles with simple flags: USA, China, Russia
    poles = [x0 + 52, x0 + w // 2, x0 + w - 52]
    # USA: red/white stripes, blue canton
    fx, fy = poles[0], y0 + 34
    for i in range(5):
        d.rectangle([fx, fy + i * 7, fx + 62, fy + i * 7 + 7],
                    fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, fy, fx + 26, fy + 18], fill=(22, 35, 63))
    # China: red flag, yellow stars
    fx = poles[1] - 31
    d.rectangle([fx, fy, fx + 62, fy + 35], fill=(222, 41, 16))
    d.ellipse([fx + 6, fy + 6, fx + 16, fy + 16], fill=(255, 220, 60))
    # Russia: white / blue / red horizontal
    fx = poles[2] - 62
    d.rectangle([fx, fy, fx + 62, fy + 12], fill=(255, 255, 255))
    d.rectangle([fx, fy + 12, fx + 62, fy + 24], fill=(0, 57, 166))
    d.rectangle([fx, fy + 24, fx + 62, fy + 35], fill=(213, 0, 50))
    for px in poles:
        d.line([px, y0 + 34, px, y0 + h - 30], fill=(52, 56, 64), width=3)
    # place label under the flags, centred, no background shape
    label = "MANILA  •  SHENZHEN"
    lf = font(BOLD, 16)
    d.text((x0 + w // 2 - d.textlength(label, font=lf) / 2, y0 + h - 24),
           label, font=lf, fill=NAVY)
    d.text((x0 + 10, y0 + 6), "3  ASIA", font=font(BOLD, 18), fill=NAVY)


def rocket_scene(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 28, 48))
    for sx, sy in [(x0 + 30, y0 + 20), (x0 + 120, y0 + 44),
                   (x0 + 200, y0 + 16), (x0 + 260, y0 + 52),
                   (x0 + 70, y0 + 70)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # rocket body, tilted and breaking in two (drawn large, centre-left)
    d.polygon([(x0 + 52, y0 + 84), (x0 + 96, y0 + 56),
               (x0 + 116, y0 + 84), (x0 + 72, y0 + 112)], fill=(230, 230, 230))
    d.polygon([(x0 + 122, y0 + 50), (x0 + 166, y0 + 22),
               (x0 + 186, y0 + 50), (x0 + 142, y0 + 78)], fill=(200, 200, 200))
    d.polygon([(x0 + 96, y0 + 56), (x0 + 116, y0 + 84),
               (x0 + 122, y0 + 50), (x0 + 142, y0 + 78)], fill=(232, 120, 30))
    # falling satellites: grey box + solar panels
    for sx, sy in [(x0 + 220, y0 + 82), (x0 + 268, y0 + 96),
                   (x0 + 188, y0 + 106)]:
        d.rectangle([sx - 18, sy - 5, sx + 18, sy + 5], fill=(40, 90, 160))
        d.rectangle([sx - 9, sy - 9, sx + 9, sy + 9], fill=(180, 180, 180))
    d.text((x0 + 10, y0 + 6), "4  SPACE", font=font(BOLD, 18),
           fill=(255, 255, 255))


def bank_scene(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 236, 240))
    # bank building: pediment + columns
    bx, by = x0 + 30, y0 + 26
    d.polygon([(bx, by + 22), (bx + 110, by), (bx + 220, by + 22)],
              fill=(52, 56, 64))
    d.rectangle([bx, by + 22, bx + 220, by + 30], fill=(52, 56, 64))
    for i in range(4):
        cx = bx + 22 + i * 58
        d.rectangle([cx - 9, by + 30, cx + 9, by + 82], fill=(120, 126, 134))
    d.rectangle([bx, by + 82, bx + 220, by + 90], fill=(52, 56, 64))
    # glitch: red zigzag across the building + error tag
    pts = [(x0 + 18, y0 + h - 34), (x0 + 70, y0 + h - 52),
           (x0 + 120, y0 + h - 30), (x0 + 170, y0 + h - 50),
           (x0 + 220, y0 + h - 32), (x0 + 268, y0 + h - 48)]
    d.line(pts, fill=(178, 34, 34), width=5, joint="curve")
    d.rectangle([x0 + w - 92, y0 + 8, x0 + w - 10, y0 + 34], fill=RED)
    d.text((x0 + w - 84, y0 + 10), "ERROR", font=font(BOLD, 17),
           fill=(255, 255, 255))
    d.text((x0 + 10, y0 + 6), "5  US FINANCE", font=font(BOLD, 18),
           fill=NAVY)


def cell(d, x0, y0, w, h, scene, headline, caption):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255),
                outline=NAVY, width=2)
    scene(d, x0 + 2, y0 + 2, w - 4, 118)
    hf = font(BOLD, 23)
    lines = wrap(d, headline, hf, w - 24)
    y = y0 + 130
    for ln in lines[:2]:
        d.text((x0 + 12, y), ln, font=hf, fill=INK)
        y += 28
    cf = font(REG, 18)
    lines = wrap(d, caption, cf, w - 24)
    for ln in lines[:3]:
        d.text((x0 + 12, y), ln, font=cf, fill=GREY)
        y += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 108], fill=NAVY)
    centred(d, W // 2, 18, "THE WORLD IN ONE IMAGE", font(BOLD, 50),
            (255, 255, 255))
    centred(d, W // 2, 76, "FIVE STORIES  •  ONE DAY  •  AROUND THE WORLD",
            font(BOLD, 19), GOLD)
    # date band
    d.rectangle([0, 108, W, 156], fill=GOLD)
    centred(d, W // 2, 116, "TUESDAY 17 NOVEMBER 2026", font(BOLD, 34), NAVY)
    # hero panel
    d.rectangle([24, 172, 1000, 522], fill=(255, 255, 255),
                outline=NAVY, width=3)
    hero_scene(d)
    hf = font(BOLD, 36)
    d.text((40, 402), "UKRAINE STRIKES KERCH BRIDGE", font=hf, fill=INK)
    cf = font(REG, 21)
    hero_cap = ("Road span collapses — second strike in under 24 hours. "
                "Russia hits Kyiv bridges; heat, water and power disrupted.")
    y = 448
    for ln in wrap(d, hero_cap, cf, 936):
        d.text((40, y), ln, font=cf, fill=GREY)
        y += 27
    # 2x2 grid
    cw, ch, gap = 480, 228, 16
    gx, gy = 24, 538
    cell(d, gx, gy, cw, ch, tanker_scene,
         "TANKERS HIT NEAR HORMUZ",
         "Two tankers struck mines and caught fire; a third reported hit. "
         "USS Theodore Roosevelt arrives — three US carriers in the region.")
    cell(d, gx + cw + gap, gy, cw, ch, flags_scene,
         "TRUMP IN MANILA; XI–TRUMP–PUTIN TO MEET",
         "Trump begins a three-day Asia trip at ASEAN. "
         "Three-way meeting in Shenzhen on Thu 19 Nov.")
    cell(d, gx, gy + ch + gap, cw, ch, rocket_scene,
         "VULCAN ROCKET FAILS; 40 SATELLITES LOST",
         "Failed about 10 minutes after launch from Cape Canaveral; "
         "40 Amazon Leo satellites lost.")
    cell(d, gx + cw + gap, gy + ch + gap, cw, ch, bank_scene,
         "JPMORGAN BUG SLOWS BANKING",
         "Software bug — not a cyberattack — slowed online banking, "
         "branches and Zelle payments on Monday.")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", os.path.abspath(out), img.size)


if __name__ == "__main__":
    main()
