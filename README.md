# The World in One Image — Tuesday 17 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261117)
[![competition](https://img.shields.io/badge/competition-news--image--20261117-green)](https://make.fun/bounty/news-image-20261117)

## About

A 1024×1024 editorial front-page infographic that sums up the world news
of **Tuesday 17 November 2026** in a single image. The masthead names the
day prominently, and five stories are shown with a drawn scene, a short
bold headline and one factual caption each:

1. **Ukraine strikes Kerch Bridge** — a road span collapses in the second
   strike in under 24 hours; Russia hits Kyiv's bridges over the Dnipro,
   disrupting heating, water and power.
2. **Tankers hit near Hormuz** — two oil tankers struck mines and caught
   fire on a route Tehran calls unauthorised; a third was reported hit.
   The USS Theodore Roosevelt arrived, making three US carriers in the
   region.
3. **Trump in Manila; Xi–Trump–Putin to meet** — President Trump arrived
   in Manila for the ASEAN summit, first stop of a three-day Asia trip.
   China confirmed a three-way meeting in Shenzhen on Thursday 19 Nov.
4. **Vulcan rocket fails; 40 satellites lost** — the ULA Vulcan rocket
   failed about 10 minutes after launching from Cape Canaveral, destroying
   its payload of 40 Amazon Leo internet satellites.
5. **JPMorgan bug slows banking** — a software bug (not a cyberattack)
   slowed online banking, branch transactions and Zelle payments on Monday.

The image is drawn with Python PIL (vector text, so every headline stays
crisp and legible); no AI image generation is used. Sources for the five
stories: Algenom, Level Headlines, NPR and Zark News briefings of
17 November 2026.

## How to run

The entry program is `main.ts` (Node 22, standard library only). It copies
the finished `entry.png` to the output directory:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the image from source first:

```sh
python3 scripts/draw.py
```

`scripts/draw.py` writes `entry.png` in the repo root. The program is
deterministic: running it twice produces byte-identical output.

## Files

- `entry.png` — the finished 1024×1024 image (≤ 1 MiB)
- `main.ts` — the entry program (copies `entry.png` to the output dir)
- `scripts/draw.py` — the PIL program that draws `entry.png`
- `package.json`, `LICENSE` (MIT)
