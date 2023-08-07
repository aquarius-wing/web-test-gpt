from typing import List


class WebsiteContext:
    url: str
    html_path: str
    html_path_after_action: str
    '''
    用于做什么的描述
    '''
    info: str
    actions: List['WebsiteAction']

    def __init__(self, url: str = '', html_path: str = '', html_path_after_action: str = '', info: str = '', actions: List['WebsiteAction'] = []):
        super().__init__()
        self.url = url
        self.html_path = html_path
        self.html_path_after_action = html_path_after_action
        self.info = info
        self.actions = actions


class WebsiteAction:
    """
    {
        "name": "Desmos主页链接",
        "css_selector": ".dcg-home-link",
        "description": "点击后跳转到Desmos主页"
    }
    """
    name: str
    css_selector: str
    description: str

    def __init__(self, name: str, css_selector: str, description: str):
        super().__init__()
        self.name = name
        self.css_selector = css_selector
        self.description = description

    def __str__(self):
        return f'{{\n\t"name": "{self.name}",\n\t"css_selector": "{self.css_selector}",\n\t"description": "{self.description}"\n}}'

    def __repr__(self):
        return self.__str__()