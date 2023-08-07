import os
import time
from typing import List

from selenium.webdriver.common.by import By

from webtestgpt.agent.base_agent import BaseAgent
from webtestgpt.agent.website_download_agent import save_html, generate_local_path
from webtestgpt.website_context import WebsiteContext, WebsiteAction
from selenium import webdriver


class WebsiteActionAgent(BaseAgent):

    def __init__(self,
                 driver: webdriver.Chrome,
                 action: WebsiteAction,
                 context: WebsiteContext,
                 execute_after_agents: List['BaseAgent'] = []):
        super().__init__(execute_after_agents)
        self.context = context
        self.driver = driver
        self.action = action

    def execute(self):
        self.driver.get(self.context.url)
        self.driver.find_element(By.CSS_SELECTOR, self.action.css_selector).click()
        time.sleep(1)
        p = generate_local_path(self.context.url)
        directory = os.path.join('./dist', p['directory'])
        os.makedirs(directory, exist_ok=True)
        print('保存至当前目录', directory)

        # 保存当前HTML到指定路径
        path = os.path.join(directory, p['path'].replace('.txt', '_after_action.txt'))
        print('保存至路径', path)
        save_html(self.driver, path)

        super().execute()

