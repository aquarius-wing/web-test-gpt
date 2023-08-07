from main import ask_claude

if __name__ == '__main__':
    response = ask_claude("""你是一个写playwright的专家，在html1.txt中是一个网站的html
    请你在阅读完成这个html后，仔细思考后
    告诉我这个网站上可点击、可操作的dom组件或菜单组件，同时给我它们的css选择器越多越好，同时告诉我它们每一个的用途
    注意不要遗漏，不要错过任何一个
    """, './html1.txt')
    print(response)