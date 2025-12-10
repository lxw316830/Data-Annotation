import json
import random
from datetime import datetime, timedelta
import os

# 确保输出目录存在
output_dir = "contracts_json"
os.makedirs(output_dir, exist_ok=True)

# 姓名与公司变体（同上）
surnames = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "郭", "何", "高", "林", "郑", "谢", "宋", "唐"]
given_names = ["丽华", "建国", "秀英", "伟", "芳", "娜", "强", "敏", "静", "磊", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "霞", "鹏"]

developer_base = "邯郸市锦光房地产开发有限公司"
developer_variants = [
    developer_base,
    developer_base.replace("有限公司", "有限责任公司"),
    developer_base + "第一分公司",
    developer_base + "置业分公司",
    "邯郸锦光房地产开发有限公司",
]

def random_date_str():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 10, 23)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%Y%m%d")

def generate_contract_number():
    return f"002{random_date_str()}{random.randint(1, 999):03d}"

def generate_buyer_name():
    return random.choice(surnames) + random.choice(given_names)

def generate_seller():
    return random.choice(developer_variants)

def generate_text(contract_no, seller, buyer):
    return f"GF-2014-0172，。合同编号：{contract_no}，。商品房买卖合同（现售），。出卖人：{seller}，。买受人：{buyer}，。中华人民共和国住房和城乡建设部，。中华人民共和国国家工商行政管理总局，。制定"

# 生成50个独立JSON文件
for i in range(1, 51):
    contract_no = generate_contract_number()
    seller = generate_seller()
    buyer = generate_buyer_name()
    text = generate_text(contract_no, seller, buyer)

    data = [
        {
            "合同编号": contract_no,
            "出卖人": seller,
            "买受人": buyer
        },
        {
            "text": text
        }
    ]

    filename = f"{output_dir}/contract_{i:02d}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成: {filename}")

print(f"\n🎉 共生成 50 个 JSON 文件，保存在 '{output_dir}' 目录中。")