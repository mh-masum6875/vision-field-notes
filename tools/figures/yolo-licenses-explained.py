"""Figures for yolo-licenses-explained: where GPL/AGPL obligations start, and the four commercial routes."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID

SLUG = "yolo-licenses-explained"


def rbox(ax, x, y, w, h, ec, fc, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.0", fc=fc, ec=ec, lw=lw))


def fig_triggers():
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.axis("off")
    rows = [
        ("Run it only on your own\nmachines, no outside users", ("Usually not\ntriggered", False), ("Usually not\ntriggered", False)),
        ("Ship a copy: a device,\ninstaller or bundled library", ("Offer source\nunder GPL", True), ("Offer source\nunder AGPL", True)),
        ("Users reach a modified\nversion over a network", ("Usually not\ntriggered", False), ("Offer source\nto those users", True)),
    ]
    x0, wq, wc, gap = 0, 34, 29.5, 3
    xg, xa = x0 + wq + gap, x0 + wq + gap + wc + gap
    ax.text(xg + wc / 2, 47, "GPL-3.0", ha="center", va="center", fontsize=14, weight="bold", color=INK)
    ax.text(xg + wc / 2, 43.5, "e.g. YOLOv7", ha="center", va="center", fontsize=11, color=INK2)
    ax.text(xa + wc / 2, 47, "AGPL-3.0", ha="center", va="center", fontsize=14, weight="bold", color=INK)
    ax.text(xa + wc / 2, 43.5, "e.g. Ultralytics YOLO", ha="center", va="center", fontsize=11, color=INK2)
    h, step = 10.5, 13
    for i, (q, g, a) in enumerate(rows):
        y = 28 - i * step
        ax.text(x0, y + h / 2, q, ha="left", va="center", fontsize=12.5, color=INK, linespacing=1.3)
        for x, (txt, on) in [(xg, g), (xa, a)]:
            if on:
                rbox(ax, x, y, wc, h, ACCENT, ACCENT + "26")
                ax.text(x + wc / 2, y + h / 2, txt, ha="center", va="center", fontsize=12.5, weight="bold", color=INK, linespacing=1.25)
            else:
                rbox(ax, x, y, wc, h, GRID, "#f6f5f1")
                ax.text(x + wc / 2, y + h / 2, txt, ha="center", va="center", fontsize=12.5, color=INK2, linespacing=1.25)
    ax.text(0, -4.5, "Simplified summary, not legal advice. What counts as modified, or as a work\nbased on the code, is a question for a qualified person.",
            ha="left", va="center", fontsize=10.5, color=INK2, style="italic")
    ax.text(50, 53.5, "GPL starts at distribution; AGPL also covers network use", ha="center", va="center",
            fontsize=14, weight="bold", color=INK)
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(-8.5, 56)
    style.save(fig, f"{SLUG}-obligation-triggers.png")


def fig_routes():
    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.axis("off")
    routes = [
        ("1  Comply with the open licence", "You release your application's source\nunder the same licence.",
         "Fits: open projects, or where the code\nis not the secret ingredient."),
        ("2  Buy a commercial licence", "Fee, scope and terms are set by the\nvendor. Read the agreement.",
         "Fits: closed products that want to keep\nusing the Ultralytics models."),
        ("3  Use a permissive detector", "Check the code, the pretrained weights\nand the pretraining data, all three.",
         "Fits: closed products that can switch\nmodel family."),
        ("4  Build your own architecture", "Most control, most effort. Every\ncomponent still needs a licence check.",
         "Fits: teams that need full ownership\nand have time to build it."),
    ]
    w, h = 48.5, 22
    pos = [(0, 25), (51.5, 25), (0, 0), (51.5, 0)]
    for (x, y), (t, cost, fit), c in zip(pos, routes, C[:4]):
        rbox(ax, x, y, w, h, c, c + "1a", lw=1.8)
        ax.text(x + 2.2, y + h - 3.6, t, ha="left", va="center", fontsize=13.5, weight="bold", color=INK)
        ax.text(x + 2.2, y + h - 10, cost, ha="left", va="center", fontsize=11.5, color=INK, linespacing=1.3)
        ax.text(x + 2.2, y + 4.5, fit, ha="left", va="center", fontsize=11.5, color=INK2, linespacing=1.3)
    ax.text(50, 51.5, "Four routes for a commercial product, each with a cost", ha="center", va="center",
            fontsize=14, weight="bold", color=INK)
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(-0.8, 54)
    style.save(fig, f"{SLUG}-commercial-routes.png")


if __name__ == "__main__":
    fig_triggers()
    fig_routes()
