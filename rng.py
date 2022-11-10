import win32api, win32con
import time
from scipy.stats import truncnorm
import random
import pyautogui

# Lower limit of click_speed in seconds
lower = 0
# Upper limit of click_speed in seconds
upper = 0
# Mean of click_speed in seconds
mu = 0
# Standard deviation of click_speed in seconds
sigma = 0
# Size of click_speed_list
size = 0

class NumGen:


    def leftClick(self):
        self.lower = 50
        self.upper = 200
        self.mu = 120
        self.sigma = 100
        self.size = 1000

        # Generate click_speed_list as normal distribution
        self.X = truncnorm(a=(-self.lower + self.mu) / self.sigma, b=+self.upper / self.sigma, scale=self.sigma).rvs(size=self.size)

        # Round the decimals off
        self.X = self.X.round().astype(int)

        # Make all the numbers positive
        self.click_speed_list = abs(self.X)

        # Randomly pick a number from click_speed_list
        self.click_speed_s = random.choice(self.click_speed_list)

        # Convert seconds to ms
        self.click_speed = self.click_speed_s / 1000
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(self.click_speed)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        print(f'Left Click: {self.click_speed}s')

#test click speed here http://instantclick.io/click-test

    def mouseMoveSpeed(self):
        self.lower = 0.25
        self.upper = 1
        self.mu = 0.75
        self.sigma = 100
        self.size = 100

        self.X = truncnorm(a=(-self.lower + self.mu) / self.sigma, b=+self.upper / self.sigma, scale=self.sigma).rvs(size=self.size)
        self.move_speed = abs(self.X)
        self.move_speed = random.choice(self.move_speed)
        print("Mouse to target in: " + self.move_speed + "s")
        return self.move_speed

    def tweenType(self):
        self.tween_list = [pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad, pyautogui.easeInBounce, pyautogui.easeInElastic]
        self.tween = random.choice(self.tween_list)
        return self.tween
