"""
Author: Zhang047
Version: 1.0.1
Date: 2025-04-11
Description: 该程序用于提取和显示 SSR 和 SS和vmess 链接。
"""

import os  # 提供与操作系统交互的功能，如文件和目录操作
import sys  # 提供对 Python 解释器的访问，允许与解释器进行交互
import subprocess  # 允许生成子进程并与其交互
import importlib  # 提供动态导入模块的功能

def check_and_install(package):
    """检查并安装缺失的包"""
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"未找到 {package}，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 检查并安装所需的包
required_packages = [
    "requests",
    "beautifulsoup4",
    "pyperclip",
    "colorama",
    "prettytable"
]

for package in required_packages:
    check_and_install(package)

# 现在安全地导入这些包
import requests  # 用于发送 HTTP 请求，获取网页内容
import re  # 提供正则表达式支持，用于字符串匹配和处理
import pyperclip  # 用于复制文本到剪贴板
from colorama import init, Fore  # 用于在终端中输出带颜色的文本，init() 初始化，Fore 提供前景色
from prettytable import PrettyTable  # 用于创建和打印美观的表格
from bs4 import BeautifulSoup  # 用于解析 HTML 和 XML 文档，方便提取数据

# 初始化 Colorama
init(autoreset=True)

def set_pip_source():
    # 确定用户目录
    if os.name == 'nt':  # Windows
        pip_config_path = os.path.join(os.path.expanduser('~'), 'pip', 'pip.ini')
        os.makedirs(os.path.dirname(pip_config_path), exist_ok=True)
        with open(pip_config_path, 'w') as f:
            f.write("[global]\n")
            f.write("index-url = https://pypi.tuna.tsinghua.edu.cn/simple\n")
    else:  # Linux 和 macOS
        pip_config_path = os.path.join(os.path.expanduser('~'), '.pip', 'pip.conf')
        os.makedirs(os.path.dirname(pip_config_path), exist_ok=True)
        with open(pip_config_path, 'w') as f:
            f.write("[global]\n")
            f.write("index-url = https://pypi.tuna.tsinghua.edu.cn/simple\n")

def print_info():
    # 打印美化后的信息
    print("╔═════════════════════════════════════════════════════════════╗")
    print("║  ✨ Author:Zhang047                                                                                                                         ║")
    print("╠═════════════════════════════════════════════════════════════╣")
    print("║  🐙 GitHub: https://www.github/Zhang047                                                                                    ║")
    print("╠═════════════════════════════════════════════════════════════╣")
    print("║  🌟 email: 2318134115@qq.com                                                                                                      ║")
    print("╚═════════════════════════════════════════════════════════════╝")

def test_url_accessibility(url):
    """测试 URL 的可访问性"""
    try:
        response = requests.head(url, allow_redirects=True)  # 使用 HEAD 请求以减少带宽
        return response.status_code == 200
    except requests.RequestException as e:
        print(Fore.RED + f"请求错误: {e}")
        return False

def find_ss_links(url):
    """从指定 URL 提取 SSR 和 SS 链接及更新时间"""
    # 发送请求
    if not test_url_accessibility(url):
        print(Fore.RED + f"无法访问网站: {url}")
        return [], None  # 返回 None 作为更新时间

    response = requests.get(url)
    if response.status_code != 200:
        print(Fore.RED + f"无法访问网站: {url}")
        return [], None  # 返回 None 作为更新时间

    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 使用正则表达式查找所有 ssr:// 和 ss:// 链接
    ssr_pattern = r'ssr://[a-zA-Z0-9_]+'
    ss_pattern = r'ss://[a-zA-Z0-9@%.#:]+'
    ss_last_modified_time =  r'北京时间[0-9年月日点时分]+'


    ssr_matches = re.findall(ssr_pattern, response.text)
    ss_matches = re.findall(ss_pattern, response.text)
    ss_last_modified_time_matches = re.findall(ss_last_modified_time, response.text)
   

    # 限制提取的链接长度
    # ssr_links = [(link[:174]) for link in ssr_matches]
    # ss_links = [(link[:110]) for link in ss_matches]
    #last_modified_time_links = [(link[4:19]) for link in last_modified_time_matches]

    return ssr_matches, ss_matches, ss_last_modified_time_matches, url


