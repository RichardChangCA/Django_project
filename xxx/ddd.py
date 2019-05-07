# # 位置： /root/pycharm_project_365/static/train_set
#
# import os
#
# move_name = os.listdir('/root/pycharm_project_365/static/train_set')
# new_name = '20152649'
# for temp in move_name:
#     os.rename('/root/pycharm_project_365/static/train_set/' + temp,
#               '/root/pycharm_project_365/static/train_set/' + new_name)
#     new_name = str(int(new_name) + 1)

# import os
# # import pydicom
# # from pydicom.data import get_testdata_files
# # # filename = get_testdata_files('/static/10067.dcm')
# # filename = r'/root/pycharm_project_365/static/10069.dcm'
# # print(filename)
# # # ds = pydicom.filereader.dcmread(filename,force=True)
# # ds = pydicom.read_file(filename, force=True)
# # # ds.PatientName
# # print(ds)
# # print("print(type(ds)):",type(ds))

# -*-coding:utf-8-*-
import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt

dcm = pydicom.read_file('/root/pycharm_project_365/static/10069.dcm')
dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept

slices = []
slices.append(dcm)
img = slices[int(len(slices) / 2)].image.copy()
ret, img = cv2.threshold(img, 90, 3071, cv2.THRESH_BINARY)
img = numpy.uint8(img)

im2, contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
mask = numpy.zeros(img.shape, numpy.uint8)
for contour in contours:
    cv2.fillPoly(mask, [contour], 255)
img[(mask > 0)] = 255

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

img2 = slices[int(len(slices) / 2)].image.copy()
img2[(img == 0)] = -2000

plt.figure(figsize=(12, 12))
plt.subplot(131)
plt.imshow(slices[int(len(slices) / 2)].image, 'gray')
plt.title('Original')
plt.subplot(132)
plt.imshow(img, 'gray')
plt.title('Mask')
plt.subplot(133)
plt.imshow(img2, 'gray')
plt.title('Result')
plt.show()
