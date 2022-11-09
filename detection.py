from vision import ItemVision
import cv2 as cv
from threading import Thread, Lock

class Detection:

    # Threading properties
    stopped = True
    lock = None
    rectangles = []
    # Properties
    vision_skills =  None
    screenshot = None

    def __init__(self, item_image_path):
        # Create a thread lock object
        self.lock = Lock()
        # Load item image
        self.vision_skills = ItemVision(item_image_path)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):

        while not self.stopped:
            if not self.screenshot is None:
                # Do object detection
                rectangles = self.vision_skills.find(self.screenshot, 0.75)
                # Lock thread while updating results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()