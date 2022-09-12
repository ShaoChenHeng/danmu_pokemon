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

direction = ('w', 's', 'a', 'd')
self_direction = ('U', 'D', 'L', 'R')

def init_redis():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r

def rotate(direction, num):
    def ll():
        pyautogui.keyDown('f')
        time.sleep(0.1)
        pyautogui.keyUp('f')

    def rr():
        pyautogui.keyDown('h')
        time.sleep(0.1)
        pyautogui.keyUp('h')

    def uu():
        pyautogui.keyDown('t')
        time.sleep(0.1)
        pyautogui.keyUp('t')

    def dd():
        pyautogui.keyDown('g')
        time.sleep(0.1)
        pyautogui.keyUp('g')
        
    if direction == 'L':
        for i in range(num + 1):
            ll()
    elif direction == 'R':
        for i in range(num + 1):
            rr()
    elif direction == 'U':
        for i in range(num + 1):
            uu()
    elif direction == 'D':
        for i in range(num + 1):
            dd()

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
    pyautogui.keyDown(key_name[1])

    time.sleep(persist_time * 0.6)
    pyautogui.keyUp(key_name[1])
    

def rush_short(key_name):
    persist_time = int(key_name[2])
    pyautogui.keyDown(key_name[1])

    time.sleep(persist_time * 0.3)
                                
    pyautogui.keyUp(key_name[1])
    
    
def save():
    pyautogui.hotkey('shift', 'F1')

def load():
    pyautogui.keyDown('j')
    pyautogui.keyDown(key_name[1])

    time.sleep(persist_time * 0.3)
                                
    pyautogui.keyUp(key_name[1])
    pyautogui.keyUp('j')
    
def enter():
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')

def shoot():
    pyautogui.keyDown('y')
    pyautogui.keyDown('r')
    time.sleep(0.3)
    pyautogui.keyUp('y')
    pyautogui.keyUp('r')

def shoot1():
    pyautogui.keyDown('y')
    time.sleep(0.1)
    pyautogui.keyUp('y')

def fight():
    pyautogui.keyDown('y')
    pyautogui.keyDown('r')
    time.sleep(0.1)
    pyautogui.keyUp('y')
    pyautogui.keyUp('r')


if __name__ == '__main__':
    r = init_redis()
    print("开始监听弹幕消息, loop_sec =", loop_sec)
    while True:
        key_name = r.lpop(list_name)
        if key_name is None:
            continue

        # long run
        if len(key_name) == 3 and \
           key_name[0] == 'l' and \
           key_name[1] in direction:
            rush(key_name)

        # short run
        elif len(key_name) == 3 and \
             key_name[0] == 's' and \
             key_name[1] in direction:
            rush_short(key_name)

        elif key_name == 'shoot':
            shoot()
            
        elif key_name == 'shoot1':
            shoot1()

        elif key_name == 'fight':
            fight()
            
        elif key_name == 'enter':
            enter()
            
        # self rotate
        elif len(key_name) == 3 and \
             key_name[0] == key_name[1] and \
             key_name[0] in self_direction and \
             '0' <= key_name[2] <= '9':
            rotate(key_name[0], int(key_name[2]))
            
        else:
            control(key_name)
        time.sleep(loop_sec)
