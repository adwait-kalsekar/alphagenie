import tensorflow as tf
from keras.models import load_model

model = load_model(f'./trained_models/AAPL-lstm.h5')

print(model.summary)
