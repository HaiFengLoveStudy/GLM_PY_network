import os
import logging
import string
from collections import deque
from zhipuai import ZhipuAI
import json


# 定义class类
class Course:
    def __init__(self, father, topic, definition, difficulty):
        self.father = father
        self.topic = topic
        self.definition = definition
        self.difficulty = difficulty

    def print_topic(self):
        print(f"Father: {self.father}")
        print(f"Topic: {self.topic}")
        print(f"Definition: {self.definition}")
        print(f"Difficulty: {self.difficulty}")

    def __str__(self):
        return f"Course(father={self.father},topic={self.topic}, definition={self.definition}, difficulty={self.difficulty})"

    def to_dict(self):
        return self.__dict__


# 日志信息处理
logging.basicConfig(
    filename='info.log',  # 日志文件名
    level=logging.INFO,  # 日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # 日志格式
)


# 从智普AI中获取数据
# 输入：技术名，每个技术列出的pre技术的个数
# 输出：脏json
#
def get_course(topic: str) -> string:
    api_key="fa80d4c885fde528c1f7bbbc7f6e6f79.HLPSBDLa1Zv4fNv7"  # 填写自己的apikey
    msg = f"请列举出{topic}所需要学习的详细具体的知识点(topic),此知识点必须是和大学科计算机网络工程相关的如果不相关，则略过，此知识点的定义(definition),并返回此知识点的学习难度（1-5）(difficulty),""使用中文输出，输出json格式内容。注意只返回json，格式参考:\"topic\": \"计算机硬件基础", "difficulty\": 5,\"definition\": \"了解计算机硬件的组成，包括CPU、内存、硬盘等，及其工作原理。"
    client = ZhipuAI(api_key=api_key)  # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user",
             "content": f'{msg}'},
        ],
    )
    resp_str = response.choices[0].message.content
    # print(resp_str)
    return resp_str


# 把获取到的字符串转成纯json字符串
# 输入：脏json字符串
# 输出：纯json字符串
# def strformat(str) -> str:
#     begin = str.find('{')
#     end = str.find('}')
#     # print(begin, end)
#     str_formatted = str[begin:end + 1]  # 截取纯json
#     return str_formatted
#



def strformat(str) -> str:
    str_formatted=''
    if str.find('[')>0:
        # 处理只有多组数据
        begin = str.find('[')
        end = str.find(']')
        # print(begin, end)
        str_formatted = str[begin:end + 1]  # 截取纯json
    else:
        # 处理一组数据
        begin = str.find('{')
        end = str.find('}')
        # print(begin, end)
        str_formatted = f"[{str[begin:end + 1]}]"  # 截取纯json


    return str_formatted



# 纯json格式转换list
# 输入:json格式
# 输出:list_course
def str2list(str1: str, father: str) -> list:
    # 解析JSON 文本
    course_data = json.loads(str1)
    # 创建课程列表
    courses = []
    # 为每一个课程创建一个 Course 对象，并添加到列表中
    for item in course_data:
        course = Course(father, item['topic'], item['definition'], item['difficulty'])
        courses.append(course)

    # for cours in courses:
    #     cours.print_topic()
    return courses


def save_queue_to_file(deque, filename):
    list_obj = list(deque)
    json_str = json.dumps(list_obj, ensure_ascii=False)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_str)
    # print('写入的队列为:', deque)
    logger.info(f'写入的队列为:{deque}')


# 从文件恢复队列
def load_queue_from_file(filename):
    # 检查文件是否存在且非空
    if os.path.isfile(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r', encoding='utf-8') as f:
            json_str = f.read()
            list_obj = json.loads(json_str)
            deque_obj = deque(list_obj)
            # print('恢复的队列为:', deque_obj)
            logger.info(f'恢复的队列为:{deque_obj}')

        return deque_obj
    else:
        deque_obj = deque(["计算机网络工程"])
        # print('恢复的队列为:', deque_obj)
        logger.info(f'恢复的队列为:{deque_obj}')
        return deque_obj


def save_list_to_json(file_path: str, course_list: list):  # 将列表转换为JSON字符串，并美化输出
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'a', encoding='utf-8') as file:
            for course in course_list:
                json_data = json.dumps(course.to_dict(), ensure_ascii=False)
                # json_data = json.dumps(course_list, indent=4, ensure_ascii=False)
                # 将JSON字符串写入文件
                file.write(json_data)
                file.write(',')
    else:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('[')


if __name__ == '__main__':
    # 日志信息
    logger = logging.getLogger()
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    count = 1
    str_original = get_course('计算机网络工程')  # 获取数据
    logger.info('正在启动查询...')
    str_format = strformat(str_original)  # 格式化脏json
    data_list = str2list(str_format, '计算机网络工程')  # json转list
    save_list_to_json('data.json', data_list)  # 数据写入文件
    # 设置队列用来广度优先便利
    data_queue = load_queue_from_file('deque.json')
    for data in data_list:
        # 添加数据
        data_queue.appendleft(data.topic)

    while data_queue:
        # print('队列数据', data_queue)
        logger.info(f'队列数据:{data_queue}')
        save_queue_to_file(data_queue, "deque.json")  # 持久化存储队列
        current_data = data_queue.pop()
        logger.info(f'正在查询:{current_data}')
        # print(f'正在查询:{current_data}')
        str_original = get_course(current_data)  # 获取数据
        str_format = strformat(str_original)  # 格式化脏json
        data_list1 = str2list(str_format, current_data)  # json转list
        # print(f'{current_data}的子知识有:')
        # for data in data_list1:
        #     print(data.topic)
        save_list_to_json("data.json", data_list1)
        for data in data_list1:
            logger.info(f'写入第{count}数据：{data.topic}')
            data_queue.appendleft(data.topic)  # 加入队列
            count += 1
