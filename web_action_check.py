from main import ask_claude

def what_website_can_do():
    response = ask_claude("""你是一个写playwright的专家，在html1.txt中是一个网站的html
    请你在阅读完成这个html后告诉我这个网站是干什么的
    越详细越好
    """, './html1.txt')
    print(response)


if __name__ == '__main__':
    response = ask_claude('''你是一个写playwright的专家，在html1.txt中是一个网站的html
    网站的作用是
    1. 网站名称是Keepwork,是一个编程学习和创作社区。

2. 网站主页介绍了Keepwork的一些核心理念和功能:
   - 创作3D互动作品
   - 基于玩与创造的自主学习
   - 建立个人知识体系、探索他人知识  
   - 拥有个人网站展示自己的作品
   - 基于项目的学习
   - 来自职业程序员的知识传授

3. 网站提供在线课程、文档、常见问题等学习资源。

4. 网站有作品展示和创作功能,用户可以在网站上展示自己的作品。

5. 网站支持Paracraft和NPL语言等相关编程产品。

6. 网站有社区功能,用户可以在社区中交流和获取帮助。

7. 网站提供商业解决方案,面向企业客户。

8. 网站支持在线下载Paracraft编程软件。

9. 整体来看,这是一个以编程学习和创作为主题的社区网站,提供学习资源和创作平台,主要面向对编程感兴趣的青少年用户。网站支持3D和游戏创作,采用项目化学习的方式。

然后我点击了一下按钮.join-button，然后网页变成了附件html2.txt
接下来我需要你根据点击前后的html，编写一个playwright的测试代码
关于编写测试代码的注意
1. nth的序号是用0开始的
2. 如果要测试输入，请仔细阅读html，然后在编写locator的时候尽可能详细地找到可以输入的dom对象
3. 如果要测试输入，请用type而不是fill
4. 如果要测试文本判断，请仔细阅读html，然后在编写locator的时候尽可能详细地找到最准确能够获取到对应文本的dom对象
5. 在使用locator来获取dom对象时，能不用div的标签选择器就不用div的标签选择器
6. 请不要用text=的选择器
7. 在使用类选择器等非唯一的选择器时，你需要指定当前实际要指向的dom的序列号
''', ['./html1.txt', './html2.txt'])
    print(response)
