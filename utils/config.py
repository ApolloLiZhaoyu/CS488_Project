import os
import os.path as osp
import numpy as np

from easydict import EasyDict as edict

__C = edict()

cfg = __C

# Root directory of project
__C.ROOT_DIR = osp.abspath(osp.join(osp.dirname(__file__), '..'))

# Data directory
__C.DATA_DIR = osp.abspath(osp.join(__C.ROOT_DIR, 'data'))

# Output directory
__C.OUT_DIR = ''

# Place outputs under an experiments directory
__C.EXP_DIR = ''

# Experiment name
__C.EXP_NAME = ''

# Random seed
__C.RAND_SEED = 2020

# Parameters
__C.Z = 2
__C.W = 1.0

__C.MU = np.array(
    [0.3, 0.5]
)

__C.A = np.array([
    [0.3, 0.7],
    [0.2, 0.6]
])

__C.GEN_TRAIN_SEQ_NUM = 3000
__C.GEN_MAX_SEQ_LEN = 200

__C.SEQ_LEN = 10

__C.BATCH_SIZE = 1024
__C.NUM_EPOCHS = 100
__C.LR = 0.005
__C.LR_STEP = 500
__C.LR_GAMMA = 0.1

__C.EVENT_CLASSES = 7
__C.EVENT_EMBED_DIM = 20
__C.LSTM_HIDDEN_DIM = 32
__C.ALPHA = 0.05
__C.DROPOUT = 0.1

__C.USE_EVENT_LOSS = True
__C.CALCULATE_A = False
__C.VERBOSE_STEP = 100


def _merge_a_into_b(a, b):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    if type(a) is not edict:
        return

    for k, v in a.items():
        # a must specify keys that are in b
        if k not in b:
            raise KeyError('{} is not a valid config key'.format(k))

        # the types must match, too
        if type(b[k]) is not type(v):
            raise ValueError(('Type mismatch ({} vs. {}) '
                              'for config key: {}').format(type(b[k]),
                                                           type(v), k))
        # recursively merge dicts
        if type(v) is edict:
            try:
                _merge_a_into_b(a[k], b[k])
            except:
                print('Error under config key: {}'.format(k))
                raise
        else:
            b[k] = v


def cfg_from_file(filename):
    """Load a config file and merge it into the default options."""
    import yaml
    with open(filename, 'r') as f:
        yaml_cfg = edict(yaml.load(f))

    _merge_a_into_b(yaml_cfg, __C)


def cfg_from_list(cfg_list):
    """Set config keys via list (e.g., from command line)."""
    from ast import literal_eval
    assert len(cfg_list) % 2 == 0
    for k, v in zip(cfg_list[0::2], cfg_list[1::2]):
        key_list = k.split('.')
        d = __C
        for subkey in key_list[:-1]:
            assert subkey in d.keys()
            d = d[subkey]
        subkey = key_list[-1]
        assert subkey in d.keys()
        try:
            value = literal_eval(v)
        except:
            # handle the case when v is a string literal
            value = v
        assert type(value) == type(d[subkey]), \
            'type {} does not match original type {}'.format(
            type(value), type(d[subkey]))
        d[subkey] = value
