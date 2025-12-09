from xinference.client import RESTfulClient
import os
from utils.correction import correct_and_save_image, corrects_and_save_image
from utils.paddle_paddle import layout_md
from utils.paddle_paddle import ocr_v5
from utils.chinese_path import chinese_path
from loguru import logger
from tqdm import tqdm
import json
import time

jhz = "持证人、登记日期、结婚证字号、男方姓名、男方国籍、男方出生日期、男方身份证号、女方姓名、女方国籍、女方出生日期、女方身份证号"
lhz = "持证人、登记日期、离婚证字号、男方姓名、男方国籍、男方出生日期、男方身份证号、女方姓名、女方国籍、女方出生日期、女方身份证号"
hkb = "姓名、出生地、籍贯、出生日期、公民身份证件编号"
wspz = "纳税人识别号、纳税人名称、金额合计（大写）、房屋坐落"
xwbl = "权利人、义务人、买方抵押权人、卖方抵押人"
ht = "卖方名称、卖方证件号、买方名称、买方证件号、合同编号、合同签订日期、交易价格"
yyzz = "名称、统一社会信用代码、营业场所、法定代表人、成立日期、营业期限"
fp = "金额合计"
htsy = "合同编号、出卖人、买受人"

file_type = "htsy"

logger.info("xinference加载模型")
client = RESTfulClient("http://127.0.0.1:9997")
model = client.get_model("qwen3")
image_dir_path = f'../image_date/{file_type}'
badcase = open('./badcase.txt', 'w', encoding='utf-8')
for image_file in tqdm(os.listdir(image_dir_path)):
    try:
        image_path = os.path.join(image_dir_path, image_file)
        img_steam = chinese_path(image_path)
        logger.info(f"开始矫正图片：{image_path}")
        correction_image_array = corrects_and_save_image(img_steam)
        if len(correction_image_array) == 0:
            logger.info(f"图片矫正失败，{image_file}")
            badcase.write(f"图片矫正失败，{image_file}\n")
            continue
        logger.info(f"图片矫正成功")
        # logger.info("版面还原·······")
        # md = layout_md(correction_image_array)
        md = ocr_v5(correction_image_array)
        logger.info("ocr识别·······")
        logger.info("ocr识别成功")
        es_json = '[{"姓名": "刘禅", "性别": "男"}, {"姓名": "刘备", "性别": "男"}]'
        messages = [{"role": "system", "content": "你是一个智能抽取助手，根据示例进行关键信息提取，严格遵循用户指令。"},
                    {"role": "user",
                     "content": f"从{md}，抽取以下字段的关键信息：{htsy},以json的格式返回:{es_json}，抽取不到就返回空，不要乱回答，严格从我提供的信息中做抽取"}]
        start_time = time.time()
        llm_output = model.chat(
            messages,
            generate_config={
                "max_tokens": 512,
                "temperature": 0.7
            }
        )
        end_time = time.time()
        logger.info(f"大模型推理耗时:{end_time-start_time}")
        json_output_list = json.loads(llm_output["choices"][0]['message']['content'])
        if not isinstance(json_output_list, list):
            json_output_list = [json_output_list]
        json_output_dict = json_output_list[0]
        json_output_list.append({"text": md})
        for json_keys in list(json_output_dict.keys()):
            if json_output_dict[json_keys] in md:
                continue
            else:
                logger.info(f"模型胡编乱造,{image_file}, {json_keys}:{json_output_dict[json_keys]}")
        name_without_ext = os.path.splitext(image_file)[0]
        with open(f'./output_json_demo/{file_type}/{name_without_ext}.json', 'w', encoding='utf-8') as f:
            json.dump(json_output_list, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(str(e))
    break
