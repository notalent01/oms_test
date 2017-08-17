from selenium import webdriver
def get_loginCookies():
    #window下执行
    # path = r'C:\Users\chriswangs\AppData\Local\Programs\Python\Python35-32\Scripts\phantomjs.exe'
    # driver = webdriver.PhantomJS(executable_path=path)
    driver = webdriver.PhantomJS
    url_login = "http://oms.synacast.com"
    driver.get(url_login)
    driver.find_element_by_xpath('/html/body/div[1]/div/ul/li[1]').click()
    driver.find_element_by_xpath('//*[@id="douya"]/a').click()
    driver.find_element_by_id("username").send_keys("16091955")
    driver.find_element_by_id("password").send_keys("Talent03")
    driver.find_element_by_name("submit").click()
    print(driver.get_cookies())
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    cookies_format = {}
    for line in cookiestr.split(";"):
        name, value = line.strip().split('=', 1)
        cookies_format[name] = value  # 为字典cookies添加内容
        driver.close()
    # print(cookies_format)
    return cookies_format
def save_cookie():
    with open("cookies/cookies.txt","w") as f:
        f.truncate()
        cookies = str(get_loginCookies())
        # print(cookies)
        f.write(cookies)
        f.close()
def format_cookies():
    cookies = {}
    with open("cookies/cookies.txt","r") as f:
        for line in f.readlines():
            cookies = eval(line)
    f.close()
    return cookies

if __name__ == '__main__':
    save_cookie()