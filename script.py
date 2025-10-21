import msvcrt
import requests
import re
import os

from DrissionPage import ChromiumPage
from DrissionPage.common import Actions
from DrissionPage.errors import *

_author = '墨青BlackCyan'
_name = 'Ulearning自动答题脚本'
_version = '1.2.0'
menu = [
    '1.自动答题',
    '2.反馈',
    '0.退出脚本'
]

# 接管端口为9333的Chrom浏览器
dp = ChromiumPage(9333)
ac = Actions(dp)

while True:
    os.system('cls')
    print((_name + ' v' + _version).center(40, '-'))
    print(("作者：" + _author).center(40, '-'))
    print(menu[0])
    print(menu[1])
    print(menu[2])
    try:
        inputMenu = int(msvcrt.getch())
        if inputMenu == 0:
            break
        elif inputMenu == 1:
            os.system('cls')
            # 输入url
            url = input('将测验界面的Url粘贴至此：')
            try:
                a = re.findall('\d+', url)
            except TypeError:
                print('Url错误, 可能是你粘贴了错误的Url\n按任意键继续...')
                msvcrt.getch()
                continue
            try:
                xhr_url = f'https://homeworkapi.ulearning.cn/quiz/homework/stu/questions?homeworkId={a[1]}&ocId={a[0]}&showAnswer=true'
            except (IndexError, TypeError):
                print('Url错误, 可能是你粘贴了错误的Url\n按任意键继续...')
                msvcrt.getch()
                continue
            # 修改url获取请求
            get_url = xhr_url
            # 用户自行输入authorization
            authorization = input('Authorization:')

            xhr_headers = {
                'authorization': authorization,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
            }

            # 爬取xhr
            xhr_response = requests.get(url=xhr_url, headers=xhr_headers)
            # 储存JSON
            xhr_json = xhr_response.json()
            try:
                xhr_json['result']
            except KeyError:
                print('读取json键值对错误\n可能是你粘贴了错误的Url或Authorization?\n按任意键继续...')
                msvcrt.getch()
                continue
            # 爬取题目答案
            correctAnswer = {}
            ID = 0
            for result in xhr_json['result']:
                correctAnswer[ID] = xhr_json['result'][ID]['correctAnswer']
                ID += 1

            # 自动答题
            answer = 0
            for ID in correctAnswer:
                if len(correctAnswer[ID]) == 1 and correctAnswer[ID][0] in ('A', 'B', 'C', 'D', 'E'):
                    if correctAnswer[ID][0] == 'A':
                        answer = 1
                    elif correctAnswer[ID][0] == 'B':
                        answer = 2
                    elif correctAnswer[ID][0] == 'C':
                        answer = 3
                    elif correctAnswer[ID][0] == 'D':
                        answer = 4
                    elif correctAnswer[ID][0] == 'E':
                        answer = 5
                    try:
                        ac.click(f'xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/ul/li[{answer}]/div/label/span[1]/input')
                    except ElementNotFoundError:
                        print(f'line: 90 未找到元素 xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/ul/li[{answer}]/div/label/span[1]/input, 可能是源代码出现问题\n按任意键继续...')
                        msvcrt.getch()
                        continue
                elif len(correctAnswer[ID]) != 1:
                    for length in range(len(correctAnswer[ID])):
                        if correctAnswer[ID][length-1] == 'A':    answer = 1
                        elif correctAnswer[ID][length-1] == 'B':   answer = 2
                        elif correctAnswer[ID][length-1] == 'C':   answer = 3
                        elif correctAnswer[ID][length-1] == 'D':   answer = 4
                        elif correctAnswer[ID][length-1] == 'E':   answer = 5
                        try:
                            ac.click(f'xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/ul/li[{answer}]/div/label/span[1]/input')
                        except ElementNotFoundError:
                            print(f'line: 105 未找到元素 xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/ul/li[{answer}]/div/label/span[1]/input, 可能是源代码出现问题\n按任意键继续...')
                            msvcrt.getch()
                            continue
                elif len(correctAnswer[ID]) == 1 and (correctAnswer[ID][0] == 'true' or correctAnswer[ID][0] == 'false'):
                    if correctAnswer[ID][0] == 'true':
                        answer = 1
                    elif correctAnswer[ID][0] == 'false':
                        answer = 2
                    try:
                        ac.click(f'xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/div[2]/label[{answer}]/span[1]/input')
                    except ElementNotFoundError:
                        print(f'line: 114 未找到元素 xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/ul/li[{answer}]/div/label/span[1]/input, 可能是源代码出现问题\n按任意键继续...')
                        msvcrt.getch()
                        continue
                elif len(correctAnswer[ID]) == 1:
                    try:
                        ac.click(f'xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/div[2]/div[1]/div[1]/textarea')
                        ac.type(correctAnswer[ID][0])
                    except ElementNotFoundError:
                        print(f'line: 121 未找到元素 xpath://*[@id="app"]/div/div[1]/div[2]/div/div[1]/div/div/ul/li[{ID + 1}]/div[2]/div[2]/div[1]/div[1]/textarea, 可能是源代码出现问题\n按任意键继续...')
                        msvcrt.getch()
                        continue
            print('自动答题完成！按任意键继续')
            msvcrt.getch()
            continue
        elif inputMenu == 2:
            ChromiumPage(9333).new_tab('https://github.com/BlackCyan07/Ulearning/issues')
            continue
        else:
            continue
    except KeyboardInterrupt:
        print('用户退出')
        exit()
    except ValueError:
        pass
