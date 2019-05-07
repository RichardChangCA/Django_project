import cv2
img = cv2.imread('/root/zlf_projects/pycharm_project_48/static/upload_face_from_android/20152649/087_1.bmp')
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)