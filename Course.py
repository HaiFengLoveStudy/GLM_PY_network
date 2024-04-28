import json


def save_list_to_json(file_path, data_list):
    json_data = json.dumps(data_list, indent=4, ensure_ascii=False)  # 将JSON字符串写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_data)


# 使用示例
object_list = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
save_list_to_json('datatest.json', object_list)
