"""Figures for preprocessing-mismatches-that-cost-accuracy.

A synthetic 1920 x 1080 test frame (drawn below) passed through the two common resize methods and a channel swap.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from style import INK, INK2, save

SLUG = "preprocessing-mismatches-that-cost-accuracy"
W, H, S = 1920, 1080, 640

img = np.full((H, W, 3), (210, 215, 205), np.uint8)
cv2.rectangle(img, (0, 820), (W, H), (150, 150, 150), -1)                    # floor
for x, col in [(420, (40, 40, 200)), (960, (30, 140, 230)), (1500, (200, 120, 40))]:
    cv2.circle(img, (x, 430), 170, col, -1)                                   # round signs (BGR colours)
    cv2.rectangle(img, (x - 60, 620), (x + 60, 900), (60, 60, 60), -1)        # posts
cv2.putText(img, "STOP", (300, 470), cv2.FONT_HERSHEY_SIMPLEX, 3.2, (255, 255, 255), 9, cv2.LINE_AA)

stretch = cv2.resize(img, (S, S), interpolation=cv2.INTER_AREA)
r = S / W
nh = int(round(H * r))
letter = np.full((S, S, 3), 114, np.uint8)
top = (S - nh) // 2
letter[top:top + nh] = cv2.resize(img, (S, nh), interpolation=cv2.INTER_AREA)
swapped = letter[:, :, ::-1].copy()

fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.6))
for ax, (im, t) in zip(axes, [(letter, "Letterbox: shape kept, grey padding"),
                              (stretch, "Stretch: circles become ellipses"),
                              (swapped, "Letterbox with BGR/RGB swapped")]):
    ax.imshow(im[:, :, ::-1])
    ax.set_title(t, loc="left", fontsize=12.5)
    ax.axis("off")
fig.suptitle("The same synthetic frame, three ways a 640 x 640 model can receive it", x=0.01, ha="left",
             fontsize=14, weight="bold", y=1.02)
fig.tight_layout()
save(fig, f"{SLUG}-resize-and-colour.png")
