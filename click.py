import win32api, win32con
import time
from scipy.stats import truncnorm
import random

# Lower limit of click_speed in seconds
lower = 50

# Upper limit of click_speed in seconds
upper = 200

# Mean of click_speed in seconds
mu = 120

# Standard deviation of click_speed in seconds
sigma = 100

# Size of click_speed_list
size = 1000

# Generate click_speed_list as normal distribution
X = truncnorm(a=(-lower + mu) /sigma, b=+upper/sigma, scale=sigma).rvs(size=size)

# Round the decimals off
X = X.round().astype(int)

# Make all the numbers positive
click_speed_list = abs(X)

# Randomly pick a number from click_speed_list
click_speed_s = random.choice(click_speed_list)
click_speed = click_speed_s / 1000


print(click_speed)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(click_speed)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print(f'Left Click: {click_speed}s')

#test click speed here http://instantclick.io/click-test