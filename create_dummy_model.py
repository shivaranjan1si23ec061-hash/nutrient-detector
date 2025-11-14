import tensorflow as tf
import os

# Create model folder if not exists
os.makedirs('model', exist_ok=True)

# ---------------------------------------------
# Corrected dummy model (for demonstration)
# ---------------------------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.Rescaling(1./255),                 # Normalize images
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),

    # 6 outputs → 6 vitamins: A, B12, C, D, E, Calcium / Iron
    tf.keras.layers.Dense(6, activation='sigmoid')     # sigmoid = better for deficiency scores
])

# Save the model
model.save('model/vitamin_model.h5')

print('Saved dummy model to model/vitamin_model.h5')
