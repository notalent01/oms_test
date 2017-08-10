#-*- coding:utf-8 -*-
import requests
import login_oms
import re
import sys
import datetime
from bs4 import BeautifulSoup
import locale;
locale.getlocale()
expectd_len = int(sys.argv[1])  #接受输入参数
expectd_min = expectd_len - 0.5 #接受最小范围
expectd_max = expectd_len + 0.5 #接受最大范围
pageSize = int(sys.argv[2])
name_list = []  # 名称
ratio_list = []  # 分辨率
rate_list = []  # 码流率
len_list = []  # 视频大小
time_list = []  # 视频时间
download_list = []  # 下载地址
total_list = []  # 用来存放结果
expected_list = [] #期望得到的结果
addr = "http://oms.synacast.com/source/sourcelist"
today = datetime.date.today()
today_str = str(today)
startday = today - datetime.timedelta(days=2)
startday_str = str(startday)
def get_expected_list():
    params = {"keyword":"","userName":"","start":startday_str,"end":today_str,"vpcId":"21","cp":"1","status":"2","sourceStorageId":"0","pageSize":pageSize}
    cookies = login_oms.format_cookies()
    res = requests.get(addr,cookies=cookies,params=params)
    html = res.text
    soup = BeautifulSoup(html,"html.parser")
    a = soup.find_all(class_='tr_class2')
    for node in a:
        b = node.find_all("td")
        ftp_href = node.find_all('a', href=re.compile("ftp"))
        index = 0
        for td_node in b:
            if index == 2:
                name_list.append(td_node.get_text())
            elif index == 3:
                ratio_list.append(td_node.get_text())
            elif index == 4:
                rate_list.append(td_node.get_text())
            elif index == 5:
                len_b = int(td_node.get_text())
                len_g = round(((len_b / 1024) / 1024) / 1024,2)
                len_list.append(len_g)
            elif index == 6:
                time_list.append(td_node.get_text())
            index += 1
        for ftp_all in ftp_href:
            ftp_url = ftp_all.get('href')
            download_list.append(ftp_url)
    length = len(name_list)
    for i in range(length):
        info_list = []
        info_list.append(name_list[i])
        info_list.append(ratio_list[i])
        info_list.append(rate_list[i])
        info_list.append(len_list[i])
        info_list.append(time_list[i])
        info_list.append(download_list[i])
        total_list.append(info_list)
    for i in range(len(total_list)):
        index_t = 0
        for j in range(len(total_list[i])):
            if index_t == 3:
                len_get = total_list[i][j]
                    # print(len_get)
                if expectd_min <= len_get <= expectd_max:
                    print(len_get)
                    expected_list.append(total_list[i])
            index_t += 1
    return expected_list

def save_list_result():
    with open("result/result.txt","w") as f:
        f.truncate()
        f.write(str(get_expected_list()))
        f.close()
if __name__ == '__main__':
    save_list_result()