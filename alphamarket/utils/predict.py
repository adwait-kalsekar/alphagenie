import tensorflow as tf
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def predict_data(ticker, df):
    model = load_model(f'alphamarket/utils/trained_models/{ticker}-lstm.h5')
    scaler = MinMaxScaler(feature_range=(0,1))
    df['scaled_values'] = scaler.fit_transform(df['Adj Close'].values.reshape(-1,1))

    predictions = model.predict(df['scaled_values'])
    predictions = scaler.inverse_transform(predictions)
    df['predictions'] = predictions
    return df