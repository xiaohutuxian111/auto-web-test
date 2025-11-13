import datetime
import json
import os
from src.utils.feishu_api import FeiShuApi


def get_string_between(org_str, start_str, end_str):
    return org_str[org_str.index(start_str) + len(start_str):org_str.index(end_str)].strip()


def update_dict_time(data_dict: dict, key: str, add_hour=8):
    if len(data_dict[key]) > 10:
        origin_time = datetime.datetime.strptime(data_dict[key], '%Y-%m-%d %H:%M:%S')
        new_time = origin_time + datetime.timedelta(hours=add_hour)
        data_dict[key] = new_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        origin_time = datetime.datetime.strptime(data_dict[key], '%H:%M:%S')
        new_time = origin_time + datetime.timedelta(hours=add_hour)
        data_dict[key] = new_time.strftime('%H:%M:%S')


def print_directory_tree(path, prefix=''):
    items = os.listdir(path)
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last = index == len(items) - 1
        if is_last:
            print(prefix + '|__' + item)
            new_prefix = prefix + '  '
        else:

            print(prefix + '|--' + item)
            new_prefix = prefix + '|  '

        if os.path.isdir(item_path):
            print_directory_tree(item_path, new_prefix)


def change_locust_report_time(html_fil_path):
    # 获取当前项目
    current_directory = os.getcwd()
    print('当前目录的树状结构')
    print_directory_tree(current_directory)

    with open(html_fil_path, 'r') as f:
        html = f.read()
        time_script_old = get_string_between(html, 'window.templateArgs', 'window.theme')
    data_dict: dict = json.loads(time_script_old)
    update_dict_time(data_dict, 'end_time')
    update_dict_time(data_dict, 'start_time')
    for history in data_dict['history']:
        update_dict_time(history, 'time')

    time_script_new = json.dumps(data_dict)
    html_new = html.replace(time_script_old, time_script_new)
    with open(html_fil_path, 'w') as f:
        f.write(html_new)
    start_time = data_dict['start_time']
    end_time = data_dict['end_time']
    num_requests = data_dict['requests_statistics'][-1]['num_requests']
    num_failures = data_dict['requests_statistics'][-1]['num_failures']
    feishu_receive_id = os.environ.get('FEISHU_ID')
    BUILD_URL = os.environ.get('BUILD_URL')
    base_url = os.environ.get('base_url')
    runtime = os.environ.get('runtime')
    vusr = os.environ.get('vusr')
    spawn_rate = os.environ.get('spawn_rate')
    slow_mo = os.environ.get('slow_mo')
    run_task_name = os.environ.get('run_task_name')

    if not run_task_name:
        run_task_name = '全流程测试'

    if feishu_receive_id and feishu_receive_id != 'auto':
        feishu_send = FeiShuApi()
        if 'ou_' in feishu_receive_id:
            receive_id_type = 'open_id'
        else:
            receive_id_type = 'chat_id'
        feishu_json = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "性能测试结果"
                },
                "template": "turquoise",
            },
            "elements": [

                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"测试域名:{base_url}\n执行时长:{runtime}\n最大并发用户数:{vusr}\n用户增加速率:{spawn_rate}\n思考时间:{slow_mo}ms\n测试对象:{run_task_name}\n\nDuring:{start_time}-{end_time}\n请求总数:{num_requests}\n请求失败数:{num_failures}",
                    }
                }

            ]
        }
        if BUILD_URL and BUILD_URL != 'None':
            feishu_json['elements'].append(
                {
                    "tag": "attion",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "查看jenkins工作流"
                            },
                            "type": "default",
                            "url": f"{BUILD_URL}artifact/"
                        }
                    ]
                }
            )

            file_key = feishu_send.upload_file(feishu_send.tenant_access_token, html_fil_path, html_fil_path)
            feishu_send.send(
                receive_id_type=receive_id_type,
                receive_id=feishu_receive_id,
                msg_type='interactive',
                content=json.dumps(feishu_json)
            )
            feishu_send.send(
                receive_id_type=receive_id_type,
                receive_id=feishu_receive_id,
                msg_type='file',
                content=json.dumps({'file_key': file_key})
            )


if __name__ == '__main__':
    change_locust_report_time('report.html')
