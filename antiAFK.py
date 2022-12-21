import pyautogui
from random import random

# python c:\AppData\Code\py\antiAFK.py


def rnd(max: int = 10, min: int = 0):
    return min + (random() * (max - min))


def rnd_int(max: int = 10, min: int = 0) -> int:
    return round(rnd(max, min))


def upDnKey():
    global k, tk
    key = tk[rnd_int(len(tk) - 1)]
    v = rnd_int(1)
    if v != k[key]:
        k[key] = v
        if v: pyautogui.keyDown(key)
        else: pyautogui.keyUp(key)


t = ('easeInQuad', 'easeOutQuad', 'easeInOutQuad')  # , 'easeInBounce'
k = {
    'ctrl': 0,
    'shift': 0,
    'alt': 0,
}
tk = tuple(k.keys())
l = len(t) - 1
s = pyautogui.size()
#seed(1)
while True:
    try:
        x = rnd_int(s.width)
        y = rnd_int(s.height)
        sec = rnd(1)
        tp = t[rnd_int(l)]
        upDnKey()
        print(
            f'Press Ctr+C to Exit. MouseTo({x:4d},{y:4d}) {sec:.2f} seconds - Mode: {tp:<15} ctrl/shift/alt:{k["ctrl"]}{k["shift"]}{k["alt"]}'
        )
        pyautogui.moveTo(x, y, sec, getattr(pyautogui, tp))
    except KeyboardInterrupt:
        print('Interrompido')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('alt')
        quit()
    except Exception as e:
        print(e)
