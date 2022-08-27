#-*-coding:utf-8-*-
import pyautogui
import redis
import time

loop_sec = 0.2
press_sec = 0.5
list_name = 'bilibili'

key_list = ('w', 's', 'a', 'd', 'j', 'k', 'u', 'i', 'z', 'x', 'c',
            'v', 'b', 'n', 'm', 'f', 'o','p','g','h', 'l',
            'q', 'e', 'r', 'y', '+', '-')



def init_redis():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r


def control(key_name):
    
    if key_name is None:
        return
    
    key_name = key_name.lower()

    if key_name in key_list:
        print("发出指令", key_name)
        pyautogui.keyDown(key_name)
        pyautogui.keyUp(key_name)
        


def rush(key_name):
    persist_time = int(key_name[2])
    pyautogui.keyDown('j')
    pyautogui.keyDown(key_name[1])

    time.sleep(persist_time * 0.6)
                                
    pyautogui.keyUp(key_name[1])
    pyautogui.keyUp('j')

def rush_short(key_name):
    persist_time = int(key_name[2])
    pyautogui.keyDown(key_name[1])

    time.sleep(persist_time * 0.2)
                                
    pyautogui.keyUp(key_name[1])
    
    
def save():
    pyautogui.hotkey('shift', 'F1')

def load():
    pyautogui.keyDown('j')
    pyautogui.keyDown(key_name[1])

    time.sleep(persist_time * 0.3)
                                
    pyautogui.keyUp(key_name[1])
    pyautogui.keyUp('j')
    
def save():
    pyautogui.hotkey('shift', 'F1')

def fish():
    pyautogui.hotkey('ctrl', 'shift', 't')

    
def load():
    pyautogui.keyDown('j')
    pyautogui.keyDown(key_name[1])

    time.sleep(persist_time * 0.3)
                                
    pyautogui.keyUp(key_name[1])
    pyautogui.keyUp('j')
    
def save():
    pyautogui.hotkey('shift', 'F1')

def load():
    pyautogui.keyDown('F1')
    pyautogui.keyUp('F1')

def enter():
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    

if __name__ == '__main__':
    r = init_redis()
    print("开始监听弹幕消息, loop_sec =", loop_sec)
    while True:
        key_name = r.lpop(list_name)
        if key_name is None:
            continue
        if len(key_name) == 3 and key_name[0] == 'l':
            rush(key_name)
        elif len(key_name) == 3 and key_name[0] == 's':
            rush_short(key_name)
        elif key_name == 'save':
            save();
        elif key_name == 'load':
            load();
        elif key_name == 'enter':
            enter()
        elif key_name == 'fish':
            fish();        
        else:
            control(key_name)
        time.sleep(loop_sec)
