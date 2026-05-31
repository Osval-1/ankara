"""
Temperature scaling calibration on the held-out validation set.

Outputs a per-crop temperature value that is copied into
services/api/src/app/services/confidence_calibrator.py (_TEMPERATURE dict).

Usage:
    python training/calibrate.py --crop cassava --checkpoint checkpoints/cassava_best.keras
"""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--crop", required=True, choices=["cassava", "maize", "plantain", "tomato", "cocoa"])
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--val-manifest", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(f"Calibration not yet implemented for crop={args.crop}")


if __name__ == "__main__":
    main()
