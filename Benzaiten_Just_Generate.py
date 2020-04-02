import tensorflow as tf
import keras.backend as K
from keras.models import Sequential

def init_layer(layer):
    session = K.get_session()
    weights_initializer = tf.variables_initializer(layer.weights)
    session.run(weights_initializer)

model = Sequential()
layer = model.load_weights('Benzaiten_ActiveSet.h5')
init_layer(layer)
