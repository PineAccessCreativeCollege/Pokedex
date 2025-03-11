import pyautogui as pag
import random as rand
from pynput.mouse import Listener
import logging

logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def main():
    for i in range(1):
        pos = pag.position()  # current mouse x and y
        x = pos[0]
        y = pos[1]
        num = rand.randint(-50,50)
        if i // 2:
            pag.moveTo(x+num, y-50, duration=0.001)  # move mouse to XY coordinates over num_second seconds
        else:
            pag.moveTo(x+num, y-50, duration=0.001)  # move mouse to XY coordinates over num_second seconds
def on_click(x, y, button, pressed):
    if pressed:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        main()

with Listener(on_click=on_click) as listener:
    listener.join()

