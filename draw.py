#!/usr/bin/env python3
"""Draw the cutest cat (code-drawn, no photos) -> entry.png, 1024x1024.

Deterministic flat illustration: a cream kitten with huge amber eyes,
tilted head, blush, whiskers, curled tail and a yarn ball.
Drawn at 2x supersampling with PIL, then downscaled (Lanczos) for
smooth anti-aliased edges. No external assets, no network.
"""
import math
from PIL import Image, ImageDraw

S = 2            # supersampling factor
W = H = 1024

CREAM = (255, 251, 242, 255)
CREAM_DARK = (243, 226, 199, 255)
OUTLINE = (216, 178, 140, 255)
ORANGE = (242, 176, 110, 255)
ORANGE_DK = (224, 148, 74, 255)
PINK = (242, 120, 140, 255)
PINK_SOFT = (255, 194, 205, 255)
BLUSH = (255, 170, 185, 130)
AMBER = (232, 163, 76, 255)
AMBER_DK = (185, 122, 46, 255)
DARK = (90, 62, 48, 255)
WHISKER = (196, 172, 150, 255)
RED = (232, 93, 93, 255)
RED_DK = (198, 62, 62, 255)
BG_TOP = (255, 247, 236, 255)
BG_BOT = (255, 236, 214, 255)
HALO = (255, 217, 192, 255)
SHADOW = (239, 211, 180, 255)


def sc(v):
    return v * S


def box(x0, y0, x1, y1):
    return (sc(x0), sc(y0), sc(x1), sc(y1))


def pt(x, y):
    return (sc(x), sc(y))


def line(d, points, fill, width):
    d.line([pt(x, y) for x, y in points], fill=fill, width=sc(width), joint="curve")


def rline(d, x0, y0, x1, y1, fill, width):
    """Line with round caps."""
    d.line([pt(x0, y0), pt(x1, y1)], fill=fill, width=sc(width))
    r = sc(width) / 2
    for x, y in ((x0, y0), (x1, y1)):
        d.ellipse((sc(x) - r, sc(y) - r, sc(x) + r, sc(y) + r), fill=fill)


def paw_print(d, cx, cy, s, color):
    """One small paw print (pad + 3 toes)."""
    d.ellipse(box(cx - 0.55 * s, cy - 0.1 * s, cx + 0.55 * s, cy + 0.7 * s), fill=color)
    for dx, dy in ((-0.55, -0.55), (0, -0.75), (0.55, -0.55)):
        d.ellipse(box(cx + dx * s - 0.22 * s, cy + dy * s - 0.22 * s,
                      cx + dx * s + 0.22 * s, cy + dy * s + 0.22 * s), fill=color)


def heart(d, cx, cy, s, color):
    d.ellipse(box(cx - s, cy - 0.75 * s, cx, cy + 0.1 * s), fill=color)
    d.ellipse(box(cx, cy - 0.75 * s, cx + s, cy + 0.1 * s), fill=color)
    d.polygon([pt(cx - s, cy - 0.15 * s), pt(cx + s, cy - 0.15 * s), pt(cx, cy + s)], fill=color)


def ear(d, apex, base_l, base_r, r=26):
    """Triangle ear with a properly rounded tip (fillet circle tangent to
    both edges, so nothing pokes outside the ear's silhouette)."""
    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1])
    def norm(v):
        l = math.hypot(*v)
        return (v[0] / l, v[1] / l)
    u1 = norm(sub(base_l, apex))
    u2 = norm(sub(base_r, apex))
    dot = max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))
    theta = math.acos(dot)
    t = r / math.tan(theta / 2)
    p1 = (apex[0] + u1[0] * t, apex[1] + u1[1] * t)
    p2 = (apex[0] + u2[0] * t, apex[1] + u2[1] * t)
    bis = norm((u1[0] + u2[0], u1[1] + u2[1]))
    o = (apex[0] + bis[0] * r / math.sin(theta / 2),
         apex[1] + bis[1] * r / math.sin(theta / 2))
    d.polygon([pt(*base_l), pt(*p1), pt(*p2), pt(*base_r)], fill=CREAM, outline=OUTLINE)
    d.ellipse(box(o[0] - r, o[1] - r, o[0] + r, o[1] + r), fill=CREAM)


