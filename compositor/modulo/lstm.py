from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM, Bidirectional, Embedding


def criar_modelo():
    model = Sequential()
    model.add(Embedding(input_dim=3375, output_dim=1024))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dropout(0.4))
    model.add(Dense(3375))
    model.add(Activation('softmax'))
    model.load_weights('teste2.hdf5')

    return model
