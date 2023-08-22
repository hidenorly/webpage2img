#   Copyright 2023 hidenorly
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

import argparse
import os
import re
import random
import string
import time

import urllib.request
from urllib.parse import urljoin
from urllib.parse import urlparse
from selenium import webdriver
from selenium import webdriver

class WebPageDownloader:
    def __init__(self, width=1920, height=1080):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        tempDriver = webdriver.Chrome(options=options)
        userAgent = tempDriver.execute_script("return navigator.userAgent")
        userAgent = userAgent.replace("headless", "")
        userAgent = userAgent.replace("Headless", "")

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(f"user-agent={userAgent}")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width, height)
        self.driver = driver
        self._driver = tempDriver

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None
        if self._driver:
            self._driver.close()
            self._driver = None

    def getRandomFilename(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))

    def getSanitizedFilenameFromUrl(self, url):
        parsed_url = urllib.parse.urlparse(url)
        filename = parsed_url.netloc+parsed_url.path

        filename = re.sub(r'[\\/:*?"<>|]', '', filename)

        return filename

    def getOutputFilename(self, url, outputPath):
        filename = self.getSanitizedFilenameFromUrl(url)
        if not filename:
            filename=self.getRandomFilename()
        filePath = str(os.path.join(outputPath, filename))
        if not filePath.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')):
            filePath = filename+".png"

        filename = os.path.basename(filePath)
        return filename, filePath

    def save(self, url, outputPath):
        try:
            self.driver.get(url)
            filename, filePath = self.getOutputFilename(url, outputPath)
            self.driver.save_screenshot(filePath)
        except:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download from web pages', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('pages', metavar='PAGE', type=str, nargs='+', help='Web pages to download from')
    parser.add_argument("-o", "--output", default='.', help="Output path")
    args = parser.parse_args()

    driver = WebPageDownloader()
    for aUrl in args.pages:
        driver.save(aUrl, args.output)
