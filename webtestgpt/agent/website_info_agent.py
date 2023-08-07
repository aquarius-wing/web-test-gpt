from typing import List

from webtestgpt.agent.base_agent import BaseAgent
from webtestgpt.claude_api import ask_claude
from webtestgpt.website_context import WebsiteContext


class WebsiteInfoAgent(BaseAgent):

    def __init__(self,
                 context: WebsiteContext,
                 execute_after_agents: List['BaseAgent'] = []):
        super().__init__(execute_after_agents)
        self.context = context

    def execute(self):
        response = ask_claude('''
    你是一个写playwright的专家，在附件1中是一个网站的html
    请你在阅读完成这个html后告诉我这个网站是干什么的
    越详细越好
        ''', self.context.html_path)
        print(response)
        self.context.info = response
        super().execute()
