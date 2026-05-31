"""
Generates a minimal placeholder SavedModel for each crop so TF Serving can boot
in local dev without a real trained model.

Output: services/ml/models/<crop>/1/saved_model.pb  (+ variables/)

Usage:
    pip install tensorflow
    python scripts/generate_placeholder_model.py
"""

import os
import numpy as np

CROPS = {
    "cassava": 5,
    "maize": 5,
    "plantain": 5,
    "tomato": 5,
    "cocoa": 5,
}

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def build_placeholder_model(num_classes: int):
    import tensorflow as tf

    inputs = tf.keras.Input(shape=(224, 224, 3), name="input_image")
    x = tf.keras.layers.GlobalAveragePooling2D()(inputs)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax", name="predictions")(x)
    return tf.keras.Model(inputs, outputs)


def main():
    import tensorflow as tf

    for crop, num_classes in CROPS.items():
        out_dir = os.path.join(MODELS_DIR, crop, "1")
        os.makedirs(out_dir, exist_ok=True)
        model = build_placeholder_model(num_classes)
        tf.saved_model.save(model, out_dir)
        print(f"  saved placeholder model → {out_dir}")


if __name__ == "__main__":
    main()
