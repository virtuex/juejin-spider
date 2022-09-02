import requests
import json
from pathlib import Path
import os
from http.client import HTTPConnection

# 打印详细请求日志
# HTTPConnection.debuglevel = 1
bookId = '6844733769996304392'
headers = {
    'Cookie': '手动添加cookie',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
r = requests.post('https://api.juejin.cn/booklet_api/v1/booklet/get?param部分从浏览器里自行拷贝',
                  headers=headers, json={'booklet_id': bookId})
rsp_json = json.loads(r.text)
book_name = str.replace(rsp_json['data']['booklet']['base_info']['title'], " ", "")
p = Path(book_name)
p.mkdir(exist_ok=True)
sections = rsp_json['data']['sections']
index = 1
for section in sections:
    section_id = section['section_id']
    rsp = requests.post('https://api.juejin.cn/booklet_api/v1/section/get?param部分从浏览器里自行拷贝',
                        headers=headers, json={'section_id': section_id})
    r_json = json.loads(rsp.text)
    section_json = r_json['data']['section']
    title = f'第{index}章—{str.replace(section_json["title"], " ", "")}'
    title = title.replace("/", "&")
    content = section_json['content']
    with open(f'{book_name}/{title}.html', "w", encoding="utf_8_sig") as f:
        f.write(content)
    print(f'爬取 [{title}] 完成')
    index = index + 1
print('所有内容爬取完成')
