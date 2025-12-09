import os
from pathlib import Path
from PIL import Image
import json
from tqdm import tqdm
from loguru import logger
from correction import correct_and_save_image
from chinese_path import chinese_path
from draw_points import draw_bbox

def process_single_image(image_path, output_dir, file_type):
    yolo_result = {}
    with Image.open(image_path) as img:
        width, height = img.size

    img_steam = chinese_path(str(image_path))  # 假设chinese_path需要str类型参数
    logger.info(f"开始矫正图片：{image_path}")

    _, corr_det = correct_and_save_image(img_steam)
    polygons = corr_det["polygons"]
    draw_bbox(polygons, str(image_path), str(output_dir))

    shapes = [{"points": list(zip(polygon[::2], polygon[1::2])),
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

    with open(output_dir / f'{image_path.stem}.json', 'w', encoding='utf-8') as f:
        json.dump(yolo_result, f, ensure_ascii=False, indent=4)


def main():
    file_type = "htsy"
    image_dir_path = Path('./uie_date') / file_type
    output_path = Path('./output_image_det')
    os.makedirs(output_path, exist_ok=True)

    for image_file in tqdm(os.listdir(image_dir_path)):
        try:
            image_path = image_dir_path / image_file
            process_single_image(image_path, output_path, file_type)
        except Exception as e:
            logger.error(f"处理文件 {image_file} 时发生错误: {e}")


if __name__ == '__main__':
    main()