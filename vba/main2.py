# 部分弹幕功能代码来自项目：https://github.com/IsoaSFlus/danmaku，感谢大佬
# 快手弹幕代码来源及思路：https://github.com/py-wuhao/ks_barrage，感谢大佬
# 仅抓取用户弹幕，不包括入场提醒、礼物赠送等。

import asyncio
import danmaku
import redis
import pyautogui

team1 = 'red'
team2 = 'green'

key_list = ('w', 's', 'a', 'd', 'j', 'k', 'u', 'i', 'z', 'x', 'f', 'i', 'o','g','h', 'l', 't','r','y','v', 'b')
direction = ('w', 's', 'a', 'd')

# 红
team_list1 = []
# 绿
team_list2 = []

def init_redis():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r

def direction_number(list_str):
    temp = []
    if len(list_str) >= 2 and '1' <= list_str[1] \
       and list_str[1] <= '9' and \
       list_str[0] in key_list:
        # temp.append(list_str[0])
        for i in range(3 * int(list_str[1])):
            temp.append(list_str[0])
        return temp
    
    return list_str
    
async def printer(q, redis):
    while True:
        m = await q.get()
        if m['msg_type'] == 'danmaku':            
            print(f'{m["name"]}：{m["content"]}')


            list_str = list(m["content"])
            
            if m["content"] == '红':
                if int(m["uid"]) in team_list1:
                    team_list1.remove(int(m["uid"]))
                    team_list1.append(int(m["uid"]))
                if int(m["uid"]) in team_list2:
                    team_list2.remove(int(m["uid"]))
                    team_list1.append(int(m["uid"]))
                if int(m["uid"]) not in team_list2 and \
                   int(m["uid"]) not in team_list1:
                    team_list1.append(int(m["uid"]))
                print(team_list1)
                print(team_list2)
            elif m["content"] == '绿':
                if int(m["uid"]) in team_list2:
                    team_list2.remove(int(m["uid"]))
                    team_list2.append(int(m["uid"]))
                if int(m["uid"]) in team_list1:
                    team_list1.remove(int(m["uid"]))
                    team_list2.append(int(m["uid"]))
                if int(m["uid"]) not in team_list2 and \
                   int(m["uid"]) not in team_list1:
                    team_list2.append(int(m["uid"]))
                
                print(team_list1)
                print(team_list2)

            if m["uid"] in team_list1:
                print('hello')
                if len(list_str) == 3 and list_str[0] == 'l' and\
                   list_str[1] in direction and \
                   '1' <= list_str[2] and list_str[2] <= '9':
                    new_str = list_str[0] + list_str[1] + list_str[2]
                    redis.rpush(team1, new_str)
                
                elif m["content"] == 'save':
                    redis.rpush(team1, 'save')
                elif m["content"] == 'nico':
                    redis.rpush(team1, 'nico')
                elif m["content"] == 'kill':
                    redis.rpush(team1, 'kill')

                else:
                    print("弹幕拆分:", list_str)
                    list_str = direction_number(list_str)
                    print(list_str)
                    for char in list_str:
                        if char.lower() in key_list:
                            print('推送队列：', char.lower())
                            redis.rpush(team1, char.lower())

            elif m["uid"] in team_list2:
                print('world')
                if len(list_str) == 3 and list_str[0] == 'l' and\
                   list_str[1] in direction and \
                   '1' <= list_str[2] and list_str[2] <= '9':
                    new_str = list_str[0] + list_str[1] + list_str[2]
                    redis.rpush(team2, new_str)
                
                elif m["content"] == 'save':
                    redis.rpush(team2, 'save')
                elif m["content"] == 'nico':
                    redis.rpush(team2, 'nico')
                elif m["content"] == 'kill':
                    redis.rpush(team2, 'kill')

                else:
                    print("弹幕拆分:", list_str)
                    list_str = direction_number(list_str)
                    print(list_str)
                    for char in list_str:
                        if char.lower() in key_list:
                            print('推送队列：', char.lower())
                            redis.rpush(team2, char.lower())
            
async def main(url):
    redis = init_redis()
    q = asyncio.Queue()
    dmc = danmaku.DanmakuClient(url, q)
    asyncio.create_task(printer(q, redis))
    await dmc.start()

a = 'http://live.bilibili.com/24616287'
asyncio.run(main(a))

