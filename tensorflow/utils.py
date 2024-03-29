import tensorflow as tf
import numpy as np
import math

def rotation(x, degs):
    x_rot = []
    angle = math.pi / 180
    for deg in degs:
        if deg == 0:
           x_rot.append(x)
        elif deg == 90:
           x_rot.append(tf.contrib.image.rotate(x, 90 * angle))
        elif deg == 180:
           x_rot.append(tf.contrib.image.rotate(x, 180 * angle))
        elif deg == 270:
           x_rot.append(tf.contrib.image.rotate(x, 270 * angle))
    return x_rot
    
def fliprot(x, aug):
    x_flip = []
    x_flip.append(x)
    x_hflip = tf.image.flip_left_right(x)
    x_flip.append(x_hflip)
    x_flip.append(tf.image.flip_up_down(x))
    x_flip.append(tf.image.flip_up_down(x_hflip))
    return x_flip

def image_crop(x, offset_h, offset_w, target_h, target_w, size=[32, 32]):
    x_crop = tf.image.crop_to_bounding_box(x, offset_h, offset_w, target_h, target_w)
    x_crop = tf.image.resize(x_crop, size=size, method=tf.image.ResizeMethod.BILINEAR)
    return x_crop

def cropping(x, aug_list):
    if len(x.shape) == 4:  # Check if there is a batch dimension
        b, h, w, c = x.shape
    else:
        h, w, c = x.shape
    img_size = [h, w]
    boxes = [[0, 0, h, w], [0, 0, h*0.75, w*0.75], [0, w*0.25, h*0.75, w*0.75], [h*0.25, 0, h*0.75, w*0.75], [h*0.25, w*0.25, h*0.75, w*0.75]]
    return [image_crop(x, int(box[0]), int(box[1]), int(box[2]), int(box[3]), size=img_size) for box in boxes]


def augmenting_data(x, aug, aug_list):
    if aug   == 'rotation':
       return rotation(x, aug_list)
    elif aug == 'fliprot':
       return fliprot(x, aug_list)
    elif aug == 'cropping':
       return cropping(x, aug_list)
    else:
       print('utils.augmenting_data: the augmentation type is not supported. Exiting ...')
       exit()
