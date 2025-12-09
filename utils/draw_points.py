import os.path

import cv2
import numpy as np

"""
boxes:[
    [778.3899, 500.9558, 778.4674, 597.69556, 994.11743, 597.7508, 993.98535, 500.77255],
    [778.3367, 389.1896, 778.3899, 500.9558, 993.98535, 500.77255, 994.0488, 389.23566]
]
"""

# 你的坐标数据
def draw_bbox(boxes, img_path, output_path):

    # 读取图片,支持中文路径
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    # 遍历每个 box
    for box in boxes:
        # 将一行坐标 reshape 成 (4,2)，再转成 int
        pts = box.reshape(4, 2).astype(int)

        # 画多边形
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

    # 保存结果
    # cv2.imwrite(f"{output_path}/{os.path.basename(img_path)}", img)
    output_file = os.path.join(output_path, os.path.basename(img_path))
    ext = os.path.splitext(output_file)[1].lower()

    # 根据扩展名选择编码格式
    if ext in ['.jpg', '.jpeg']:
        success, buf = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    elif ext == '.png':
        success, buf = cv2.imencode('.png', img)
    else:
        # 默认用 JPG
        success, buf = cv2.imencode('.jpg', img)

    if not success:
        raise RuntimeError(f"图像编码失败: {output_file}")
    with open(output_file, 'wb') as f:
        f.write(buf.tobytes())
