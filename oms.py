#-*- coding:utf-8 -*-
import requests
import login_oms
import re
import sys
import datetime
from bs4 import BeautifulSoup
addr = "http://oms.synacast.com/source/sourcelist"
today = datetime.date.today()
today_str = str(today)
startday = today - datetime.timedelta(days=2)
startday_str = str(startday)
params = {"keyword":"","userName":"","start":startday_str,"end":today_str,"vpcId":"21","cp":"1","status":"2","sourceStorageId":"0","pageSize":"50"}
cookies = login_oms.format_cookies()
res = requests.get(addr,cookies=cookies,params=params)
html = res.text
soup = BeautifulSoup(html,"html.parser")
a = soup.find_all(class_='tr_class2')
expectd_len = int(sys.argv[1])
expectd_min = expectd_len - 0.5
expectd_max = expectd_len + 0.5
# print(a)
# arr = []
name_list= []
ratio_list= []
rate_list = []
len_list = []
time_list = []
download_list = []
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
    # arr += b[1]
# print(name_list)
# print(ratio_list)

length = len(name_list)
total_list = []
for i in range(length):
    info_list = []
    info_list.append(name_list[i])
    info_list.append(ratio_list[i])
    info_list.append(rate_list[i])
    info_list.append(len_list[i])
    info_list.append(time_list[i])
    info_list.append(download_list[i])
    total_list.append(info_list)

print(total_list)
print("获取到的视频数量：",len(total_list))
# print(total_list[1][0])
expected_list = []
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
print(expected_list)
        # if len >= 1000000000 and len < 1500000000:
        #     print(total_list)

