import numpy as np

# from keras.layers import Dense
# from keras.layers import LSTM
import joblib

class lstm_model():
    def __init__(self):
        self.model = self.load_model("/usr/local/Desktop/paper1/paper1/model/best_model_lstm_new.hdf5")
        self.scaler = joblib.load('/usr/local/Desktop/paper1/paper1/model/scaler.save')
        # return self._model()
    
    def load_model(self, filepath):
        print("Load model")
        self.model = load_model(filepath)
        return self.model

    def build_model(self):
        # unit = hidden state
        # self.model.add(LSTM(units=64, input_shape=(1, 4), activation='relu', return_sequences=True))

        # self.model.add(LSTM(units=128, activation='relu', return_sequences=True))

        # self.model.add(LSTM(units=64, activation='relu', return_sequences=False))

        # # lop dau vao hinh tron
        # self.model.add(Dense(1)) 
        pass

    def threshhold(self, data):
        return 1 if data >= 0.5 else 0
    
    def min_max_scaler(self, datas):
        return self.scaler.transform(np.array(datas).reshape(1, -1))

    def predict(self, data):
        new_input = self.min_max_scaler(data)
        return self.threshhold(self.model.predict( np.array([new_input, ])))
