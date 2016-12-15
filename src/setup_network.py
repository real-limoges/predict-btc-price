'''
Set up the bulding_rnnand organize the data for the RNN
'''
import warnings
import numpy as np
import pandas as pd
import tflearn as tf
import matplotlib.pyplot as plt
import seaborn

warnings.filterwarnings("ignore")

HISTORY = 30
FUTURE = 8
DATASET = '../data/dataset.csv'


def define_model(input_shape):
    '''
    Builds the RNN map
    '''

    bulding_rnn = tf.input_data(shape=input_shape)
    bulding_rnn = tf.lstm(bulding_rnn, 32, activation='softsign',
                          return_seq=False)
    bulding_rnn = tf.fully_connected(bulding_rnn, 8, activation='linear')
    bulding_rnn = tf.regression(
        bulding_rnn,
        optimizer='sgd',
        loss='mean_square',
        learning_rate=0)
    return bulding_rnn


def organize_data(original_rnn_data):
    '''
    Organizes the data into time slices
    '''

    np_original_data = original_rnn_data.values

    target = np_original_data[HISTORY + FUTURE - 1:, :]
    data_matrix = np_original_data[:len(target), :]

    final_data_matrix = np.empty([len(target), HISTORY, 8])

    for i, _ in enumerate(data_matrix):
        chunk = data_matrix[i:i + HISTORY, :]

        if chunk.shape == (HISTORY, 8):
            final_data_matrix[i, :, :] = chunk
        else:
            final_data_matrix[i, :, :] = np.ones(
                (HISTORY, 8))

    return (final_data_matrix, target)


def create_train_test(X_frame, y_frame):
    '''
    Creates a train/test split by the last 300 realizations
    '''
    final_X_train = X_frame[:-300, :]
    final_y_train = y_frame[:-300, :]
    final_X_test = X_frame[-300:, :]
    final_y_test = y_frame[-300:, :]

    mean_X = np.mean(final_X_train)
    mean_Y = np.mean(final_y_train)
    std_X = np.mean(final_X_train)
    std_Y = np.mean(final_y_train)

    print std_X
    print final_X_train.shape
    final_X_train = (final_X_train - mean_X) / std_X
    final_X_test = (final_X_test - mean_X)/ std_X
    final_y_train = (final_y_train - mean_Y) / std_Y
    final_y_test = (final_y_test - mean_Y)/ std_Y

    return (final_X_train, final_X_test, final_y_train, final_y_test)


def chart_predictions(predicted, actual):
    plt.figure(figsize=(20,25))

    for i, point in enumerate(predicted.T):
        plt.plot(point, 'k-', label = 'Act/ual')
        plt.plot(actual[:,i], 'c-', label='Forecast')
        plt.legend()

        plt.show()


if __name__ == '__main__':
    built_rnn = define_model([None, HISTORY, FUTURE])
    rnn_net = tf.DNN(built_rnn, clip_gradients=0.0, tensorboard_verbose=0)

    final_data_matrix, target = organize_data(pd.read_csv(DATASET))

    final_X_train, final_X_test, final_y_train, final_y_test = create_train_test( final_data_matrix, target )


    rnn_net.fit(final_X_train, final_y_train, n_epoch=25)
    rnn_net.save('../data/model.tfl')
    predicted = np.array(rnn_net.predict(final_X_test))
    
    chart_predictions(final_y_test, predicted)


