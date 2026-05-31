"""
Evaluation against the locked field-test set.

Metrics: top-1 accuracy, per-class recall, ECE, confusion matrix.
Must pass thresholds before a model candidate can be deployed.

Usage:
    python training/evaluate.py --crop cassava --checkpoint checkpoints/cassava_best.keras
"""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--crop", required=True, choices=["cassava", "maize", "plantain", "tomato", "cocoa"])
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--field-test-manifest", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(f"Evaluation pipeline not yet implemented for crop={args.crop}")


if __name__ == "__main__":
    main()