def draw_head():
    """Head (with ears) on its own transparent layer, so it can tilt."""
    layer = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Ears (behind head)
    for sgn in (-1, 1):
        ear(d, (512 + sgn * -162, 150),
            (512 + sgn * -202, 330), (512 + sgn * -32, 265))
        # inner ear
        iapex = (512 + sgn * -152, 205)
        d.polygon([pt(512 + sgn * -177, 300), pt(*iapex), pt(512 + sgn * -67, 260)],
                  fill=PINK_SOFT)
        d.ellipse(box(iapex[0] - 14, iapex[1] - 14, iapex[0] + 14, iapex[1] + 14),
                  fill=PINK_SOFT)
    # Head
    d.ellipse(box(262, 238, 762, 698), fill=CREAM, outline=OUTLINE, width=sc(6))
    # Forehead stripes
    for dx in (-58, 0, 58):
        rline(d, 512 + dx, 300, 512 + dx * 0.85, 348, ORANGE, 13)
    # Eyes: big amber, white highlights
    for sgn in (-1, 1):
        cx, cy = 512 + sgn * 104, 472
        d.ellipse(box(cx - 80, cy - 90, cx + 80, cy + 90), fill=(255, 255, 255, 255),
                  outline=(138, 107, 79, 255), width=sc(4))
        d.ellipse(box(cx - 62, cy - 72, cx + 62, cy + 72), fill=AMBER, outline=AMBER_DK,
                  width=sc(4))
        d.ellipse(box(cx - 26, cy - 40, cx + 26, cy + 40), fill=(30, 20, 16, 255))
        d.ellipse(box(cx - 34, cy - 58, cx - 2, cy - 26), fill=(255, 255, 255, 255))
        d.ellipse(box(cx + 16, cy + 28, cx + 34, cy + 46), fill=(255, 255, 255, 255))
    # Blush
    d.ellipse(box(330, 566, 402, 604), fill=BLUSH)
    d.ellipse(box(622, 566, 694, 604), fill=BLUSH)
    # Nose + mouth
    d.polygon([pt(488, 548), pt(536, 548), pt(512, 580)], fill=PINK)
    d.ellipse(box(498, 566, 526, 586), fill=PINK)
    d.line([pt(512, 580), pt(512, 602)], fill=DARK, width=sc(5))
    d.arc(box(470, 588, 512, 626), 0, 180, fill=DARK, width=sc(5))
    d.arc(box(512, 588, 554, 626), 0, 180, fill=DARK, width=sc(5))
    # Whiskers
    for sgn in (-1, 1):
        for i, (y0, y1, x1) in enumerate(((520, 500, 170), (548, 548, 160), (576, 596, 170))):
            line(d, [(512 + sgn * 205, y0), (512 + sgn * 300, (y0 + y1) / 2),
                     (512 + sgn * 345, y1)], WHISKER, 4)
    return layer


def main():
    img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Background: vertical gradient
    for y in range(H * S):
        t = y / (H * S)
        c = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)) + (255,)
        d.line([(0, y), (W * S, y)], fill=c)
    # Halo circle behind the cat
    d.ellipse(box(512 - 430, 500 - 430, 512 + 430, 500 + 430), fill=HALO)
    # Faint paw prints in the background
    paw_print(d, 150, 180, 34, (243, 216, 186, 255))
    paw_print(d, 880, 240, 30, (243, 216, 186, 255))
    paw_print(d, 120, 760, 30, (243, 216, 186, 255))
    paw_print(d, 900, 700, 34, (243, 216, 186, 255))

    # Soft shadow under the cat
    d.ellipse(box(300, 905, 724, 972), fill=SHADOW)

    # Tail: curled on the ground at the lower right (behind body), outlined
    tail_pts = [(678, 855), (762, 885), (822, 928), (812, 972), (748, 982)]
    line(d, tail_pts, OUTLINE, 62)
    line(d, tail_pts, CREAM, 50)
    # tail stripes (short bands across the tail)
    for (x0, y0, x1, y1) in ((748, 872, 776, 898), (812, 916, 830, 944), (800, 962, 776, 984)):
        d.line([pt(x0, y0), pt(x1, y1)], fill=ORANGE, width=sc(16))

    # Body: chubby sitting kitten
    d.ellipse(box(330, 620, 694, 940), fill=CREAM, outline=OUTLINE, width=sc(6))
    d.ellipse(box(420, 700, 604, 920), fill=(255, 253, 248, 255))
    # Front paws together
    d.ellipse(box(415, 845, 507, 932), fill=CREAM, outline=OUTLINE, width=sc(5))
    d.ellipse(box(517, 845, 609, 932), fill=CREAM, outline=OUTLINE, width=sc(5))
    for cx in (461, 563):
        d.line([pt(cx, 890), pt(cx, 922)], fill=OUTLINE, width=sc(4))

    # Yarn ball beside the paws
    d.ellipse(box(776, 848, 868, 940), fill=RED, outline=RED_DK, width=sc(4))
    d.arc(box(782, 862, 862, 926), 200, 340, fill=RED_DK, width=sc(5))
    d.arc(box(776, 848, 868, 940), 20, 120, fill=RED_DK, width=sc(5))
    d.arc(box(794, 880, 850, 936), 250, 60, fill=RED_DK, width=sc(5))
    # loose thread curling from the ball toward the paw
    line(d, [(780, 920), (730, 940), (668, 932)], RED_DK, 5)

    # Head, tilted slightly for charm
    head = draw_head()
    head = head.rotate(5, resample=Image.BICUBIC, center=pt(512, 468))
    img.alpha_composite(head)

    # Little floating heart
    heart(d, 800, 210, 26, PINK)

    img = img.convert("RGB").resize((W, H), Image.LANCZOS)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
