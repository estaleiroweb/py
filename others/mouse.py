import pyautogui

try:
    while True:
        p=pyautogui.position()
        print(
            f'\rPress Ctr+C to Exit. Mouse Position({p.x:4d},{p.y:4d})', end = ''
        )
except KeyboardInterrupt:
    quit()
