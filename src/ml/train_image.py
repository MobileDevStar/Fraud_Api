import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models

def load_dataset(root_dir, img_size=(224,224)):
    X, y = [], []
    for label_name, label_idx in [("genuine", 0), ("fraud", 1)]:
        folder = os.path.join(root_dir, label_name)
        for fn in os.listdir(folder):
            if not fn.lower().endswith((".png",".jpg")): continue
            img = Image.open(os.path.join(folder, fn)).convert("RGB")
            img = img.resize(img_size)
            X.append(np.array(img) / 255.0)
            y.append(label_idx)
    return np.array(X), np.array(y)

if __name__ == "__main__":
    # 1. Load images + labels
    X, y = load_dataset("data/synth/images")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 2. Build a simple CNN
    model = models.Sequential([
        layers.Conv2D(32, 3, activation="relu", input_shape=(224,224,3)),
        layers.MaxPool2D(),
        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPool2D(),
        layers.Conv2D(128, 3, activation="relu"),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    # 3. Train
    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        batch_size=32
    )

    # 4. Save
    os.makedirs("models", exist_ok=True)
    model.save("models/fraud_detector.h5")
    print("Model trained and saved to models/fraud_detector.h5")
