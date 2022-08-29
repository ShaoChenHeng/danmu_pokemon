import pyautogui
import redis
import time

loop_sec = 0.2
press_sec = 0.5
team1 = 'red'
key_list = ('w', 's', 'a', 'd', 'j', 'k', 'u', 'i', 'o',)


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

    time.sleep(persist_time * 0.3)
                                
    pyautogui.keyUp(key_name[1])
    pyautogui.keyUp('j')
    
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
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
        pyautogui.keyDown('s')
        pyautogui.keyUp('s')
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
        pyautogui.keyDown('w')
        pyautogui.keyUp('w')

def kill():
    for i in range(0,5):
        pyautogui.keyDown('j')
        pyautogui.keyUp('j')
        pyautogui.keyDown('j')
        pyautogui.keyUp('j')
        pyautogui.keyDown('w')
        pyautogui.keyUp('w')
        pyautogui.keyDown('k')
        pyautogui.keyUp('k')
        pyautogui.keyDown('k')
        pyautogui.keyUp('k')
        pyautogui.keyDown('k')
        pyautogui.keyUp('k')
        time.sleep(1)

if __name__ == '__main__':
    r = init_redis()
    print("开始监听弹幕消息, loop_sec =", loop_sec)
    while True:
        key_name = r.lpop(team1)
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
