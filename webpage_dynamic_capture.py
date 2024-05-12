#   Copyright 2024 hidenorly
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import argparse

def capture_webpage(url, target, direction, point, count, output_folder):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(3)

        element = driver.find_element(By.ID, target)
        if not element:
            element = driver.find_element_by_xpath(target)

        if element:
            for i in range(1, count+1):
                action = ActionChains(driver)
                action.click_and_hold(element).move_by_offset(point, 0).release().perform()

                screenshot_path = f"{output_folder}/output_{i}.png"
                print(screenshot_path)
                driver.save_screenshot(screenshot_path)

    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture webpage with drag and drop action")
    parser.add_argument("url", type=str, help="URL of the webpage to capture")
    parser.add_argument("--direction", type=str, choices=["left", "right", "up", "down"], default="left", help="Direction of drag")
    parser.add_argument("--point", type=int, default=50, help="Point to drag")
    parser.add_argument("--count", type=int, default=200, help="Number of captures")
    parser.add_argument("--target", type=str, default=None, help="Specify target element id")
    parser.add_argument("-o", "--output", type=str, default=".", help="Output folder")
    args = parser.parse_args()

    capture_webpage(args.url, args.target, args.direction, args.point, args.count, args.output)
