"""
This module contains functions for compressing fully-connected and conv layers.
"""

from absl import logging
from tensorflow import keras

from svd_layer import get_svd_seq


def get_compressed_model(model, decompose_info):
    """Compresses source model using decompositions from decompose_info dict.

    For example if decompose_info = {
            'dense': ('svd', 10)
    }
    it means that the layer with the name 'dense' will be compressed
    using TruncatedSVD with truncation rank 10.

    For fully-connected layer you can use SVD decomposition
    For convolution layer networks CP3, CP4, Tucker-2 are available.

    If you want learn more about different tensor decomposition refer:

    'Tensor Networks for Dimensionality Reduction and Large-Scale Optimization.
    Part 1 Low-Rank Tensor Decompositions.'

    :param model: source model.
    :param decompose_info: dict that describes what layers compress using what decomposition method.
                           Possible decompositions are: 'svd', 'cp3', 'cp4', 'tucker-2'.
    :return: new tf.keras.Model with compressed layers.
    """
    model_input = model.input
    x = model_input

    for idx, layer in enumerate(model.layers):
        if layer.name not in decompose_info:
            x = layer(x)
            continue

        decompose, decomp_rank = decompose_info[layer.name]
        if decompose.lower() == 'svd':
            logging.info('SVD layer {}'.format(layer.name))
            for svd_layer in get_svd_seq(layer, rank=decomp_rank, copy_conf=True):
                x = svd_layer(x)
        else:
            logging.info('Incorrect decomposition type for the layer {}'.format(layer.name))
            raise NameError("Wrong Decomposition Name. You should use one of: ['svd', 'cp3', 'cp4', 'tucker-2']")

    return keras.Model(model_input, x)


