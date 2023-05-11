from bs4 import BeautifulSoup
from urllib.request import urlopen
import locale
locale.setlocale(locale.LC_TIME,'ko_KR.UTF-8')
from datetime import datetime, date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
#크롬 브라우저를 띄우기 위해 웹 드라이버 임포트
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select

#아지트에 메시지 보내기용 
import requests 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

#크롬 드라이버 실행
driver=webdriver.Chrome(ChromeDriverManager().install())

#아지트홈에서 로그인
url = 'https://kakaoenterprise.agit.in'
driver.get(url)

time.sleep(1)

driver.find_element("id","email").send_keys('serena.lsh@kakaoenterprise.com')
driver.find_element('id','password').send_keys('isyou633@@')
driver.find_element(By.CLASS_NAME,'ag__submit').click()

#크롤링 대상으로 이동(본인이 만든 아지트)
driver.get('https://kakaoenterprise.agit.in/g/300071439/wall')
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

reports = soup.select('.wall__wall-message')

#글쓴이 이름 구하기
def get_writer(report):
    writer = report.select('.user-display-name__id')
    return writer[0].get_text()

#요청글의 담당자 구하기
def get_assignee(report):
    assignee = report.select('.task-assignee-label')
    return assignee[0].get_text()

#글상태 구하기
def get_reportstatus(report):
    mps = report.select('.request-status-indicator__status-button--active')
    print(mps)
    return mps[0].get_text()

#글 ID 가져오기
def get_parentid(report):
    parentid = report.select('a')[0]['id']
    return parentid

#요청상태일때 보낼 메시지(요청양식에 지정된 담당자에게 보낼 메시지를 text에 작성합니다.)
def send_message_request_agit(): 
    parentid = get_parentid(report)
    mensionid = " @"+get_assignee(report)

    url = "https://agit.in/webhook/c47f6055-ce93-4401-80b4-4768d1d5454f" 
    payload = {
        "parent_id" : parentid, 
        "text" : "(수정필요)위 글을 확인해주세요." + mensionid
        }
    return requests.post(url, json=payload)


dateFormatter = '%Y년 %m월 %d일(%a) %H:%M'
now = datetime.now()

for report in reports :
    try: 
        wrotedate = report.select('.agit__from-now')
        datetext = wrotedate[0].get_text()
        wrotetime = datetime.strptime(datetext, dateFormatter)
        datediff = now - wrotetime
        print(datediff.days)

        reportstatus = get_reportstatus(report)
    
    
        if reportstatus == '요청' and datediff.days >= 1 :
            send_message_request_agit()
            time.sleep(1)        
        else :
            print()    
    except Exception as e :
        print(e)

driver.close()

