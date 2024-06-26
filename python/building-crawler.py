from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException,TimeoutException
from time import sleep
import pyautogui
import asyncio


def login(driver, username, password):
    """
    Logs into a website using selenium.
    
    Parameters:
        driver (webdriver): The selenium webdriver object.
        url (str): The URL of the login page.
        username (str): The username to login with.
        password (str): The password to login with.
    """
    wait = WebDriverWait(driver, 10)

    # Open the login page
    driver.get('https://m.eais.go.kr/mbi/mbi/aza01/MBIAZA01F02?returnUrl=%2Fmbi%2FMBIADB01P01')

    # 로그인 버튼 클릭
    try:
      # 버튼이 로드될 때까지 최대 10초 대기
      login_button = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div/div/div[3]/button[1]'))
      )
      login_button.click()

    except Exception as e:
      pass
    
    # 아이디와 비밀번호 입력 후 로그인
    try:
      print('로그인 시도')
      # 아이디 입력
      id_field = wait.until(
        EC.presence_of_element_located((By.ID, "membId"))
      )
      id_field.send_keys(username)

      # 비밀번호 입력
      password_field = wait.until(
        EC.presence_of_element_located((By.ID, "pwd"))
      )
      password_field.send_keys(password)

      # 로그인 버튼 클릭
      login_submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div/div[1]/div/button'))
      )
      login_submit_button.click()
    except Exception as e:
      print(e)
      pass


def search_building(driver,address,dong):
    print(address)
    wait = WebDriverWait(driver, 10)
    sleep(1)

    check_building = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#__layout > div > div > div.container > div.box-list2.pdT-medium.base-side > button:nth-child(1)')))
    check_building.click()

    # 주소 입력 필드가 로드될 때까지 대기
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#__layout > div > div:nth-child(1) > div > div.container > div > div.search1 > div > div > input'))
    )
    search_input.send_keys(address) 
    search_input.send_keys(Keys.ENTER)

    sleep(1)

    results = driver.find_elements(By.CLASS_NAME, 'result-item')
    print('result',len(results))
    for result in results:
      address_text_elements = result.find_elements(By.XPATH, './/span[@class="text"]')
      print('address_text_elements',address_text_elements)
      for address_text_element in address_text_elements:
        print(address_text_element.text)
        if address in address_text_element.text:
          try:
            result.click()
            done=True
            sleep(1)
            break
          except:
            break
        else:
          continue
      if(done):
        break


    next_results = driver.find_elements(By.CLASS_NAME, 'next-list_item')

    if(len(next_results)==1):
      next_results[0].click()
      print('여기는 갔어..?')
      return

    for result in next_results:
      text_element = result.find_element(By.CSS_SELECTOR, '.text')
      print('text',text_element.text)
      if(len(text_element.text)<1):
        return
      if dong in text_element.text:
        result.click()
        return


def select_report_type(driver,ho,report_type):
  print('왜 안와')
  sleep(1)
  wait=WebDriverWait(driver,10)
  folder_btns = driver.find_elements(By.CLASS_NAME,'folder-list_btn')
  error=[]

  for folder_btn in folder_btns:
    text_element = folder_btn.find_element(By.CLASS_NAME,'text')
    len = folder_btn.find_element(By.TAG_NAME,'em')
  
  for type in report_type:
    for folder_btn in folder_btns:
      text_element = folder_btn.find_element(By.CLASS_NAME,'text')
      len = folder_btn.find_element(By.TAG_NAME,'em')
      if(int(len.text)==0):
        error.append('type은 가져올수 없는 건물입니다')
        print(f'{type}은 가져올수 없는 건물입니다')
        continue

      if(type !='전유부' and type in text_element.text):
        folder_btn.click()
        id = check_data(type)
        check = wait.until(EC.presence_of_element_located((By.ID,id)))
        check.click()
      elif(type in text_element.text):
        folder_btn.click()
        sleep(2)

        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div[1]/div[4]/div')))
        table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div[1]/div[4]/div/table')))
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        for row in rows:
          ho_name = row.find_elements(By.TAG_NAME, 'td')[3].text
          if ho in ho_name:
            # 체크박스 클릭
            print(ho, '/',ho_name)
            checkbox_table = row.find_elements(By.TAG_NAME, 'td')[0]
            checkbox=checkbox_table.find_element(By.TAG_NAME,'input')
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            sleep(1)  # 스크롤이 완료될 시간을 줌
            driver.execute_script("arguments[0].click();", checkbox)
            break


def check_data(type):
  if('총괄' in type):
    return 'filterRecap_0'
  
  if('일반' in type):
    return 'filterGnrl_0'
    
  if('다가구' in type):
    return 'filterGnrl_0'
    
  if('표제부' in type):
    return 'filterTitle_0'
    


