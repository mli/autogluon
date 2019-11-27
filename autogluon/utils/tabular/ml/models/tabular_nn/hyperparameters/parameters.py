""" Default (fixed) hyperparameter values used in Neural network model """
import mxnet as mx

from ....constants import BINARY, MULTICLASS, REGRESSION
from .......scheduler.resource import get_gpu_count


def get_fixed_params():
    """ Parameters that currently cannot be searched during HPO """
    fixed_params = {
        'num_epochs': 300,  # maximum number of epochs for training NN
        'num_dataloading_workers': 1,  # will be overwritten by nthreads_per_trial
        'ctx': (mx.gpu() if get_gpu_count() > 0 else mx.cpu()),  # will be overwritten by ngpus_per_trial  # NOTE: Causes crash during GPU HPO if not wrapped in a function.
        'seed_value': None,  # random seed for reproducibility (set = None to ignore)
        # For data processing:
        'proc.embed_min_categories': 4,  # apply embedding layer to categorical features with at least this many levels. Features with fewer levels are one-hot encoded. Choose big value to avoid use of Embedding layers
        # Options: [3,4,10, 100, 1000]
        'proc.impute_strategy': 'median',  # # strategy argument of sklearn.SimpleImputer() used to impute missing numeric values
        # Options: ['median', 'mean', 'most_frequent']
        'proc.max_category_levels': 500,  # maximum number of allowed levels per categorical feature
        # Options: [10, 100, 200, 300, 400, 500, 1000, 10000]
        'proc.skew_threshold': 0.99,  # numerical features whose absolute skewness is greater than this receive special power-transform preprocessing. Choose big value to avoid using power-transforms
        # Options: [0.2, 0.3, 0.5, 0.8, 1.0, 10.0, 100.0]
    }
    return fixed_params


def get_hyper_params():
    """ Parameters that currently can be tuned during HPO """
    hyper_params = {
        ## Hyperparameters for neural net architecture:
        'network_type': 'widedeep',  # Type of neural net used to produce predictions
        # Options: ['widedeep', 'feedforward']
        'layers': None,  # List of widths (num_units) for each hidden layer (Note: only specifies hidden layers. These numbers are not absolute, they will also be scaled based on number of training examples and problem type)
        # Options: List of lists that are manually created
        'numeric_embed_dim': None,  # Size of joint embedding for all numeric+one-hot features.
        # Options: integer values between 10-10000
        'activation': 'relu',  # Activation function
        # Options: ['relu', 'softrelu' 'elu'??, 'tanh']
        'max_layer_width': 2056,  # maximum number of hidden units in network layer (integer > 0)
        # Does not need to be searched by default
        'embedding_size_factor': 1.0,  # scaling factor to adjust size of embedding layers (float > 0)
        # Options: range[0.01 - 100] on log-scale
        'embed_exponent': 0.56,  # exponent used to determine size of embedding layers based on # categories.
        'max_embedding_dim': 100,  # maximum size of embedding layer for a single categorical feature (int > 0).
        ## Regression-specific hyperparameters:
        'y_range': None,  # Tuple specifying whether (min_y, max_y). Can be = (-np.inf, np.inf).
        # If None, inferred based on training labels. Note: MUST be None for classification tasks!
        'y_range_extend': 0.05,  # Only used to extend size of inferred y_range when y_range = None.
        ## Hyperparameters for neural net training:
        'use_batchnorm': True,  # whether or not to utilize Batch-normalization
        # Options: [True, False]
        'dropout_prob': 0.1,  # dropout probability, = 0 turns off Dropout.
        # Options: range(0.0, 0.5)
        'batch_size': 512,  # batch-size used for NN training
        # Options: [32, 64, 128. 256, 512, 1024, 2048]
        'loss_function': None,  # MXNet loss function minimized during training
        'optimizer': 'adam',  # MXNet optimizer to use.
        # Options include: ['adam','sgd']
        'learning_rate': 3e-4,  # learning rate used for NN training (float > 0)
        'weight_decay': 1e-6,  # weight decay regularizer (float > 0)
        'clip_gradient': 100.0,  # gradient clipping threshold (float > 0)
        'momentum': 0.9,  # momentum which is only used for SGD optimizer
        'epochs_wo_improve': 20,  # we terminate training if validation performance hasn't improved in the last 'epochs_wo_improve' # of epochs
        # TODO: Epochs could take a very long time, we may want smarter logic than simply # of epochs without improvement (slope, difference in score, etc.)
    }
    return hyper_params


# Note: params for original NNTabularModel were:
# weight_decay=0.01, dropout_prob = 0.1, batch_size = 2048, lr = 1e-2, epochs=30, layers= [200, 100] (semi-equivalent to our layers = [100],numeric_embed_dim=200)
def get_default_param(problem_type, num_classes=None):
    if problem_type == BINARY:
        return get_param_binary()
    elif problem_type == MULTICLASS:
        return get_param_multiclass(num_classes=num_classes)
    elif problem_type == REGRESSION:
        return get_param_regression()
    else:
        return get_param_binary()


def get_param_multiclass(num_classes):
    params = get_fixed_params()
    params.update(get_hyper_params())
    return params


def get_param_binary():
    params = get_fixed_params()
    params.update(get_hyper_params())
    return params


def get_param_regression():
    params = get_fixed_params()
    params.update(get_hyper_params())
    return params
