import json
from typing import List
from bs4 import BeautifulSoup, Tag, NavigableString


def recursive_split(html: str, max_length: int = 2000, exclude_tags: List[str] = None) -> List[str]:
    if exclude_tags is None:
        exclude_tags = ['meta']

    def split_node(node: Tag) -> List[str]:
        children = list(node.children)
        if len(children) == 1:
            if isinstance(children[0], Tag):
                return split_node(children[0])
            elif node.getText() is not None and node.getText() != '':
                print('node.getText()', node.getText())
                return [str(node).strip()]
            else:
                print(str(node))

        result = []
        for child in node.children:
            if not isinstance(child, NavigableString) and child.name not in exclude_tags:
                child_str = str(child).strip()  # 去除换行符
                current_html = child_str
                if len(current_html) >= max_length:
                    if isinstance(child, Tag):
                        child_result = split_node(child)
                        result.extend(child_result)
                    else:
                        result.append(current_html)
                elif child.getText() is not None and child.getText() != '':
                    result.append(current_html)
        # if current_html:
        #     result.append(current_html)
        return result

    soup = BeautifulSoup(html, 'html.parser')
    return split_node(soup)


if __name__ == '__main__':
    # 示例HTML文本
    html_text = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <p>Some text here...</p>
            <p>More text...</p>
            <p>More textMore textMore textMore textMore textMore text...</p>
        </div>
    </body>
    </html>
    '''
    with open('../dist/www.desmos.com/scientific.txt', 'r', encoding='utf-8') as f:
        html_text = f.read()

    result = recursive_split(html_text, 3000, ['head', 'script', 'svg', 'style'])
    print(json.dumps(result, indent=4, ensure_ascii=False))
