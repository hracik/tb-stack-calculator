#!/usr/bin/env python3
"""Icon tool for the Krappy Calculator: takes unit / epic icons from game screenshots the same way every time.

  python3 tools/icon_tool.py find SHOT.png
        finds the tier badges (the round II / III / ... circles) in a screenshot, prints them numbered and writes SHOT_find.png
        with the numbers drawn on, so you can see which one is which.

  python3 tools/icon_tool.py unit SHOT.png --badge 2 --style army  --to epicunit:candle:1      # one stack of an epic (the 1 = type: 0 melee, 1 ranged, 2 mounted, 3 flying)
  python3 tools/icon_tool.py unit SHOT.png --badge 1 --style sales --to merc:"Elder Witch"     # a mercenary / unit picture
        --badge  = the number from `find`, or x,y,r (centre and radius of the tier badge in pixels)
        --style  = which screen the card comes from: army (the Start march screen, the number sits on a dark band at the bottom of the art)
                   or sales (the Sales / shop screen, the number sits on the art and the card has a parchment frame)
        --crop   = optional, "x0,x1,y0,y1" in units of the badge radius, measured from the badge centre (to override the style)
        The picture is cut from the art only (the number is left out), put into the standard frame (dark gold, 112 x 112) and gets the tier badge of
        the screenshot in the top left corner - the same as every other unit picture in the app. SHOT_<name>.png is written next to the app for a look.

  python3 tools/icon_tool.py epic SHOT.png --box x0,y0,x1,y1 --key candle
        the epic monster: the box is the golden frame of the epic picture (with its level badge). Writes the framed picture (120 px, the battle report)
        and the plain art (72 px, the picker and the summary).

All results go straight into app.js (ICD for mercenaries, EPIC_UN / EPIC_FR / EPIC_IC for epics) - nothing to paste. Needs Pillow (with AVIF), numpy, opencv.
"""
import sys, re, io, os, base64, argparse
import numpy as np
from PIL import Image, ImageDraw
import cv2

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app.js')
OUT = 112
# the frame of the existing unit pictures, outside in (sampled from them): black, dark, dark, brown, brown-gold x3
FRAME = [(1, 0, 0), (15, 9, 0), (15, 9, 0), (43, 28, 7), (85, 66, 33), (85, 66, 33), (85, 66, 33)]
# art window, from the badge centre, in badge radii: x0, x1, y0, y1 (the part of the card that is only picture - no number, no frame)
STYLES = {'army': (0.29, 5.06, -0.19, 3.61), 'sales': (0.41, 4.78, -0.47, 3.91)}


def b64(im, fmt='AVIF', **k):
    o = io.BytesIO(); im.save(o, fmt, **k); return base64.b64encode(o.getvalue()).decode()


def find_badges(img):
    """The tier badges: a round, fully saturated coloured disc (green II, blue III ...) with a gold ring. Found by colour (circles in the colour mask) and checked
    for the gold ring around the disc, so round things inside the pictures do not fool it."""
    a = np.array(img.convert('RGB')); W = a.shape[1]
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    mask = ((hsv[..., 1] > 200) & (hsv[..., 2] > 40)).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cs = cv2.HoughCircles(cv2.GaussianBlur(mask, (5, 5), 0), cv2.HOUGH_GRADIENT, dp=1, minDist=int(W * 0.05), param1=100, param2=14,
                          minRadius=int(W * 0.016), maxRadius=int(W * 0.03))
    out = []
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    for x, y, r in (cs[0] if cs is not None else []):
        x, y, r = int(x), int(y), int(r)
        y0, y1, x0, x1 = max(y - 2 * r, 0), y + 2 * r, max(x - 2 * r, 0), x + 2 * r
        d = np.hypot(xx[y0:y1, x0:x1] - x, yy[y0:y1, x0:x1] - y)
        fill = (mask[y0:y1, x0:x1][d < r * 0.8] > 0).mean()
        ring = hsv[y0:y1, x0:x1][(d > r * 1.12) & (d < r * 1.4)]            # the ring: gold / yellow-brown, strongly lit
        gold = ((ring[:, 0] > 10) & (ring[:, 0] < 30) & (ring[:, 1] > 100)).mean() if len(ring) else 0
        if fill > 0.6 and gold > 0.4: out.append((x, y, int(round(r / 0.72))))
    # one badge can give several circles: keep the first of every group that overlaps
    keep = []
    for c in out:
        if all(np.hypot(c[0] - k[0], c[1] - k[1]) > c[2] * 0.8 for k in keep): keep.append(c)
    keep.sort(key=lambda c: (round(c[1] / (W * 0.1)), c[0]))
    return keep


def cmd_find(a):
    im = Image.open(a.shot).convert('RGB'); bs = find_badges(im)
    d = ImageDraw.Draw(im)
    for i, (x, y, r) in enumerate(bs, 1):
        print(f'{i}: x={x} y={y} r={r}')
        d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 0, 255), width=3); d.text((x + r + 4, y - r), str(i), fill=(255, 255, 0))
    p = os.path.splitext(a.shot)[0] + '_find.png'; im.save(p); print('written', p)


def get_badge(im, spec):
    if ',' in spec:
        x, y, r = [int(float(v)) for v in spec.split(',')]; return x, y, r
    bs = find_badges(im); return bs[int(spec) - 1]


def circle(im, x, y, r):
    c = im.crop((x - r, y - r, x + r, y + r)); m = Image.new('L', (c.width * 4, c.height * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, m.width - 1, m.height - 1), fill=255); return c, m.resize(c.size, Image.LANCZOS)


