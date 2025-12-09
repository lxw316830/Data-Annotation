import json
import os
import shortuuid

type_list = ["htsy"]
result_data = []
json_id = 0
for input_json_type in type_list:
    input_json_path = f'./output_json_demo/{input_json_type}'
    for json_dir in os.listdir(input_json_path):
        result_dict = {}
        json_id += 1
        result_dict["id"] = json_id
        annotations_dict = {}
        annotations_dict["id"] = json_id
        annotations_result = []
        annotations = []
        json_path = os.path.join(input_json_path, json_dir)
        with open(json_path, 'r', encoding='utf-8') as f:
            json_datas = json.load(f)
        result_text = json_datas[-1]["text"]
        for a in range(len(json_datas[:-1])):
            dict_keys = list(json_datas[a].keys())
            for json_data in dict_keys[:1]:
                json_data_value = json_datas[a][json_data]
                start = result_text.find(json_data_value)
                end = start + len(json_data_value)
                annotations_result_value = {"start": start, "end": end, "text": json_data_value, "labels": [json_data]}
                uid = shortuuid.uuid()[:10]
                annotations_result.append(
                    {"value": annotations_result_value, "type": "labels", "to_name": "text", "from_name": "label", "id": uid})
            for json_data in dict_keys:
                json_data_value = json_datas[a][json_data]
                start = result_text.rfind(json_data_value)
                end = start + len(json_data_value)
                annotations_result_value = {"start": start, "end": end, "text": json_data_value, "labels": [json_data]}
                uid = shortuuid.uuid()[:10]
                annotations_result.append({"value": annotations_result_value, "type": "labels", "to_name": "text", "from_name": "label", "id": uid})
        annotations_dict["result"] = annotations_result
        annotations.append(annotations_dict)
        result_dict["annotations"] = annotations
        result_dict["data"] = {"text": result_text}
        result_data.append(result_dict)

with open(f"./data/train.json", "w", encoding='utf-8') as f:
    json.dump(result_data, f, ensure_ascii=False, indent=4)
