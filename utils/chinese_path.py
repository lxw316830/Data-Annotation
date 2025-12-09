import numpy as np
import cv2

# 解决中文路径报错问题，返回二进制流
def chinese_path(image_path):

    with open(image_path, 'rb') as f:
        date = f.read()
    nparr = np.frombuffer(date, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img