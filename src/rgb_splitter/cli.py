import argparse
import os  # Path işlemleri için os modülünü eklememiz gerekiyor
from .core import run


def main():
    parser = argparse.ArgumentParser(
        prog="rgb-split",
        description="Split RGGB CFA FITS files into R/G/B FITS planes (superpixel, no interpolation).",
    )
    parser.add_argument("--input", "-i", default="./data", help="Input directory (default: ./data)")
    
    # DEĞİŞİKLİK 1: default değerini None yaptık ve help metnini güncelledik.
    parser.add_argument(
        "--output", 
        "-o", 
        default=None, 
        help="Output directory (Optional. Default: <input_dir>/rgb_split)"
    )
    
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=None,
        help="Number of worker processes (default: cpu_count-1)",
    )

    args = parser.parse_args()

    # DEĞİŞİKLİK 2: Eğer output girilmediyse, input yolunun içine rgb_split ekle
    input_dir = args.input
    output_dir = args.output

    if output_dir is None:
        # Örnek: input="./data" ise output="./data/rgb_split" olur
        output_dir = os.path.join(input_dir, "rgb_split")

    # core.run fonksiyonuna hesapladığımız output_dir'i gönderiyoruz
    raise SystemExit(run(input_dir, output_dir, args.workers))