"""
Monocular depth estimation on agricultural field images.

Uses Depth Anything V2 (Small) — a public pretrained model — to predict a dense
depth map from a single RGB photo, for canopy / crop depth perception in
agri-robotics scenarios. Outputs side-by-side RGB | colorized-depth panels.

Usage:
    python depth_estimate.py --images /path/to/field_images --n 3
"""
import argparse
import glob
import os

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import pipeline

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
MODEL_ID = "depth-anything/Depth-Anything-V2-Small-hf"


def colorize(depth: np.ndarray) -> np.ndarray:
    d = cv2.normalize(depth.astype(np.float32), None, 0, 255, cv2.NORM_MINMAX)
    return cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_MAGMA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True, help="dir of field images")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--width", type=int, default=900, help="output panel width per side")
    args = ap.parse_args()

    os.makedirs(ASSETS, exist_ok=True)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Loading {MODEL_ID} on {device} ...")
    pipe = pipeline("depth-estimation", model=MODEL_ID, device=device)

    paths = []
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        paths += glob.glob(os.path.join(os.path.expanduser(args.images), ext))
    paths = sorted(paths)[: args.n]
    print(f"Running on {len(paths)} images ...")

    for i, p in enumerate(paths, 1):
        img = Image.open(p).convert("RGB")
        depth = np.array(pipe(img)["depth"])          # HxW
        depth_c = colorize(depth)                       # HxWx3 BGR

        rgb = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        rgb = cv2.resize(rgb, (depth_c.shape[1], depth_c.shape[0]))

        h = int(args.width * rgb.shape[0] / rgb.shape[1])
        rgb = cv2.resize(rgb, (args.width, h))
        depth_c = cv2.resize(depth_c, (args.width, h))
        panel = cv2.hconcat([rgb, depth_c])

        out = os.path.join(ASSETS, f"depth_demo_{i}.jpg")
        cv2.imwrite(out, panel, [cv2.IMWRITE_JPEG_QUALITY, 88])
        print(f"  saved {out}")

    print("Done.")


if __name__ == "__main__":
    main()
