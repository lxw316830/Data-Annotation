import os
from pathlib import Path
from PIL import Image
import json
from tqdm import tqdm
from loguru import logger
from utils.correction import correct_and_save_image
from utils.chinese_path import chinese_path
from utils.draw_points import draw_bbox

def process_single_image(image_path, output_dir, file_type, output_json):
    """
        处理单张图像文件，执行矫正、检测并保存结果
        """
    # 存放最终处理结果
    yolo_result = {}
    # 获取图像尺寸信息
    with Image.open(image_path) as img:
        width, height = img.size
    # 处理中文路径兼容性问题
    img_steam = chinese_path(str(image_path))
    logger.info(f"开始矫正图片：{image_path}")
    # 执行图像检测操作
    _, corr_det = correct_and_save_image(img_steam)
    polygons = corr_det["polygons"]
    # 在图像上绘制边界框，保存方便人工校验
    draw_bbox(polygons, str(image_path), str(output_dir))
    # yolo-seg训练数据转化
    shapes = [{"points": [[float(x), float(y)] for x, y in zip(polygon[::2], polygon[1::2])],
               "label": file_type,
               "description": "",
               "shape_type": "polygon",
               "flags": {}} for polygon in polygons]

    yolo_result.update({
        "version": "5.5.0",
        "flags": {},
        "shapes": shapes,
        "imagePath": image_path.name,
        "imageHeight": height,
        "imageWidth": width
    })

    with open(output_json / f'{image_path.stem}.json', 'w', encoding='utf-8') as f:
        json.dump(yolo_result, f, ensure_ascii=False, indent=4)


def main():
    # 需要标注文件类型
    file_type = "fp"
    # 图像文件目录
    image_dir_path = Path('../image_date') / file_type
    # 存放校验图像数据文件目录
    output_image = Path('./output_image_det')
    os.makedirs(output_image, exist_ok=True)
    # 存放json结果的文件目录
    output_json = Path('./output_json_det')
    os.makedirs(output_json, exist_ok=True)
    for image_file in tqdm(os.listdir(image_dir_path)):
        try:
            image_path = image_dir_path / image_file
            process_single_image(image_path, output_image, file_type, output_json)
        except Exception as e:
            logger.error(f"处理文件 {image_file} 时发生错误: {e}")


if __name__ == '__main__':
    main()