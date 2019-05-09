# # import cv2
# # img = cv2.imread('/root/zlf_projects/pycharm_project_48/static/upload_face_from_android/20152649/087_1.bmp')
# # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# import json
# import operator
# dict_match = {}
# file_dir_name = "wowow/xxx/ssss.jpg"
# num = 0
# while(num!=5):
#     dict_match.setdefault(num, "0")
#     print("dict_match", dict_match)
#     dict_match[num] = file_dir_name
#     num += 1
#
# sorted_x = sorted(dict_match.items(), key=operator.itemgetter(0))
#
# dict_match_json = {
#     'version': "1.0",
#     'results': sorted_x,
#     'explain': {
#         'used': True,
#         'details': "this is for dict_match josn when you train",
#   }
# }
# json_str = json.dumps(dict_match_json, indent=4)
# json_path = './test_data.json'
# with open(json_path, 'w') as json_file:
#     json_file.write(json_str)
#
# with open(json_path, 'r') as load_f:
#     load_dict = json.load(load_f)
#     print(load_dict)
#     print(load_dict["results"][0])
#     print(len(load_dict["results"]))
#     print(load_dict["results"][0][0])
#     print(load_dict["results"][0][1])


import tensorflow as tf
import cv2
import dlib
import numpy as np
import os
import random
import sys
from sklearn.model_selection import train_test_split
import argparse

# my_faces_path = './my_faces'
# other_faces_path = './other_faces'
size = 64


# imgs = []
# labs = []


def getPaddingSize(img):
    h, w, _ = img.shape
    top, bottom, left, right = (0, 0, 0, 0)
    longest = max(h, w)

    if w < longest:
        tmp = longest - w
        # //表示整除符号
        left = tmp // 2
        right = tmp - left
    elif h < longest:
        tmp = longest - h
        top = tmp // 2
        bottom = tmp - top
    else:
        pass
    return top, bottom, left, right


# def readData(path, h=size, w=size):
#     for next_path in os.listdir(path):
#         next_path = path + '/' + next_path
#         for filename in os.listdir(next_path):
#             if filename.endswith('.bmp'):
#                 filename = next_path + '/' + filename
#
#                 img = cv2.imread(filename)
# 				# 或者长宽不匹配的差值，下一步使得图片变成正方形
#                 top, bottom, left, right = getPaddingSize(img)
#                 # 将图片放大， 扩充图片边缘部分，用纯黑[0,0,0]填充
#                 img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
#                 img = cv2.resize(img, (h, w))
#
#                 imgs.append(img)
#                 labs.append(path)


# readData(my_faces_path)
# readData(other_faces_path)
# # 将图片数据与标签转换成数组
# imgs = np.array(imgs)
# labs = np.array([[0, 1] if lab == my_faces_path else [1, 0] for lab in labs])
# # 随机划分测试集与训练集，test_size表示测试集的比例
# train_x, test_x, train_y, test_y = train_test_split(imgs, labs, test_size=0.05, random_state=random.randint(0, 100))
# # 参数：图片数据的总数，图片的高、宽、通道
# train_x = train_x.reshape(train_x.shape[0], size, size, 3)
# test_x = test_x.reshape(test_x.shape[0], size, size, 3)
# # 将数据转换成小于1的数
# train_x = train_x.astype('float32') / 255.0
# test_x = test_x.astype('float32') / 255.0
#
# print('train size:%s, test size:%s' % (len(train_x), len(test_x)))
# # 图片块，每次取128张图片
# batch_size = 128
# num_batch = len(train_x) // batch_size

x = tf.placeholder(tf.float32, [None, size, size, 3])
y_ = tf.placeholder(tf.float32, [None, 2])

keep_prob_5 = tf.placeholder(tf.float32)  # dropout
keep_prob_75 = tf.placeholder(tf.float32)

v1 = tf.get_variable("v1", shape=[3])


def weightVariable(shape):
    init = tf.random_normal(shape, stddev=0.01)  # 正态分布，标准差0.01
    return tf.Variable(init, shape)


def biasVariable(shape):
    init = tf.random_normal(shape)
    return tf.Variable(init)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


