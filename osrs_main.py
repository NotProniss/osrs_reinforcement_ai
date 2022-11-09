import cv2 as cv
from time import sleep
from time import time
from window_capture import WindowCapture
from vision import ItemVision
import pyautogui
from click import leftClick
from threading import Thread
from detection import Detection

DEBUG = True
# Init window capture class
wincap = WindowCapture('RuneLite - Too Run 2200')

checking_exp = False

# load trained model
#cascade_skills = cv.CascadeClassifier('data/cascade/cascade.xml')
#assert not cascade_skills.empty()
# load empty Vision class
vision = ItemVision(None)
#vision_skills = ItemVision('images/skill_icon.jpg')
vision_total_level = ItemVision('images/total_level.jpg')

# load detector
detector = Detection('images/skill_icon.jpg')

def check_total_lvl_exp(rectangles):
    # Do actions
    if len(rectangles) > 0:
        # Click on skills icon
        targets = vision.get_click_points(rectangles)
        target = wincap.get_screen_pos(targets[0])
        pyautogui.moveTo(x=target[0], y=target[1], duration=0.5, tween=pyautogui.easeOutQuad) # over 1 second move start fast end slow
        leftClick()

        sleep(5)
    global checking_exp
    checking_exp = False

wincap.start()
detector.start()

# Start timer
loop_time = time()
while True:

    # If we dont have a screenshot dont run code below this point
    if wincap.screenshot is None:
        continue

    # Do the object detection (Ai)
    #rectangles = cascade_skills.detectMultiScale(screenshot)

    # Give detector current screenshot
    detector.update(wincap.screenshot)

    # Non Ai
    rectangles1 = vision_total_level.find(wincap.screenshot, 0.75)

    if DEBUG:
        # Draw rectangles on original image
        detection_image = vision.draw_rectangles(wincap.screenshot, detector.rectangles)

        # Display final image
        cv.imshow('Game', detection_image)
    # Start action thread
    if not checking_exp:
        checking_exp = True
        t = Thread(target=check_total_lvl_exp, args=(detector.rectangles,))
        t.start()


    # Count FPS
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    # Wait for 1ms to see if q pressed
    key = cv.waitKey(1)
    if key == ord('q'):
        detector.stop()
        wincap.stop()
        cv.destroyAllWindows()
        break
    #elif key == ord('p'):
    #    cv.imwrite('data/positive/{}.jpg'.format(loop_time), screenshot)
    #elif key == ord('n'):
    #    cv.imwrite('data/negative/{}.jpg'.format(loop_time), screenshot)

print('done')


