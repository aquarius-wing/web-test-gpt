from typing import List, Optional, Dict
from selenium import webdriver
import time
from webtestgpt.agent.base_agent import BaseAgent
import os
from urllib.parse import urlparse

from webtestgpt.website_context import WebsiteContext


def save_html(driver, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)


def generate_local_path(url: str) -> Optional[Dict[str, str]]:
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid URL")

    domain = parsed_url.netloc
    # claude attachment only support txt file type
    path = parsed_url.path if parsed_url.path and parsed_url.path != '/' else "index.txt"

    path = path + '.txt' if path.find('.') == -1 else path
    path = path[1:] if path.startswith('/') else path
    path = path.replace('/', '_')
    return {
        "directory": domain,
        "path": path
    }


class WebsiteDownloadAgent(BaseAgent):

    def __init__(self,
                 driver: webdriver.Chrome,
                 context: WebsiteContext,
                 execute_after_agents: List['BaseAgent'] = []):
        super().__init__(execute_after_agents)
        self.url = context.url
        self.context = context
        self.driver = driver

    def execute(self) -> str:
        '''
        执行下载网页的操作
        :return: 保存的网页的路径
        '''

        # 打开指定的URL
        self.driver.get(self.url)

        # 等待页面加载完成
        time.sleep(5)
        p = generate_local_path(self.url)
        directory = os.path.join('./dist', p['directory'])
        os.makedirs(directory, exist_ok=True)
        print('保存至当前目录', directory)

        # 保存当前HTML到指定路径
        path = os.path.join(directory, p['path'])
        save_html(self.driver, path)

        # 关闭浏览器
        self.driver.quit()
        super().execute()
        self.context.html_path = path


if __name__ == "__main__":
    url = "https://keepwork.com/"
    agent = WebsiteDownloadAgent([], url)
    agent.execute()
    # local_path = agent.generate_local_path(url)
    # print('local_path', local_path)
