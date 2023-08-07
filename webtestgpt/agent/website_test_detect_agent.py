import json
import time
from typing import List

from webtestgpt.agent.base_agent import BaseAgent
from webtestgpt.claude_api import ask_claude
from webtestgpt.split_html import recursive_split
from webtestgpt.website_context import WebsiteContext, WebsiteAction


class WebsiteTestDetectAgent(BaseAgent):

    @staticmethod
    def parse_json_array(json_str: str):
        index = json_str.find('[')
        index2 = json_str.rfind(']')
        if index == -1 or index2 == -1:
            return []

        try:
            return json.loads(json_str[index:index2 + 1])
        except:
            if json_str.count('[') > 1:
                return WebsiteTestDetectAgent.parse_json_array(json_str[index + 1:])

    def __init__(self, context: WebsiteContext, execute_after_agents: List['BaseAgent'] = []):
        super().__init__(execute_after_agents)
        self.context = context

    def execute(self) -> str:
        index = 0
        with open(self.context.html_path, 'r', encoding='utf-8') as f:
            html_text = f.read()

            result = recursive_split(html_text, 3000, ['head', 'script', 'svg', 'style'])
            for dom in result:
                # 这里不要加上info，会影响json数组的生成
                response = ask_claude('''
        你是一个写playwright的专家，在最后的html是一个网站的html
        请你在阅读完成这个html后，按照html的模块挨个思考后
        告诉我这个网站上可点击的按钮、链接、菜单等组件
        同时给我它们的css选择器，同时告诉我它们每一个的用途
        注意不要遗漏，不要错过任何一个，但是如果没有一个可点击的组件，那么就回答我JSON的空数组就可以了
        输出格式是一个json的数组，形如
        [{"name": "按钮1", "css_selector": "button#btn1", "description": "这个按钮是用来干什么的"}, {"name": "按钮2", "css_selector": "button#btn2", "description": "这个按钮是用来干什么的"}]
        html如下
        ''' + dom + '''
                ''')
                #         response = ask_claude('''
                # 你是一个写playwright的专家，在附件中是一个网站的一部分html
                # 请你在阅读完成这个html后，按照html的模块挨个思考后
                # 帮我统计一下有多少个我这个html上可点击的按钮、链接、菜单等组件
                # 注意不要遗漏，不要重复
                #                 ''', self.context.html_path)
                data = WebsiteTestDetectAgent.parse_json_array(response)
                for item in data:
                    action = WebsiteAction(item['name'], item['css_selector'], item['description'])
                    self.context.actions.append(action)

                index += 1
                time.sleep(10)
                # break at first for testing
                if index >= 2:
                    break
        super().execute()


if __name__ == '__main__':
    s = '''
 Here are the clickable components I found in the provided HTML:

```json
[
  {
    "name": "Math Tools dropdown",
    "css_selector": "span#header-link-0",
    "description": "Toggles open/closed the Math Tools dropdown menu."
  },
  {
    "name": "Graphing Calculator link", 
    "css_selector": "a.dcg-dropdown-link[href='/calculator?lang=en']",
    "description": "Links to the Graphing Calculator tool."
  },
  {
    "name": "Scientific Calculator link",
    "css_selector": "a.dcg-dropdown-link[href='/scientific?lang=en']", 
    "description": "Links to the Scientific Calculator tool."
  },
  {
    "name": "Four-Function Calculator link",
    "css_selector": "a.dcg-dropdown-link[href='/fourfunction?lang=en']",
    "description": "Links to the Four-Function Calculator tool."
  },
  {
    "name": "Test Practice link",
    "css_selector": "a.dcg-dropdown-link[href='/practice?lang=en']",
    "description": "Links to the Test Practice tool."
  },
  {
    "name": "Matrix Calculator link",
    "css_selector": "a.dcg-dropdown-link[href='/matrix?lang=en']",
    "description": "Links to the Matrix Calculator tool."
  },
  {
    "name": "Geometry Tool link",
    "css_selector": "a.dcg-dropdown-link[href='/geometry?lang=en']",
    "description": "Links to the Geometry Tool."
  },
  {
    "name": "Google Play Store link",
    "css_selector": "a.dcg-primary-link[href='https://play.google.com/store/apps/developer?id=Desmos+Inc']",
    "description": "Links to Desmos apps in the Google Play Store."
  },
  {
    "name": "iOS App Store link",
    "css_selector": "a.dcg-primary-link[href='https://apps.apple.com/us/developer/desmos/id653517543']",
    "description": "Links to Desmos apps in the iOS App Store."
  }
]
```
    '''
    print(WebsiteTestDetectAgent.parse_json_array(s))
