import tensorflow as tf

import numpy as np
import matplotlib.pyplot as plt
#import h5py
import os

# Define dataset path
DATASET_PATH = "cat_model/dataset"

# Image parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32


# Load datasets
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(DATASET_PATH, "train"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(DATASET_PATH, "val"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(DATASET_PATH, "test"),
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

# Data Augmentation
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
])

# Normalize pixel values (rescale to [0,1])
normalization_layer = tf.keras.layers.Rescaling(1./255)
train_dataset = train_dataset.map(lambda x, y: (data_augmentation(normalization_layer(x), training=True), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))
test_dataset = test_dataset.map(lambda x, y: (normalization_layer(x), y))

# Load MobileNetV2 without top layers (pretrained on ImageNet)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze first 100 layers
base_model.trainable = True
for layer in base_model.layers[:100]:  
    layer.trainable = False

# Build custom model
# THIS MIGHT NEED ADJUSTMENT LATER
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),  # dropout to reduce overfitting
    tf.keras.layers.Dense(1, activation="sigmoid")  # Binary classification
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), 
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Early stopping to prevent overfitting
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,  
    restore_best_weights=True
)

# Train the model
EPOCHS = 20  # tends to stop at 10
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS,
    callbacks=[early_stopping]
)

# Evaluate the model on test data
test_loss, test_acc = model.evaluate(test_dataset)
print(f"Test Accuracy: {test_acc:.4f}")

# Plot training history
plt.plot(history.history["accuracy"], label="train accuracy")
plt.plot(history.history["val_accuracy"], label="val accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

# Save. Replace X with the version number
model.save("cat_detectorX.h5")
print("Model saved as cat_detectorX.h5")

model.summary()

