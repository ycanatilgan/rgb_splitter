import argparse
import os
from .core import run


def _resolve_default_output(input_path: str) -> str:
    # input dosya ise: dosyanın klasörü / rgb_split
    # input klasör ise: klasör / rgb_split
    if os.path.isfile(input_path):
        return os.path.join(os.path.dirname(input_path), "rgb_split")
    return os.path.join(input_path, "rgb_split")


def main():
    parser = argparse.ArgumentParser(
        prog="rgb-split",
        description="Split RGGB CFA FITS files into R/G/B FITS planes (superpixel, no interpolation).",
        epilog=(
            "Examples:\n"
            "  rgb-split                  (Process current directory)\n"
            "  rgb-split ./data\n"
            "  rgb-split ./data ./out\n"
            "  rgb-split ./data/example.fits\n"
            "  rgb-split ./data=./out\n"
            "  rgb-split -i ./data -o ./out -w 8\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Yeni kullanım: rgb-split INPUT [OUTPUT]
    # Ek kısa yol: rgb-split INPUT=OUTPUT
    parser.add_argument(
        "input",
        nargs="?",
        default=".",
        help="Input path (directory OR a single .fit/.fits). Defaults to current directory. You can also pass INPUT=OUTPUT here.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Optional output directory. If omitted, default is <input>/rgb_split (or <input_file_dir>/rgb_split).",
    )

    # Geriye dönük uyumluluk: eski flag'ler
    parser.add_argument(
        "--input", "-i",
        dest="input_flag",
        default=None,
        help="(Legacy) Input path (directory OR file).",
    )
    parser.add_argument(
        "--output", "-o",
        dest="output_flag",
        default=None,
        help="(Legacy) Output directory.",
    )

    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=None,
        help="Number of worker processes (default: cpu_count-1)",
    )

    args = parser.parse_args()

    # 1) Input seçimi: flag verilmişse onu kullan, yoksa positional
    input_path_raw = args.input_flag if args.input_flag is not None else args.input

    # 2) Tek argüman INPUT=OUTPUT desteği (yalnızca output ayrıca verilmediyse)
    input_path = input_path_raw
    output_from_inline = None
    if args.output is None and args.output_flag is None and isinstance(input_path_raw, str) and "=" in input_path_raw:
        left, right = input_path_raw.split("=", 1)
        left = left.strip()
        right = right.strip()
        if left and right:
            input_path = left
            output_from_inline = right

    # 3) Output seçimi öncelik sırası:
    #    - legacy -o/--output
    #    - inline INPUT=OUTPUT
    #    - ikinci positional OUTPUT
    #    - default
    if args.output_flag is not None:
        output_dir = args.output_flag
    elif output_from_inline is not None:
        output_dir = output_from_inline
    elif args.output is not None:
        output_dir = args.output
    else:
        output_dir = _resolve_default_output(input_path)

    raise SystemExit(run(input_path, output_dir, args.workers))
