import os
import time
from typing import List

from selenium.webdriver.common.by import By

from webtestgpt.agent.base_agent import BaseAgent
from webtestgpt.agent.website_download_agent import save_html, generate_local_path
from webtestgpt.claude_api import ask_claude
from webtestgpt.openai_api import ask_openai
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
        self.context.html_path_after_action = path
        response = ask_claude('''
    你是一个写playwright的专家，在两个附件都是网页的html
    当网页显示为第一个附件时，我点击了一下组件div.dcg-selectable-btn[aria-label='A B C']，然后网页变成了第二个附件
    接下来我需要你根据点击前后的html，只关注有差别的变化的部分，不要关注没有变化的部分，编写一个playwright的测试代码
    关于编写测试代码的注意
    0. 访问网站的时候加上{waitUntil: 'networkidle'}
    1. nth的序号是用0开始的
    2. 如果要测试输入，请仔细阅读html，然后在编写locator的时候尽可能详细地找到可以输入的dom对象
    3. 如果要测试输入，请用type而不是fill
    4. 如果要测试文本判断，请仔细阅读html，然后在编写locator的时候尽可能详细地找到最准确能够获取到对应文本的dom对象
    5. 在使用locator来获取dom对象时，能不用div的标签选择器就不用div的标签选择器
    6. 请不要用text=的选择器
    7. 在使用类选择器等非唯一的选择器时，你需要指定当前实际要指向的dom的序列号
    8. 除了要判断关键组件的变化之后的状态，也要关注它们变化之前的状态
    9. 请把代码整体输出
        ''', attachments=[self.context.html_path, self.context.html_path_after_action])
        '''
        加上
        - 不要用toHaveClass，而要用evaluate直接获取，然后split(" ").includes来判断class的存在与否
        没有用，所以后面用chatgpt来转换一下
        '''
        print('response1', response)
        response = ask_openai(f'''
        你是一个写playwright的专家，在两个---中间包含了一段playwright代码
        只需要输出代码的部分即可
        请你基于下面的规则来重写它
        1. 将toHaveClass转换成evaluate直接获取，然后split(" ").includes来判断class的存在与否
        ---
        {response}
        ---
        ''')

        print('response2', response)
        super().execute()
        return response

