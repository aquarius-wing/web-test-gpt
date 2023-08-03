from selenium import webdriver
import time
import os

from selenium.webdriver.common.by import By


def save_html(driver, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

def main(url, download_path):
    # 创建一个Chrome浏览器实例
    driver = webdriver.Chrome()

    # 打开指定的URL
    driver.get(url)

    # 等待页面加载完成
    time.sleep(5)

    # 通过CSS选择器或XPath找到要点击的元素
    click_element = driver.find_element(By.CSS_SELECTOR, '[dcg-command="1"]')

    # 点击元素
    click_element.click()

    # 等待操作生效
    time.sleep(2)

    # 保存当前HTML到指定路径
    save_html(driver, download_path)

    # 关闭浏览器
    driver.quit()

if __name__ == '__main__':
    url = 'https://www.desmos.com/scientific?lang=zh-CN'
    download_path = os.path.join(os.getcwd(), 'downloaded_html.txt')
    main(url, download_path)
