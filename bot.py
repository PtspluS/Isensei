import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
import random
import matplotlib.pyplot as plt

name = "Martin"

model = load_model('advanced_bot.h5')

def play(board, available_cells, player):

    # taux d'exploration
    explore_rate = 0.2

    map = np.copy(board).reshape(1,49)

    max = [-1,-1]

    #on remplace les 2 par des -1
    np.where(map == 2, -1, map)

    # map avec les proba
    prob_map = model.predict(map)

    # on reshape
    prob_map = prob_map.reshape((7,7))

    # on vient trier
    list_proba = sort_map(prob_map)


    # iterateur
    i = 0

    if explore_rate > random.random():
        return random.choice(available_cells)
    else:
        while not isin(available_cells, max):
            max = list_proba[len(list_proba)-1-i]
            i += 1

        return max

def isin(tab, elt):
    for e in tab:
        if e == elt:
            return True

    return False

def sort_map(map):
    """
    resume = {}
    sort = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            resume[(i, j)] = map[i][j]

    srtd = [k for k in sorted(resume.values())]
    for e in srtd:
        sort.append(list(list(resume.keys())[list(resume.values()).index(e)]))
        srtd.remove(e)
    return sort
    """
    a = np.array(map)
    i = (-a).argsort(axis=None, kind='mergesort')
    j = np.unravel_index(i, a.shape)
    #sort = np.vstack(j).T
    sort = [[x,y] for x,y in zip(j[0],j[1])]
    return sort

class Network:

    def __init__(self, create = True):

        if create :
            opt = Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
            self.model = Sequential()
            self.model.add(Dense(49, activation='tanh', input_dim=49, kernel_initializer='random_normal',
                                     bias_initializer='ones'))
            self.model.add(Dense(196, activation='relu', kernel_initializer='random_normal',
                                     bias_initializer='ones'))
            self.model.add(Dense(392, activation='relu', kernel_initializer='random_normal',
                             bias_initializer='ones'))
            self.model.add(Dense(286, activation='relu', kernel_initializer='random_normal',
                             bias_initializer='ones'))
            self.model.add(Dense(150, activation='relu', kernel_initializer='random_normal',
                             bias_initializer='ones'))
            self.model.add(Dense(49, activation='sigmoid', kernel_initializer='random_normal',
                             bias_initializer='ones'))
            self.model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

        else:
            self.load()

        self.model.summary()

    def predict(self, board):
        out = self.model.predict(board)
        return out

    def train(self, training_data, target_data, epochs = 1000, batch_size = 1, verbose = 0):
        history = self.model.fit(training_data, target_data, epochs= epochs, batch_size= batch_size, verbose=verbose)

        scores = self.model.evaluate(training_data, target_data, verbose=1)
        print('Test loss:', scores[0])
        print('Test accuracy:', scores[1])
        plt.plot(history.history['loss'])
        plt.plot(history.history['accuracy'])
        plt.show()


    def save(self):
        name = 'advanced_bot.h5'
        self.model.save(name)
        print("The model is saved as : "+name)

    def load(self):
        self.model = load_model('advanced_bot.h5')
        print('Model loaded from : advanced_bot.h5')
