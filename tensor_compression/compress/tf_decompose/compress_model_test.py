import tensorflow as tf

from tensorflow import keras
from compress_model import get_compressed_model

#TODO: write regular tests
if __name__ == "__main__":
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(1024, activation=tf.nn.relu),
        keras.layers.Dense(256, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_images[:100, ...], train_labels[:100, ...], epochs=1)

    print('Evaluate source model')
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=0)
    print('Test accuracy:', test_acc)

    compressed_model = get_compressed_model(model, {
                                                        'dense': ('svd', 750),
    })

    compressed_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    print('Evaluate compressed model')
    test_loss, test_acc = compressed_model.evaluate(test_images, test_labels, verbose=0)
    print('Test accuracy:', test_acc)

    for layer in compressed_model.layers:
        print(layer.name)