
import tensorflow as tf


def add_layer(inputs, out_size, activation_function=None, name='', with_scope=False):
    # add one more layer and return the output of this layer
    # 可以加任意的层数 为DL打好基础
    in_size = int(inputs.shape[-1])  # inputs的最后一维
    if with_scope:
        # 大部件，定义层 layer，里面有 小部件 with定义的部件可以在tensorbord里看到
        with tf.name_scope('layer'):
            # 区别：小部件
            with tf.name_scope('weights'):
                weights = tf.Variable(tf.random.normal([in_size, out_size]), name='W'+name)
            with tf.name_scope('biases'):
                biases = tf.Variable(tf.zeros([1, out_size]) + 0.02, name='b'+name)
            # with tf.name_scope('wx_plus_b'):
    else:
        weights = tf.Variable(tf.random.normal([in_size, out_size]), name='W'+name)
        biases = tf.Variable(tf.zeros([1, out_size]) + 0.02, name='b'+name)

    wx_plus_b = tf.add(tf.matmul(inputs, weights), biases)
    if activation_function is None:
        outputs = wx_plus_b
    else:
        outputs = activation_function(wx_plus_b, name=name)
    return weights, biases, outputs


def add_conv_layer(x_in, core_size, channels_out, strides, padding='SAME', name='conv1_1'):
    _, height_in, width_in, channels_in = x_in.shape
    core_ = tf.random.truncated_normal(core_size + [int(channels_in), channels_out], stddev=0.1)
    kernel = tf.Variable(core_, name='weights_')
    conv = tf.nn.conv2d(x_in, kernel, strides, padding=padding)
    biases = tf.Variable(tf.constant(0.0, shape=[channels_out], dtype=tf.float32), name='biases_')
    print(core_, conv.shape, biases.shape)
    out = tf.nn.bias_add(conv, biases)
    return tf.nn.relu(out, name=name)


def add_pooling(x, ksize, strides, pooling_func=tf.nn.max_pool2d, name='max_pool'):
    activation = pooling_func(x, ksize, strides, padding='SAME', name=name)
    print(activation.shape)
    return activation
