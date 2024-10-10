from uiautomation import ControlFromCursor
import time


while True:
    c = ControlFromCursor()
    print(c)
    print(c.Name)
    time.sleep(2)