# must have strides[0]= strides[3] = 1, strides=[1, stride, stride, 1] -> horizontal, vertices
# padding='SAME' 补0

def maxPool(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# 池化窗口大小2*2


def dropout(x, keep):
    return tf.nn.dropout(x, keep)


def cnnLayer():
    # 第一层
    # W1 = weightVariable([3, 3, 3, 32])  # 卷积核大小(3,3)， 输入通道(3)， 输出通道(32)
    # b1 = biasVariable([32])
    W1 = tf.get_variable("W1", shape=[3, 3, 3, 32])
    b1 = tf.get_variable("b1", shape=[32])
    # 卷积
    conv1 = tf.nn.relu(conv2d(x, W1) + b1)
    # 池化
    pool1 = maxPool(conv1)
    # 减少过拟合，随机让某些权重不更新
    drop1 = dropout(pool1, keep_prob_5)

    # 第二层
    # W2 = weightVariable([3, 3, 32, 64])
    # b2 = biasVariable([64])
    W2 = tf.get_variable("W2", shape=[3, 3, 32, 64])
    b2 = tf.get_variable("b2", shape=[64])
    conv2 = tf.nn.relu(conv2d(drop1, W2) + b2)
    pool2 = maxPool(conv2)
    drop2 = dropout(pool2, keep_prob_5)

    # 第三层
    # W3 = weightVariable([3, 3, 64, 64])
    # b3 = biasVariable([64])
    W3 = tf.get_variable("W3", shape=[3, 3, 64, 64])
    b3 = tf.get_variable("b3", shape=[64])
    conv3 = tf.nn.relu(conv2d(drop2, W3) + b3)
    pool3 = maxPool(conv3)
    drop3 = dropout(pool3, keep_prob_5)

    # 全连接层
    # Wf = weightVariable([8 * 16 * 32, 512])
    # bf = biasVariable([512])
    Wf = tf.get_variable("Wf", shape=[8 * 8 * 64, 512])
    bf = tf.get_variable("bf", shape=[512])
    drop3_flat = tf.reshape(drop3, [-1, 8 * 16 * 32])  # 变成8 * 16 * 32列，-1代表行数不知道
    dense = tf.nn.relu(tf.matmul(drop3_flat, Wf) + bf)
    dropf = dropout(dense, keep_prob_75)

    # 输出层
    # Wout = weightVariable([512, 2])
    # bout = biasVariable([2])
    Wout = tf.get_variable("Wout", shape=[512, 2])
    bout = tf.get_variable("bout", shape=[2])
    out = tf.add(tf.matmul(dropf, Wout), bout)
    return out


output = cnnLayer()
predict = tf.argmax(output, 1)  # 将output中向量行找最大索引

saver = tf.train.Saver()  # 将训练后的变量保存


# sess = tf.Session()
# saver.restore(sess, tf.train.latest_checkpoint('.')) # 自动获取最后一次保存的变量
# saver.restore(sess, "./tmp/model.ckpt")

def is_my_face(image):
    res = sess.run(predict, feed_dict={x: [image / 255.0], keep_prob_5: 1.0, keep_prob_75: 1.0})
    print("res", res)  # [0, 1]是自己
    return res[0]


# 使用dlib自带的frontal_face_detector作为我们的特征提取器


detector = dlib.get_frontal_face_detector()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

for image in os.listdir(args["image"]):
    print("file:", image)
    # cam = cv2.VideoCapture(0)
    # _, img = cam.read()
    img = cv2.imread(os.path.join(args["image"], image))
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray_image, 1)
    # if not len(dets):
    # print('Can`t get face.')
    # continue
    # cv2.imshow('img', img)
    # key = cv2.waitKey(30) & 0xff
    # if key == 27:
    # sys.exit(0)
    # else:
    # print("Get face")
    for i, d in enumerate(dets):
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0
        face = img[x1:y1, x2:y2]
        # 调整图片的尺寸
        face = cv2.resize(face, (size, size))
        # print('Is this my face? %s' % is_my_face(face))
        with tf.Session() as sess:
            saver.restore(sess, "./static/anti_proof_dataset/tmp/model.ckpt")
            print("v1 : %s" % v1.eval())
            print('is true face? %s' % is_my_face(face))
