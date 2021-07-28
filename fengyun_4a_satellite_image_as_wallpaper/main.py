import requests
import numpy as np
import cv2
import logging
import math
from datetime import datetime
from platform import platform
import os
import click
logging.basicConfig(level=logging.INFO)


def set_as_wallpaper(filepath):
    logging.info("set as wallpaper")
    if 'macOS' in platform():
        cmd = f"""osascript -e 'tell application "System Events" to set picture of every desktop to "{filepath}"'"""
        ret = os.system(cmd)
        if ret != 0:
            raise Exception(f"set wallpaper error: {ret}")
    else:
        raise Exception(f"unknown OS: {platform()}")


def download_disk(margin):
    URL = r"http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG"
    logging.info(f"downloading {URL}")
    raw = requests.get(URL)
    if not raw.ok:
        raise Exception(f"failed to download image, status_code={raw.status_code}")
    img = cv2.imdecode(np.frombuffer(raw.content, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise Exception("cannot decode image")
    raw_height,raw_width,_ = img.shape
    logging.info(f"raw image resolution = {raw_width}x{raw_height}")

    r = min(raw_height, raw_width) // 2
    mask = np.zeros(img.shape, np.uint8)
    mask = cv2.circle(mask, (len(img) // 2, len(img[0]) // 2), r, (255, 255, 255), thickness=-1)
    img = cv2.bitwise_and(img, mask)

    height = math.ceil((raw_height + 2 * margin) / 90) * 90
    width = math.ceil(height / 9 * 16)
    logging.info(f"wallpaper resolution = {width}x{height}")
    
    wallpaper = np.zeros((height, width, 3), np.uint8)
    offset_width = (width - raw_width) // 2
    offset_height = (height - raw_height) // 2
    wallpaper[offset_height:(offset_height + raw_height), offset_width:(offset_width + raw_width)] = img
    return wallpaper


def download_China(margin):
    URL = r"http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_CHINA.JPG"
    logging.info(f"downloading {URL}")
    raw = requests.get(URL)
    img = None
    if not raw.ok:
        raise Exception(f"failed to download image, status_code={raw.status_code}")
    img = cv2.imdecode(np.frombuffer(raw.content, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise Exception("cannot decode image")
    raw_height,raw_width,_ = img.shape
    logging.info(f"raw image resolution = {raw_width}x{raw_height}")
    return img
        

@click.command()
@click.option('-t', '--type', default="disk", type=click.Choice(["disk", "China"], case_sensitive=False), help="capture type")
@click.option('-m', '--margin', default=160, type=int)
@click.option('--wallpaper', default=False, is_flag=True, help="set as wallpaper")
@click.argument('filepath', type=click.Path())
def main(margin, type, filepath, wallpaper):
    if margin < 0:
        margin = 0
    now = datetime.now()
    logging.info(f"type={type}")
    logging.info(f"margin={margin}")
    logging.info(f"current time is: {now}")
    filepath = now.strftime(filepath)
    logging.info(f"save to {filepath}")

    img = None
    if type == "disk":
        img = download_disk(margin)
    elif type == "China":
        img = download_China(margin)
    if img is not None:
        cv2.imwrite(filepath, img)
        if wallpaper:
            set_as_wallpaper(filepath)

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"{e}")
