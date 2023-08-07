import json

from selenium import webdriver

from webtestgpt.agent.website_action_agent import WebsiteActionAgent
from webtestgpt.agent.website_download_agent import WebsiteDownloadAgent
from webtestgpt.agent.website_info_agent import WebsiteInfoAgent
from webtestgpt.agent.website_test_detect_agent import WebsiteTestDetectAgent
from webtestgpt.claude_api import ask_claude
from webtestgpt.website_context import WebsiteContext, WebsiteAction

if __name__ == '__main__':

    context = WebsiteContext()
    context.url = "https://www.desmos.com/scientific?lang=en"
    context.html_path = './dist/www.desmos.com/scientific.txt'
    with open('./dist/www.desmos.com/scientific_info.txt', 'r', encoding='utf-8') as f:
        context.info = f.read()
    # action1_json = ''
    # with open('./dist/www.desmos.com/scientific_action1.json', 'r', encoding='utf-8') as f:
    #     action1_json = f.read()
    # data = json.loads(action1_json)
    #
    # context.actions = [WebsiteAction(item['name'], item['css_selector'], item['description']) for item in data]

    # print(str(context.actions))
    driver = webdriver.Chrome()
    # WebsiteDownloadAgent(driver, context).execute()
    # WebsiteInfoAgent(context).execute()
    # WebsiteTestDetectAgent(context).execute()
    # context.actions = [
    #     WebsiteAction('字母键', "div.dcg-selectable-btn[aria-label='A B C']", '切换到字母输入'),
    # ]
    response = WebsiteActionAgent(driver, WebsiteAction('字母键', "div.dcg-selectable-btn[aria-label='A B C']", '切换到字母输入'), context)\
        .execute()


