import cv2 as cv
import numpy as np

class ItemVision:
    # Constants
    TRACKBAR_WINDOW = 'Trackbars'


    # Properties
    item_img = None
    item_w = 0
    item_h = 0
    method = None

    # Constructor
    def __init__(self, item_img_path, method=cv.TM_CCOEFF_NORMED):
        if item_img_path:

            # Load image to match
            self.item_img = cv.imread(item_img_path, cv.IMREAD_COLOR)

            # Save dimensions
            self.item_w = self.item_img.shape[1]
            self.item_h = self.item_img.shape[0]

        # Methods: https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
        self.method = method

    def find(self, screen_img, threshold=0.9, max_results=5):

        result = cv.matchTemplate(screen_img, self.item_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # if not results found reshape empty array to prevent errors
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.item_w, self.item_h]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

        # limited the max number of results for performance
        if len(rectangles) > max_results:
            print('Warning too many results, raise the threshold.')
            rectangles = rectangles[:max_results]
        return rectangles


    def get_click_points(self, rectangles):
        points = []
        for (x, y, w, h) in rectangles:

            # Determine center
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            # Save points
            points.append((center_x, center_y))

        return points

    def draw_rectangles(self, screen_img, rectangles):

        # BRG colors
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        # loop over all locations and draw boxes
        for (x, y, w, h) in rectangles:
            # Determine box pos
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            thickness = 1
            #normal_center = np.random.normal(center_x, center_y, 1000)

            cv.rectangle(screen_img, top_left, bottom_right, line_color, thickness, line_type)

        return screen_img


    def draw_crosshairs(self, screen_img, points):

        # BGR colors
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS
        marker_size = 5

        for (center_x, center_y) in points:
            cv.drawMarker(screen_img, (center_x, center_y), marker_color, marker_type, marker_size)

        return screen_img
