import pyautogui
import redis
import time

loop_sec = 0.2
press_sec = 0.5
team2 = 'green'
key_list = ( 'z', 'x', 'f', 'g','h','c','v', 't', 'y', 'b', 'r', 'o')


def init_redis():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r


def control(key_name):
    
    if key_name is None:
        return
    
    key_name = key_name.lower()

    if key_name == 'w':
        key_name = 't'
    elif key_name == 's':
        key_name = 'g'
    elif key_name == 'a':
        key_name = 'f'
    elif key_name == 'd':
        key_name = 'h'
    elif key_name == 'j':
        key_name = 'y'
    elif key_name == 'k':
        key_name = 'r'
    elif key_name == 'u':
        key_name = 'b'
    elif key_name == 'i':
        key_name = 'v'
    
    if key_name in key_list:
        print("发出指令", key_name)
        pyautogui.keyDown(key_name)
        
        pyautogui.keyUp(key_name)
        


def rush(key_name):
    persist_time = int(key_name[2])
    pyautogui.keyDown('y')
    key = key_name[1]
    if key == 'w':
        key = 't'
    elif key == 's':
        key = 'g'
    elif key == 'a':
        key = 'f'
    elif key == 'd':
        key  = 'h'
    elif key == 'j':
        key = 'y'
    elif key == 'k':
        key = 'r'
    elif key  == 'u':
        key = 'b'
    elif key == 'i':
        key = 'v'
    
    pyautogui.keyDown(key)

    time.sleep(persist_time * 0.3)
                                
    pyautogui.keyUp(key)
    pyautogui.keyUp('y')
    
def save():
    pyautogui.hotkey('shift', 'F1')

def fish():
    pyautogui.hotkey('ctrl', 'shift', 't')


def shifTab():
    pyautogui.hotkey('shift', 'tab')

def load():
    pyautogui.keyDown('F1')
    pyautogui.keyUp('F1')

def nico():
    for i in range(0,5):
        pyautogui.keyDown('f')
        pyautogui.keyUp('f')
        pyautogui.keyDown('g')
        pyautogui.keyUp('g')
        pyautogui.keyDown('h')
        pyautogui.keyUp('h')
        pyautogui.keyDown('t')
        pyautogui.keyUp('t')

def kill():
    for i in range(0,5):
        pyautogui.keyDown('r')
        pyautogui.keyUp('r')
        pyautogui.keyDown('r')
        pyautogui.keyUp('r')
        pyautogui.keyDown('t')
        pyautogui.keyUp('t')
        pyautogui.keyDown('y')
        pyautogui.keyUp('y')
        pyautogui.keyDown('y')
        pyautogui.keyUp('y')
        pyautogui.keyDown('y')
        pyautogui.keyUp('y')
        time.sleep(1)

if __name__ == '__main__':
    r = init_redis()
    print("开始监听弹幕消息, loop_sec =", loop_sec)
    while True:
        key_name = r.lpop(team2)
        if key_name is None:
            continue
        if len(key_name) == 3:
            rush(key_name)
        elif key_name == 'save':
            save();
        elif key_name == 'nico':
            nico();
        elif key_name == 'kill':
            kill();
        else:
            control(key_name)
        time.sleep(loop_sec)
