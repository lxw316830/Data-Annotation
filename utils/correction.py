from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from loguru import logger
from PIL import Image
import numpy as np

correction_model = None

def load_correction_model():
    global correction_model
    if correction_model is not None:
        logger.info("图片矫正模型已加载，跳过")
        return correction_model

    logger.info("开始加载图片矫正模型")
    try:
        correction_model = pipeline(Tasks.card_detection_correction, model='iic/cv_resnet18_card_correction')
        logger.info("图片矫正模型加载成功")
        return correction_model
    except:
        logger.exception(f"图片矫正模型加载失败")
        raise


# 单张矫正拼接
def correct_and_save_image(input_image_steam):
    global correction_model

    if correction_model is None:
        correction_model = load_correction_model()
    logger.info("开始图片矫正")
    result = correction_model(input_image_steam)
    if len(result["scores"]) == 0:
        return []
    else:
        logger.info("图片矫正成功")
    max_score_index = result["scores"].index(max(result["scores"]))
    output_img_array = result["output_imgs"][max_score_index]
    output_img_steam = Image.fromarray(np.array(output_img_array[:, :, ::-1]), 'RGB')
    return output_img_array, result


# 多张矫正拼接
def corrects_and_save_image(input_image_steam):
    global correction_model

    if correction_model is None:
        correction_model = load_correction_model()
    logger.info("开始图片矫正")
    result = correction_model(input_image_steam)
    output_imgs = result['output_imgs']
    if len(result["scores"]) == 0:
        return []
    else:
        logger.info("图片矫正成功")
    pil_images = []
    for output_img in output_imgs:
        rgb_img = output_img[:, :, ::-1]
        pil_img = Image.fromarray(rgb_img, 'RGB')
        pil_images.append(pil_img)
    widths, heights = zip(*(img.size for img in pil_images))
    max_width = max(widths)
    total_height = sum(heights)
    # 创建新的空白图像
    concatenated_img = Image.new('RGB', (max_width, total_height))
    # 逐个粘贴图片
    y_offset = 0
    for img in pil_images:
        # 居中对齐（可选）
        x_offset = (max_width - img.width) // 2
        concatenated_img.paste(img, (x_offset, y_offset))
        y_offset += img.height
    output_img_array = np.array(concatenated_img)
    return output_img_array


if __name__ == '__main__':
    correct_and_save_image('./jhz/13040001202501020302_结婚证(买方)_2.jpg')
