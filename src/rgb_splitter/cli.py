import argparse
from .core import run


def main():
    parser = argparse.ArgumentParser(
        prog="rgb-splitter",
        description="Split RGGB CFA FITS files into R/G/B FITS planes (superpixel, no interpolation).",
    )
    parser.add_argument("--input", "-i", default="./data", help="Input directory (default: ./data)")
    parser.add_argument("--output", "-o", default="./output_rgb", help="Output directory (default: ./output_rgb)")
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=None,
        help="Number of worker processes (default: cpu_count-1)",
    )

    args = parser.parse_args()
    raise SystemExit(run(args.input, args.output, args.workers))