def clean_badge(im, x, y, r):                    # takes the old badge out of the picture so no ring peeks from under the new one
    arr = np.array(im); m = np.zeros(arr.shape[:2], np.uint8); cv2.circle(m, (x, y), int(r * 1.2), 255, -1)
    return Image.fromarray(cv2.inpaint(arr, m, 6, cv2.INPAINT_TELEA))


def make_unit(im, x, y, r, style, crop=None):
    x0, x1, y0, y1 = crop or STYLES[style]
    art = clean_badge(im, x, y, r).crop((round(x + x0 * r), round(y + y0 * r), round(x + x1 * r), round(y + y1 * r)))
    c = Image.new('RGB', (OUT, OUT), (0, 0, 0)); d = ImageDraw.Draw(c)
    for i, col in enumerate(FRAME): d.rectangle((i, i, OUT - 1 - i, OUT - 1 - i), outline=col)
    n = len(FRAME); c.paste(art.resize((OUT - 2 * n, OUT - 2 * n), Image.LANCZOS), (n, n))
    b, m = circle(im, x, y, int(r * 0.88)); R = 15
    c.paste(b.resize((2 * R, 2 * R), Image.LANCZOS), (1, 1), m.resize((2 * R, 2 * R), Image.LANCZOS))
    return c


def put(js, pat, new):
    js2, n = re.subn(pat, lambda m: m.group(1) + new, js, 1)
    if n != 1: raise SystemExit('could not place it in app.js: ' + pat)
    return js2


def cmd_unit(a):
    im = Image.open(a.shot).convert('RGB'); x, y, r = get_badge(im, a.badge)
    crop = [float(v) for v in a.crop.split(',')] if a.crop else None
    ic = make_unit(im, x, y, r, a.style, crop); data = 'data:image/avif;base64,' + b64(ic, quality=75)
    js = open(APP, encoding='utf-8').read(); kind, *rest = a.to.split(':')
    if kind == 'merc':                            # a mercenary / unit picture: ICD
        name = rest[0]
        if f'"{name}":"data:image' in js: js = re.sub(r'("%s":")data:image/[^"]+' % re.escape(name), lambda m: m.group(1) + data, js, 1)
        else: js = js.replace('const ICD={', 'const ICD={"%s":"%s",' % (name, data), 1)
    elif kind == 'epicunit':                      # one stack of an epic: EPIC_UN[epic][type]
        key, ty = rest[0], rest[1]
        m = re.search(r'(const EPIC_UN=\{(?:.*?,)?%s:\{)([^}]*)\}' % re.escape(key), js)
        if m:
            parts = dict(re.findall(r'(\d):("data:image/[^"]+")', m.group(2))); parts[ty] = '"%s"' % data
            body = ','.join('%s:%s' % (k, parts[k]) for k in sorted(parts))
            js = js[:m.start()] + m.group(1) + body + '}' + js[m.end():]
        else: js = js.replace('const EPIC_UN={', 'const EPIC_UN={%s:{%s:"%s"},' % (key, ty, data), 1)
    else: raise SystemExit('--to must be merc:NAME or epicunit:KEY:TYPE')
    open(APP, 'w', encoding='utf-8').write(js)
    p = os.path.splitext(a.shot)[0] + '_' + re.sub(r'\W+', '_', a.to) + '.png'; ic.resize((224, 224), Image.LANCZOS).save(p)
    print('put into app.js:', a.to, '| preview', p)


def cmd_epic(a):
    im = Image.open(a.shot).convert('RGB'); x0, y0, x1, y1 = [int(v) for v in a.box.split(',')]
    box = im.crop((x0, y0, x1, y1)); w, h = box.size
    fr = box.resize((120, 120), Image.LANCZOS)
    ic = box.crop((int(w * .17), int(h * .21), int(w * .79), int(h * .83))).resize((72, 72), Image.LANCZOS)      # the plain art inside the frame, no badge
    js = open(APP, encoding='utf-8').read()
    for var, im2, fmt, mime in (('EPIC_FR', fr, 'AVIF', 'avif'), ('EPIC_IC', ic, 'JPEG', 'jpeg')):
        d = 'data:image/%s;base64,%s' % (mime, b64(im2, fmt, quality=80))
        if re.search(r'const %s=\{(?:.*?,)?%s:"' % (var, a.key), js): js = re.sub(r'(const %s=\{(?:.*?,)?%s:")[^"]+' % (var, a.key), lambda m: m.group(1) + d, js, 1)
        else: js = js.replace('const %s={' % var, 'const %s={%s:"%s",' % (var, a.key, d), 1)
    open(APP, 'w', encoding='utf-8').write(js)
    p = os.path.splitext(a.shot)[0] + '_epic_' + a.key + '.png'
    c = Image.new('RGB', (260, 130), (40, 40, 40)); c.paste(fr, (0, 5)); c.paste(ic.resize((120, 120)), (135, 5)); c.save(p); print('put into app.js: epic', a.key, '| preview', p)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest='c', required=True)
    f = sp.add_parser('find'); f.add_argument('shot'); f.set_defaults(fn=cmd_find)
    u = sp.add_parser('unit'); u.add_argument('shot'); u.add_argument('--badge', required=True); u.add_argument('--style', choices=list(STYLES), default='army')
    u.add_argument('--to', required=True); u.add_argument('--crop'); u.set_defaults(fn=cmd_unit)
    e = sp.add_parser('epic'); e.add_argument('shot'); e.add_argument('--box', required=True); e.add_argument('--key', required=True); e.set_defaults(fn=cmd_epic)
    a = ap.parse_args(); a.fn(a)
