import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By

path = '/home/yeshey/Desktop/projects/zorig-classification/geckodriver'  # Ensure correct path

service = Service(path)
wd = webdriver.Firefox(service=service)

def get_images(wd,delay,max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=shingzo+carpentry&sca_esv=aac09e88d3bc5d88&gl=us&sxsrf=AHTn8zqg3qyxA8zM0HcfPw4eWnirHKrleg:1739023299550&source=hp&biw=1600&bih=777&ei=w2OnZ46JH9rcvr0PxZSamAw&iflsig=ACkRmUkAAAAAZ6dx04dwBxga3KhnqFFYREWfUbdaDikn&oq=shi&gs_lp=EgNpbWciA3NoaSoCCAAyBBAjGCcyBBAjGCcyCxAAGIAEGLEDGIMBMgUQABiABDIFEAAYgAQyCxAAGIAEGLEDGIMBMgUQABiABDIFEAAYgAQyCxAAGIAEGLEDGIMBMgUQABiABEiQE1CWBVjcB3ABeACQAQCYAXWgAdgCqgEDMC4zuAEByAEA-AEBigILZ3dzLXdpei1pbWeYAgSgAvUCqAIKwgIHECMYJxjqAsICCBAAGIAEGLEDwgILEAAYgAQYsQMYigWYAwWSBwMxLjOgB5AX&sclient=img&udm=2"

    wd.get(url)
    image_urls = set()

    while len(image_urls) < max_images:
        scroll_down(wd)
        thumnails = wd.find_elements(By.CLASS_NAME,"YQ4gaf")

        for img in thumnails[len(image_urls):max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME,"sFlh5c FyHeAf")
            for image in images:
                if image.get_atribute('src') and 'http' in image.get_atribute('src'):
                    image_urls.add(image.get_atributes('src'))
                    print(f"found image! {len(image_urls)}")

    return image_urls


def downloads_image(download_path, url, filename):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + filename

        with open(file_path,"wb") as f:
            image.save(f,'JPEG')

        print("success")
    except Exception as e:
        print("failed - ",e)

urls = get_images(wd,1,5)
print(urls)
wd.quit()