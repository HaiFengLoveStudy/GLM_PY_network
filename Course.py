import json

from collections import deque


def queueFlieWriterHandler(queue: deque):
    file = open("queue.txt", 'w', encoding='utf-8')
    queue_items = []  # 用于持久化队列
    for item in queue:
        item = deque.get()
        queue_items.append(item)
        queue.task_done()  # 标记
    json_data = json.dumps(queue_items)
    file.write(json_data)
if __name__ == '__main__':
    deque=deque()
    for i in range(10):
        deque.append(i)

    queueFlieWriterHandler(deque)