import time
import sys
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

naver_id = input("네이버 아이디를 입력하세요. : ")
naver_pw = input("계정의 비밀번호를 입력하세요. : ")
category_id = input("검색 허용 여부를 전환하고 싶은 카테고리의 id를 입력하세요. : ")
page_num = 1
perform_cnt = 0
cycle = 0

driver = webdriver.Chrome()
driver.get("https://www.naver.com/")

go_to_login = driver.find_element(By.XPATH, '//*[@id="account"]/div/a')
go_to_login.click()

id_box = driver.find_element(By.XPATH, '//*[@id="id"]')
pw_box = driver.find_element(By.XPATH, '//*[@id="pw"]')

id_box.click()
pyperclip.copy(naver_id)
id_box.send_keys(Keys.CONTROL + 'v')

pw_box.click()
pyperclip.copy(naver_pw)
pw_box.send_keys(Keys.CONTROL + 'v')

btn_login_submit = driver.find_element(By.XPATH, '//*[@id="log.login"]')
btn_login_submit.click()

# 로그인 성공 시 새로운 브라우저 등록 여부를 묻는 버튼 등장 -> '등록 안함' 클릭
# 버튼이 등장하지 않는다면 프로그램 종료
try:
    driver.find_element(By.XPATH, '//*[@id="new.dontsave"]').click()
except:
    print("아이디와 비밀번호를 다시 한 번 확인해주세요.")
    sys.exit("프로그램이 종료되었습니다.")

# 검색 허용 여부 전환을 원하는 카테고리 접속
driver.get(
    f'https://blog.naver.com/PostList.naver?blogId={naver_id}&from=postList&categoryNo={category_id}&parentCategoryNo={category_id}')


def change_permission_setting():
    if perform_cnt == 0:
        btn_open_list = driver.find_element(
            By.XPATH, '//*[@id="toplistSpanBlind"]')
        btn_open_list.click()

        btn_open_posting_manage = driver.find_element(
            By.XPATH, '//*[@id="btnSwitchManager"]/i')
        btn_open_posting_manage.click()

    check_all = driver.find_element(By.ID, 'checkall')
    driver.execute_script('arguments[0].click();', check_all)

    btn_change_setting = driver.find_element(
        By.XPATH, '//*[@id="listManagerWrapper"]/a[1]/i')
    btn_change_setting.click()
    time.sleep(1)

    # 설정 변경 팝업으로 윈도우 전환
    driver.switch_to.window(driver.window_handles[1])

    check_search_permission = driver.find_element(
        By.XPATH, '//*[@id="ManageForm"]/fieldset/div[2]/table/tbody/tr[6]/th/span/label')
    check_search_permission.click()

    btn_change_submit = driver.find_element(
        By.XPATH, '//*[@id="ManageForm"]/fieldset/div[3]/a[2]')
    btn_change_submit.click()

    # '바꾸시겠습니까?' alert 확인 누르기
    alert = driver.switch_to.alert
    alert.accept()

    time.sleep(3)

    # 기본 창으로 전환
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(3)


def find_page_btn():
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
        By.XPATH, f'//*[@id="toplistWrapper"]/div[2]/div/a[{page_num}]')))
    driver.find_element(
        By.XPATH, f'//*[@id="toplistWrapper"]/div[2]/div/a[{page_num}]').click()


def click_next_page():
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
        By.XPATH, f'//*[@id="toplistWrapper"]/div[2]/div/a[10]')))
    driver.find_element(
        By.XPATH, f'//*[@id="toplistWrapper"]/div[2]/div/a[10]').click()
    for i in range(1, cycle):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, f'//*[@id="toplistWrapper"]/div[2]/div/a[11]')))
        driver.find_element(
            By.XPATH, f'//*[@id="toplistWrapper"]/div[2]/div/a[11]').click()


while True:
    change_permission_setting()

    btn_open_list = driver.find_element(
        By.XPATH, '//*[@id="toplistSpanBlind"]')
    btn_open_list.click()
    time.sleep(3)

    if 1 <= page_num <= 9 and cycle == 0:  # 1~9
        try:
            find_page_btn()
            page_num += 1
            perform_cnt += 1
            time.sleep(3)
        except Exception as e:
            print('에러 메세지: ', e)
            break
    elif page_num == 10 and cycle == 0:  # 10
        try:
            find_page_btn()
            time.sleep(3)
            page_num = 2
            cycle += 1
        except Exception as e:
            print('에러 메세지: ', e)
            break
    elif cycle > 0 and 2 <= page_num <= 10:  # 11 ~ (2~10)
        try:
            click_next_page()
            find_page_btn()
            page_num += 1
            time.sleep(3)
        except Exception as e:
            print('에러 메세지: ', e)
            break
    elif page_num == 11 and cycle > 0: # 다음 페이지 버튼 (10번 제외)
        try:
            click_next_page()
            find_page_btn()
            time.sleep(3)
            page_num = 2
            cycle += 1
        except Exception as e:
            print('에러 메세지: ', e)
            break