def find_vmess_links(url):
    """从指定 URL 提取 SSR 和 SS 链接及更新时间"""
    # 发送请求
    if not test_url_accessibility(url):
        print(Fore.RED + f"无法访问网站: {url}")
        return [], None  # 返回 None 作为更新时间

    response = requests.get(url)
    if response.status_code != 200:
        print(Fore.RED + f"无法访问网站: {url}")
        return [], None  # 返回 None 作为更新时间

    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 使用正则表达式查找所有vmess://链接
    vmess_pattern = r'vmess://[a-zA-Z0-9_=]+'
    vmess_last_modified_time = r'北京时间[0-9年月日点时分]+'

    vmess_matches = re.findall(vmess_pattern, response.text)

    vmess_last_modified_time_matches = re.findall(vmess_last_modified_time, response.text)


    return vmess_matches, vmess_last_modified_time_matches



def display_links(ssr_links, ss_links, ss_last_modified_time, vmess_links, vmess_last_modified_time):
    """显示 SSR 和 SS 链接及其更新时间的表格"""
    # 创建表格
    table = PrettyTable()
    table.field_names = ["序号", "类型", "链接", "更新时间"]

    # 设置列宽，启用自动换行
    table.max_width["序号"] = 2  # 设置最大宽度为2字符
    table.max_width["链接"] = 60  # 设置最大宽度为60字符
  

    # 设置时间格式
    #time1 =  ss_last_modified_time
    #time2 =  vmess_last_modified_time
    time1 = [(link[4:]) for link in ss_last_modified_time]
    time2 = [(link[4:]) for link in vmess_last_modified_time]

    # 添加 SSR 链接
    for i, link in enumerate(ssr_links, start=1):
        table.add_row([i, "SSR", link, time1])
        # 添加分割线
        table.add_row(["----", "--------", "------------------------------------------------------------", "------------------------"])

    

    # 添加 SS 链接
    start_index1 = len(ssr_links) + 1  # SS 链接的起始序号
    for i, link in enumerate(ss_links, start=start_index1):
        table.add_row([i, "SS", link, time1])
        # 添加分割线
        table.add_row(["----", "--------", "------------------------------------------------------------", "------------------------"])

     # 添加 vmess 链接
    start_index2 = len(ssr_links) + len(ss_links) + 1  #  链接的起始序号
    for i, link in enumerate(vmess_links, start=start_index2):
        table.add_row([i, "Vmess", link, time2])


    # 调用函数以打印信息
    print_info()
    print(table)
###—————————
def write_parsed_text_to_file(content, filename="666.txt"):
    """
    将正则解析的文本写入到当前脚本所在目录的txt文件中
    
    :param content: 需要写入的文本内容（字符串）
    :param filename: 要保存的文件名（默认为parsed_text.txt）
    :return: 返回完整的文件保存路径
    """
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 组合完整文件路径
    file_path = os.path.join(script_dir, filename)
    
    # 写入文件（使用UTF-8编码），会替换为最新的内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return file_path
###————————————————
if __name__ == "__main__":
    set_pip_source()
    
    target_url_01 = "https://gitlab.com/zhifan999/fq/-/wikis/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    target_url_02 = "https://fgithub.xyz/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    target_url_03 = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    target_url_vmess = "https://gitlab.com/zhifan999/fq/-/wikis/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    target_url = target_url_01
    # 查找 ssr:// 和 ss:// 链接及更新时间
    ssr_links, ss_links, ss_last_modified_time, url = find_ss_links(target_url)
    
    vmess_links, vmess_last_modified_time = find_vmess_links(target_url_vmess)
    # 显示链接
    display_links(ssr_links, ss_links, ss_last_modified_time, vmess_links, vmess_last_modified_time)
###——————————————
# 从正则解析的元组vmess_links中提取字符串

# 遍历元组并打印每个元素（自动换行）
for vmess_text in vmess_links:
    print(vmess_text)
    save_path=write_parsed_text_to_file(vmess_text)
   
####——————————————————

    print(Fore.CYAN + "程序结束，按任意键退出...")
    print("文件已保存在脚本所在文件夹下")
    input()  # 保持终端打开

