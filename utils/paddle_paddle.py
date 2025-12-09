from paddleocr import PPStructureV3
from loguru import logger
from paddleocr import PaddleOCR


layout_model = None
# 加载版面还原模型
def load_layout_model():
    global layout_model
    if layout_model is not None:
        logger.info("版面分析模型已加载，跳过")
        return layout_model
    logger.info("开始加载版面还原模型")
    try:
        layout_model = PPStructureV3()
        logger.info("版面还原模型加载成功")
        return layout_model
    except:
        logger.exception(f"版面还原模型加载失败")
        raise

# 加载ocr识别模型
ocr_model = None
def load_ocr_model():
    global ocr_model
    if ocr_model is not None:
        logger.info("ocr识别模型已加载，跳过")
        return ocr_model
    logger.info("开始加载ocr识别模型")
    try:
        ocr_model = PaddleOCR(
            use_doc_orientation_classify=False,  # 通过 use_doc_orientation_classify 参数指定不使用文档方向分类模型
            use_doc_unwarping=False,  # 通过 use_doc_unwarping 参数指定不使用文本图像矫正模型
            use_textline_orientation=False,  # 通过 use_textline_orientation 参数指定不使用文本行方向分类模型
        )
        return ocr_model
    except:
        logger.exception(f"ocr识别模型加载失败")
        raise

# 支持np.array,image_path
def layout_md(correction_image_array):
    global layout_model
    if layout_model is None:
        layout_model = load_layout_model()
    logger.info("开始版面还原")
    layout_result = layout_model.predict(correction_image_array)
    markdown_list = []
    for res in layout_result:
        md_info = res.markdown
        markdown_list.append(md_info)
    markdown_texts = layout_model.concatenate_markdown_pages(markdown_list)
    logger.info("版面还原成功")
    return markdown_texts

# 支持np.array,image_path
def ocr_v5(correction_image_array):
    global ocr_model
    if ocr_model is None:
        ocr_model = load_ocr_model()
    logger.info("开始ocr识别")
    ocr_result_list = ocr_model.predict(correction_image_array)
    if ocr_result_list is not None:
        logger.info("ocr识别成功")
        rec_texts = ""
        for ocr_result in ocr_result_list:
            rec_texts = "，。".join(ocr_result["rec_texts"])
        return rec_texts
    else:
        logger.warning("ocr识别结果为空")
        raise Exception("ocr识别结果为空")