def apply_report(driver):
  wait = WebDriverWait(driver, 10)
  apply_btn=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#__layout > div > div:nth-child(1) > div > div.bottom-fixbar > div > button')))
  apply_btn.click()
  
  sleep(1)

  next_btn=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#__layout > div > div:nth-child(1) > div > div.bottom-layer-popup.type2.js-btmLayer.active > div.popup > div > button')))
  next_btn.click()


  table=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#__layout > div > div:nth-child(1) > div > div > div.pdT-medium.base-side > div.tbl-scroll.js-tblScroll.mgT-medium > div > table > tbody')))
  rows = table.find_elements(By.TAG_NAME,'tr')

  sleep(1)
  show_btn=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#__layout > div > div:nth-child(1) > div > div > div.pdT-medium.base-side > button')))
  show_btn.click()

  return len(rows)



def view_report(driver,report_type):
  wait=WebDriverWait(driver,10)
  sleep(2)
  try:
    table = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div[1]/div/table/tbody')))
    table_rows = table.find_elements(By.TAG_NAME,'tr')
  except:
    table = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/div[2]/div[1]/div[2]/table/tbody')))
    table_rows = table.find_elements(By.TAG_NAME,'tr')


  for (i,type) in enumerate(report_type):

    view_button = table_rows[i].find_element(By.TAG_NAME,'button')
    view_button.click()
    
    print(i,type)
    # tab 전환
    sleep(2)  # 탭이 열릴 시간을 줌

    for _ in range(5):  # 최대 5개의 랜덤 탭이 열릴 수 있음
      if len(driver.window_handles) > 1:
          driver.switch_to.window(driver.window_handles[-1])
          sleep(3)
          save_pdf(driver)  # PDF 저장 함수 호출 desired_filename.pdf
          driver.close()

    driver.switch_to.window(driver.window_handles[0])
    close_extra_tabs(driver) 

def save_pdf(driver):
  try:
    
    # PDF 저장을 위한 단축키 사용
    # pyautogui.hotkey('command', 'p')  # Cmd
    #  + P를 눌러 인쇄 팝업을 엶     
    pyautogui.keyDown('command')
    pyautogui.press('p')
    pyautogui.keyUp('command')
    sleep(1)  # 인쇄 대화상자가 열릴 시간을 기다림
    pyautogui.press('tab', presses=4, interval=0.5)         
    pyautogui.press('down', presses=2, interval=0.5)  # PDF로 저장 옵션 선택
    sleep(1)  # 저장 대화상자가 열릴 시간을 기다림
    pyautogui.press('enter',presses=2,interval=0.5)
    sleep(2)  # 파일이 저장될 시간을 기다림


    pyautogui.press('tab', presses=5, interval=0.5)

    pyautogui.press('enter',presses=2)
    sleep(2)  # 파일이 저장될 시간을 기다림

    print('완료')
  except Exception as e:
      print(f"An error occurred while saving the PDF: {e}")


def close_extra_tabs(driver):
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])

def handle_alerts(driver):
    while True:
        try:
            alert = Alert(driver)
            alert.accept()
            print("Alert accepted")
        except NoAlertPresentException:
            # 경고 창이 없으면 아무것도 하지 않음
            pass
        sleep(1)  # 1초마다 경고 창 감지

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.querySelector('.ag-center-cols-viewport').scrollHeight")
    while True:
        driver.execute_script("document.querySelector('.ag-center-cols-viewport').scrollTop = document.querySelector('.ag-center-cols-viewport').scrollHeight")
        sleep(2)  # 스크롤 후 페이지가 로드될 시간을 주기 위해 잠시 대기
        new_height = driver.execute_script("return document.querySelector('.ag-center-cols-viewport').scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


if __name__ == "__main__":
    # 크롬 옵션 설정 (옵션은 필요에 따라 추가/삭제 가능)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('detach', True)

    
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # alert = Alert(driver)
    # alert.accept()

    my_username = "es2006"
    my_password = "wngustkd1!"
    address="지봉로 107"
    dong=""
    ho=""
    report_type=['일반']

    actions = [{
        "action": login,
        "args": [driver, my_username, my_password]
      },
      {"action":search_building,"args":[driver,address,dong]},
      {"action":select_report_type,"args":[driver,ho,report_type]},
      {"action":apply_report,"args":[driver]},
      {"action":view_report,"args":[driver,report_type]}
    ]
      #     {"action":apply_buildingInfo,"args":[driver,dong,ho]},
      # {"action":get_report,"args":[driver]}

    report_cnt = 0

    for action in actions:
      if isinstance(action, dict):          
        if action["action"] == apply_report:
          report_cnt = action["action"](driver)
          print(report_cnt)
        else:
          result = action["action"](*action["args"])


      else:
          result = action(driver)
      print(result)
