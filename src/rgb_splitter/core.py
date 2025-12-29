import os
import glob
import numpy as np
from astropy.io import fits
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import warnings
import time
import datetime

warnings.filterwarnings("ignore", category=UserWarning)


def _process_single_file_extraction(args):
    """
    ProcessPoolExecutor için pickle-friendly wrapper.
    """
    filepath, input_dir, output_dir = args
    filename = os.path.basename(filepath)

    try:
        # 1. Klasör Yapısını Hazırla
        rel_path = os.path.relpath(filepath, input_dir)
        base_output_folder = os.path.join(output_dir, os.path.dirname(rel_path))

        # Kanal bazlı alt klasörler
        r_folder = os.path.join(base_output_folder, "R")
        g_folder = os.path.join(base_output_folder, "G")
        b_folder = os.path.join(base_output_folder, "B")
        os.makedirs(r_folder, exist_ok=True)
        os.makedirs(g_folder, exist_ok=True)
        os.makedirs(b_folder, exist_ok=True)

        name, ext = os.path.splitext(filename)

        out_r = os.path.join(r_folder, f"{name}{ext}")
        out_g = os.path.join(g_folder, f"{name}{ext}")
        out_b = os.path.join(b_folder, f"{name}{ext}")

        # Resume: hepsi varsa atla
        if os.path.exists(out_r) and os.path.exists(out_g) and os.path.exists(out_b):
            return "SKIPPED"

        with fits.open(filepath) as hdul:
            data = hdul[0].data
            header = hdul[0].header
            original_dtype = data.dtype

            # Superpixel extraction (RGGB)
            R_raw = data[0::2, 0::2]
            G1_raw = data[0::2, 1::2]
            G2_raw = data[1::2, 0::2]
            B_raw = data[1::2, 1::2]

            G_avg = (G1_raw.astype(np.float32) + G2_raw.astype(np.float32)) / 2.0

            # dtype koru
            if np.issubdtype(original_dtype, np.integer):
                R_final = R_raw
                B_final = B_raw
                G_final = np.clip(G_avg, 0, 65535).astype(original_dtype)
            else:
                R_final = R_raw
                B_final = B_raw
                G_final = G_avg.astype(original_dtype)

            channels = {
                "R": (R_final, out_r),
                "G": (G_final, out_g),
                "B": (B_final, out_b),
            }

            process_date = datetime.datetime.now().isoformat()

            for channel_name, (img_data, out_path) in channels.items():
                new_header = header.copy()

                # WCS/geometri güncellemesi
                if "CRPIX1" in new_header:
                    new_header["CRPIX1"] /= 2
                if "CRPIX2" in new_header:
                    new_header["CRPIX2"] /= 2
                if "CDELT1" in new_header:
                    new_header["CDELT1"] *= 2
                if "CDELT2" in new_header:
                    new_header["CDELT2"] *= 2

                # Filtre bilgisi
                new_header["FILTER"] = (channel_name, "Extracted RGB Channel")

                # Traceability
                new_header["CREATOR"] = ("Python Science Splitter", "Software used for splitting")
                new_header["PARENT"] = (filename, "Original CFA file name")

                # History
                new_header.add_history(f"[{process_date}] CFA SPLIT PROCESS APPLIED")
                new_header.add_history("Method: Superpixel Extraction (No Interpolation)")

                new_header.add_history("Software Ref: https://github.com/ycanatilgan/rgb_splitter")
                
                new_header.add_history(f"Channel: {channel_name} extracted from RGGB pattern")
                if channel_name == "G":
                    new_header.add_history("Note: Green channel is average of G1 and G2 pixels")

                fits.writeto(out_path, img_data, new_header, overwrite=True, checksum=True)

        return "OK"

    except Exception as e:
        return f"ERROR: {filename} - {str(e)}"


def run(input_dir: str, output_dir: str, workers: int | None = None) -> int:
    """
    Ana işlemi çalıştırır. 0: başarılı, 1: hatalı.
    """
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    if workers is None:
        cpu = os.cpu_count() or 1
        workers = max(1, cpu - 1)

    print("--- RGB SPLITTER (CLI) ---")
    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Workers: {workers}")

    files = glob.glob(os.path.join(input_dir, "**", "*.fit*"), recursive=True)
    files = [f for f in files if os.path.isfile(f) and not f.endswith("summary.txt")]

    print(f"Toplam {len(files)} dosya işlenecek.")

    start_time = time.time()

    results = {"OK": 0, "SKIPPED": 0, "ERROR": 0}
    errors: list[str] = []

    tasks = [(f, input_dir, output_dir) for f in files]

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = list(
            tqdm(
                executor.map(_process_single_file_extraction, tasks),
                total=len(tasks),
                unit="img",
            )
        )

        for res in futures:
            if res == "OK":
                results["OK"] += 1
            elif res == "SKIPPED":
                results["SKIPPED"] += 1
            elif isinstance(res, str) and res.startswith("ERROR"):
                results["ERROR"] += 1
                errors.append(res)

    print("\n--- İŞLEM TAMAMLANDI ---")
    print(f"Süre: {time.time() - start_time:.2f} saniye")
    print(f"Başarılı: {results['OK']}")
    print(f"Atlanan: {results['SKIPPED']}")
    print(f"Hatalı: {results['ERROR']}")

    if errors:
        print("\nHatalar:")
        for err in errors:
            print(err)
        return 1

    return 0
