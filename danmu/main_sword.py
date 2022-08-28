#-*-coding:utf-8-*-
import asyncio
import danmaku
import redis
import pyautogui

list_name = 'bilibili'
key_list = ('w', 's', 'a', 'd', 'j', 'k', 'u', 'i', 'z', 'x', 'c',
            'v', 'b', 'n', 'm', 'f', 'o','p','g','h', 'l',
            'q', 'e', 'r', 'y', '+', '-')
direction = ('w', 's', 'a', 'd')

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

            print(m["content"])
            m["content"] = m["content"].replace("前", 'wq')
            m["content"] = m["content"].replace("后", 'sq')
            m["content"] = m["content"].replace('左', 'aq')
            m["content"] = m["content"].replace("右", 'dq')
            
            print(f'{m["name"]}：{m["content"]}')
            list_str = list(m["content"])
            
            if len(list_str) == 3 and list_str[0] == 'l' and\
               list_str[1] in direction and \
               '1' <= list_str[2] and list_str[2] <= '9':
                
                new_str = list_str[0] + list_str[1] + list_str[2]
                redis.rpush(list_name, new_str)
                
            elif len(list_str) == 2 and \
               list_str[0] in direction and \
               '1' <= list_str[1] and list_str[1] <= '9':
                
                new_str = 's' + list_str[0] + list_str[1]
                redis.rpush(list_name, new_str)
                
            elif m["content"] == 'save':
                redis.rpush(list_name, 'save')
            elif m["content"] == 'enter':
                redis.rpush(list_name, 'enter')
                
            elif m["content"][0] == 'L' and \
                 m["content"][1] == 'L':
                if len(m["content"]) == 2:
                    new_str = m["content"] + '0'
                    redis.rpush(list_name, new_str)
                elif len(m["content"]) == 3 and \
                     '0' <= m["content"][2] <= '9':
                    redis.rpush(list_name, m["content"])
                    
            elif m["content"][0] == 'R' and \
                 m["content"][1] == 'R':
                if len(m["content"]) == 2:
                    new_str = m["content"] + '0'
                    redis.rpush(list_name, new_str)
                elif len(m["content"]) == 3 and \
                     '0' <= m["content"][2] <= '9':
                    redis.rpush(list_name, m["content"])
            else:
                print("弹幕拆分:", list_str)
                list_str = direction_number(list_str)
                print(list_str)
                for char in list_str:
                    if char.lower() in key_list:
                        print('推送队列：', char.lower())
                        redis.rpush(list_name, char.lower())
            

async def main(url):
    redis = init_redis()
    q = asyncio.Queue()
    dmc = danmaku.DanmakuClient(url, q)
    asyncio.create_task(printer(q, redis))
    await dmc.start()


a = 'http://live.bilibili.com/24616287'
asyncio.run(main(a))

