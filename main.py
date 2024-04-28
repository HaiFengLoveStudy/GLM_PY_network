import string
from collections import deque
from zhipuai import ZhipuAI
import json


# 定义class类
class Course:
    def __init__(self, topic, definition, difficulty):
        # self.father = father
        self.topic = topic
        self.definition = definition
        self.difficulty = difficulty

    def print_topic(self):
        # print(f"Father: {self.father}")
        print(f"Topic: {self.topic}")
        print(f"Definition: {self.definition}")
        print(f"Difficulty: {self.difficulty}")

    def __str__(self):
        return f"Course(topic={self.topic}, definition={self.definition}, difficulty={self.difficulty})"

    def to_dict(self):
        return self.__dict__


# 从智普AI中获取数据
# 输入：技术名，每个技术列出的pre技术的个数
# 输出：脏json
#
def get_course(topic: str) -> string:
    msg = f"请列举出{topic}所需要学习的详细具体的知识点(topic),此知识点必须是和大学科计算机网络工程相关的如果不相关，则略过，此知识点的定义(definition),并返回此知识点的学习难度（1-5）(difficulty),""使用中文输出，输出json格式内容。注意只返回json，格式参考:\"topic\": \"计算机硬件基础", "difficulty\": 5,\"definition\": \"了解计算机硬件的组成，包括CPU、内存、硬盘等，及其工作原理。"
    client = ZhipuAI(api_key="fa80d4c885fde528c1f7bbbc7f6e6f79.HLPSBDLa1Zv4fNv7")  # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user",
             "content": f'{msg}'},
        ],
    )
    resp_str = response.choices[0].message.content
    return resp_str


# 把获取到的字符串转成纯json字符串
# 输入：脏json字符串
# 输出：纯json字符串
def strformat(str) -> str:
    begin = str.find('[')
    end = str.find(']')
    # print(begin, end)
    str_formatted = str[begin:end + 1]  # 截取纯json
    return str_formatted


# 纯json格式转换list
# 输入:json格式
# 输出:list_course
def str2list(str: str) -> list:
    # 解析JSON 文本
    course_data = json.loads(str)
    # 创建课程列表
    courses = []
    # 为每一个课程创建一个 Course 对象，并添加到列表中
    for item in course_data:
        course = Course(item['topic'], item['definition'], item['difficulty'])
        courses.append(course)
    return courses


def save_queue_to_file(deque, filename):
    list_obj = list(deque)
    json_str = json.dumps(list_obj, ensure_ascii=False)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_str)
    print('写入的队列为:', deque)


# 从文件恢复队列
def load_queue_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        json_str = f.read()
        list_obj = json.loads(json_str)
        deque_obj = deque(list_obj)
        print('恢复的队列为:', deque_obj)

    return deque_obj


def save_list_to_json(file_path: str, course_list: list):  # 将列表转换为JSON字符串，并美化输出
    json_data = json.dumps(course_list, indent=4, ensure_ascii=False)
    # 将JSON字符串写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_data)
# todo: course_list 转文件失败

if __name__ == '__main__':
    str_original = get_course('计算机网络工程')  # 获取数据
    str_format = strformat(str_original)  # 格式化脏json
    data_list = str2list(str_format)  # json转list
    save_list_to_json('data.json', data_list)  # 写入文件
    # 设置队列用来广度优先便利
    data_queue = load_queue_from_file('deque.json')
    for data in data_list:
        # 添加数据
        data_queue.appendleft(data.topic)

    while data_queue:
        print('队列数据', data_queue)
        save_queue_to_file(data_queue, "deque.json")  # 持久化存储队列
        current_data = data_queue.pop()
        print(f'正在查询:{current_data}')
        str_original = get_course(current_data)  # 获取数据
        str_format = strformat(str_original)  # 格式化脏json
        data_list1 = str2list(str_format)  # json转list
        print(f'{current_data}的子知识有:')
        for data in data_list1:
            print(data)
        print('==========================')
        save_list_to_json("data.json", data_list1)

        for data in data_list1:
            print('写入数据：', data)
            # print(data.topic)
            data_queue.appendleft(data.topic)   #加入队列
