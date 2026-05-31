"""
Training entry point.

Usage:
    python training/train.py --crop cassava --dataset-version v1 --epochs 20

Steps:
1. Load dataset from R2 manifest
2. Apply augmentation (albumentations)
3. Build model (MobileNetV3-Large or EfficientNet-Lite-B0 backbone)
4. Fine-tune with per-crop classifier head
5. Save best checkpoint
"""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--crop", required=True, choices=["cassava", "maize", "plantain", "tomato", "cocoa"])
    parser.add_argument("--dataset-version", required=True)
    parser.add_argument("--backbone", default="mobilenetv3", choices=["mobilenetv3", "efficientnet_lite"])
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--output-dir", default="checkpoints/")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(f"Training pipeline not yet implemented for crop={args.crop}")


if __name__ == "__main__":
    main()
