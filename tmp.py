import re

with open('/Users/jaho/jaho/ba/vipquery/upload/a43276be-e6f9-415c-bd83-d17c0bcf4605/seesaw.txt', 'r') as f:
    txt = f.read().lstrip('﻿门店名称,评论内容,评论日期').strip()

txt = re.sub('\d\d\d\d-\d\d-\d\d', "$$$$", txt)

store_comments = {}
for line in txt.split('$$$$'):
    # print(line)
    if not line:
        continue

    if "\"" in line:
        store_name = line.split(',"')[0]
        comment = line.split(',"')[1].rstrip(',').rstrip('"')
    else:
        store_name = line.split('),')[0] + ')'
        comment = line.split('),')[1].rstrip(',').rstrip('"')
    print(store_name)
    print(comment)
    print("---------")
    if store_name not in store_comments:
        store_comments[store_name] = []
    store_comments[store_name].append(comment.replace('\n',''))

for store_name, comments in store_comments.items():
    with open(f'{store_name}.txt', 'w') as f:
        for comment in comments:
            f.write(f'{comment}\n')
