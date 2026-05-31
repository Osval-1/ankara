"""
Export a trained checkpoint as a TF SavedModel and upload to Cloudflare R2.

Usage:
    python training/export.py --crop cassava --checkpoint checkpoints/cassava_best.keras \
        --dataset-version v1 --code-commit abc1234
"""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--crop", required=True, choices=["cassava", "maize", "plantain", "tomato", "cocoa"])
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--dataset-version", required=True)
    parser.add_argument("--code-commit", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(f"Export not yet implemented for crop={args.crop}")


if __name__ == "__main__":
    main()
