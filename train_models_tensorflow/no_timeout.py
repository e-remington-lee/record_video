import os

import tensorflow as tf
import numpy as np
import matplotlib as plt
from tensorflow.keras import layers, models, regularizers
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

i_s = 80
tf.keras.backend.clear_session()
# tf.compat.v1.disable_eager_execution()


L2_WEIGHT_DECAY = 0.01
L1_WEIGHT_DECAY = 0.003

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)


def make_model():
    # add bias regularlizers??
    tf.keras.backend.clear_session()
    input_layer = tf.keras.layers.Input(shape=(i_s, i_s, 3))
    # x = tf.keras.layers.Conv2D(64, (3,3), kernel_initializer='he_normal')(input_layer)
    # x = tf.keras.layers.Conv2D(64, (3,3), kernel_initializer='he_normal', kernel_regularizer=regularizers.l1_l2(L2_WEIGHT_DECAY))(input_layer)
    x = tf.keras.layers.Conv2D(64, (3,3), kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(input_layer)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    # x = tf.keras.layers.Conv2D(64, (3,3), kernel_initializer='he_normal')(x)
    x = tf.keras.layers.Conv2D(64, (3,3), kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    x = tf.keras.layers.MaxPool2D((2,2), strides=2)(x)
    x = tf.keras.layers.BatchNormalization()(x)

    # p1a = tf.keras.layers.Conv2D(128, (1,1), padding="same", kernel_initializer='he_normal')(x)
    p1a = tf.keras.layers.Conv2D(128, (1,1), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(x)
    p1a = tf.keras.layers.BatchNormalization()(p1a)
    p1a = tf.keras.layers.Activation("relu")(p1a)

    # p1a = tf.keras.layers.Conv2D(128, (3,3), padding="same", kernel_initializer='he_normal')(p1a)
    p1a = tf.keras.layers.Conv2D(128, (3,3), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(p1a)
    p1a = tf.keras.layers.BatchNormalization()(p1a)
    p1a = tf.keras.layers.Activation("relu")(p1a)

    p1b = tf.keras.layers.MaxPool2D((3,3), padding="same", strides=1)(x)

    # p1b = tf.keras.layers.Conv2D(128, (1,1), padding="same", kernel_initializer='he_normal')(p1b)
    p1b = tf.keras.layers.Conv2D(128, (1,1), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(p1b)
    p1b = tf.keras.layers.BatchNormalization()(p1b)
    p1b = tf.keras.layers.Activation("relu")(p1b)

    # p1b = tf.keras.layers.Conv2D(128, (3,3), padding="same", kernel_initializer='he_normal')(p1b)
    p1b = tf.keras.layers.Conv2D(128, (3,3), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(p1b)
    p1b = tf.keras.layers.BatchNormalization()(p1b)
    p1b = tf.keras.layers.Activation("relu")(p1b)

    cat_256 = tf.keras.layers.Concatenate(axis=-1)([p1a, p1b])

    x = tf.keras.layers.MaxPool2D((2,2), strides=2)(cat_256)

    # p2a = tf.keras.layers.Conv2D(256, (1,1), padding="same", kernel_initializer='he_normal')(x)
    p2a = tf.keras.layers.Conv2D(256, (1,1), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(x)
    p2a = tf.keras.layers.BatchNormalization()(p2a)
    p2a = tf.keras.layers.Activation("relu")(p2a)

    # p2a = tf.keras.layers.Conv2D(256, (3,3), padding="same", kernel_initializer='he_normal')(p2a)
    p2a = tf.keras.layers.Conv2D(256, (3,3), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(p2a)
    p2a = tf.keras.layers.BatchNormalization()(p2a)
    p2a = tf.keras.layers.Activation("relu")(p2a)

    p2b = tf.keras.layers.MaxPool2D((3,3), strides=1, padding="same")(x)

    # p2b = tf.keras.layers.Conv2D(256, (1,1), padding="same", kernel_initializer='he_normal')(p2b)
    p2b = tf.keras.layers.Conv2D(256, (1,1), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(p2b)
    p2b = tf.keras.layers.BatchNormalization()(p2b)
    p2b = tf.keras.layers.Activation("relu")(p2b)

    # p2b = tf.keras.layers.Conv2D(256, (3,3), padding="same", kernel_initializer='he_normal')(p2b)
    p2b = tf.keras.layers.Conv2D(256, (3,3), padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(p2b)
    p2b = tf.keras.layers.BatchNormalization()(p2b)
    p2b = tf.keras.layers.Activation("relu")(p2b)

    cat_512 = tf.keras.layers.Concatenate()([p2a, p2b])

    x = tf.keras.layers.MaxPool2D((2,2), strides=2)(cat_512)

    # x = tf.keras.layers.Conv2D(512, (1,1),  padding="same", kernel_initializer='he_normal')(x)
    x = tf.keras.layers.Conv2D(512, (1,1),  padding="same", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    x = tf.keras.layers.MaxPool2D((2,2), strides=2)(x)

    # x = tf.keras.layers.Conv2D(512, (3,3), kernel_initializer='he_normal')(x)
    x = tf.keras.layers.Conv2D(512, (3,3), kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    x = tf.keras.layers.MaxPool2D((2,2), strides=2)(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Flatten()(x)

    # x = tf.keras.layers.Dense(1024, activation="relu", kernel_initializer='he_normal')(x)
    x = tf.keras.layers.Dense(1024, activation="relu", kernel_initializer='he_normal', bias_initializer="he_normal", kernel_regularizer=regularizers.l2(L2_WEIGHT_DECAY))(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(512, activation="relu", kernel_initializer='he_normal', bias_initializer="he_normal")(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(5, activation="softmax", kernel_initializer='he_normal', bias_initializer="he_normal")(x)

    model = Model(input_layer, x, name='xNet_reg')
    ## If i wanted earlier layers to output, I would probably just do what I did above, but then reference that output layer. 
    ## Similar to how we did the inception layers, but instead of concatenating it back, just do a softmax output

    return model
model = make_model()
model.summary()


model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.015, momentum=0.9, decay=0.00004), loss='categorical_crossentropy', metrics=['acc', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

TRAINING_DIR = "../labeled_data/emotions_5/train/"
train_datagen = ImageDataGenerator(
      rescale=1./255,
      horizontal_flip=True)
      # rotation_range=40,
      # width_shift_range=0.1,
      # height_shift_range=0.1,
      # shear_range=0.2,
      # zoom_range=0.1,
      # fill_mode='nearest')

train_generator = train_datagen.flow_from_directory(TRAINING_DIR, target_size=(i_s,i_s), 
batch_size=64, class_mode="categorical", shuffle=True)

VALIDATION_DIR = "../labeled_data/emotions_5/validation/"
validation_datagen = ImageDataGenerator(rescale=1./255)

validation_generator = validation_datagen.flow_from_directory(VALIDATION_DIR, target_size=(i_s,i_s),batch_size=64, class_mode="categorical", shuffle=True)

check_points = "../checkpoint/checkpoint.hb/"
check_point_dir = os.path.dirname(check_points)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=check_point_dir, verbose=1, monitor="val_acc", save_best_only=True)

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./log_dir")

lambda_callback_1 = tf.keras.callbacks.LambdaCallback(on_epoch_begin=lambda batch, logs : tf.keras.backend.clear_session())
lambda_callback_2 = tf.keras.callbacks.LambdaCallback(on_epoch_begin=lambda batch, logs : make_model())

model = tf.keras.models.load_model("..\\faceReader\\xNet_v4.1.1_SGD_80x80_7679")

history = model.fit(train_generator,
                            epochs=150,
                            verbose=1,  
                            validation_data=validation_generator,
                            callbacks=[cp_callback, lambda_callback_1, lambda_callback_2])

faceReader_dir = "..\\faceReader\\xNet_v4.2.0_SGD_80x80_night\\"

tf.saved_model.save(model, faceReader_dir)

test_dir = "../labeled_data/emotions_5/test"
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(test_dir, target_size=(i_s,i_s), 
batch_size=64, class_mode="categorical")

model.evaluate(test_generator)
