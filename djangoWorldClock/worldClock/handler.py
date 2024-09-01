import time
import ast
import json

from aliyun.log import *


client = LogClient("", "", "")


# 自定义日志处理器函数
def custom_handler(message):
    data = ast.literal_eval(message)

    # 将字典的键值对转换为元组形式的列表
    contents = [(key, str(value)) for key, value in data.items()]

    project = ""
    logstore = ""

    topic = 'topic'
    source = '127.0.0.1'

    logitemList = []  # LogItem list
    logItem = LogItem()
    logItem.set_time(int(time.time()))
    logItem.set_contents(contents)
    for i in range(0, 1):
        logitemList.append(logItem)
    request = PutLogsRequest(project, logstore, topic, source, logitemList, compress=False)

    response = client.put_logs(request)
    response.log_print()

    # check cursor time
    res = client.get_end_cursor(project, logstore, 0)
    end_cursor = res.get_cursor()

    res = client.get_cursor_time(project, logstore, 0, end_cursor)
    res.log_print()

    res = client.get_previous_cursor_time(project, logstore, 0, end_cursor)
    res.log_print()


def patching(record):
    def serialize(r):
        subset = {
            "request_id": r["extra"]["request_id"],
            "level": r["level"].name,
            "timestamp": r["time"].timestamp(),
            "message": r["message"],
        }
        return json.dumps(subset)
    record["extra"] = serialize(record)