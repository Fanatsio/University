import argparse
import cv2
import os
from src.cpmc_proposals import generate_proposals

def main():
    parser = argparse.ArgumentParser(description="CPMC-like proposal generator")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--out", default="results", help="Output directory")
    parser.add_argument("--nseg", type=int, default=800)
    parser.add_argument("--compact", type=float, default=7.0)
    parser.add_argument("--grid", type=int, default=50)
    parser.add_argument("--topk", type=int, default=200)
    parser.add_argument("--workers", type=int, default=8, help="Number of parallel workers for GraphCut (default: 1 — no parallelism)")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    img = cv2.imread(args.image)
    if img is None:
        raise RuntimeError("Cannot load image: " + args.image)

    generate_proposals(
        img,
        image_name=os.path.basename(args.image),
        out_dir=args.out,
        n_segments=args.nseg,
        compactness=args.compact,
        grid_step=args.grid,
        top_k=args.topk,
        use_subframes=True,
        workers=args.workers,
    )

if __name__ == "__main__":
    main()
