import tensorflow as tf
import os
os.makedirs('model', exist_ok=True)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(6, activation='softmax')
])

model.save('model/vitamin_model.h5')
print('Saved dummy model to model/vitamin_model.h5')
