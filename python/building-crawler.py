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

    results = driver.find_elements(By.CSS_SELECTOR, '.result-item')
    for result in results:
      address_text_elements = result.find_elements(By.CSS_SELECTOR, '.address-text .text')
      for address_text_element in address_text_elements:
        if address in address_text_element.text:
          try:
            result.click()
          except:
            break

    next_list = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "next-list"))
    )
    if(next_list):
      next_results = driver.find_elements(By.CSS_SELECTOR, '.next-list_item')
      print('next_results',len(next_results))
      if(len(next_results)==1):
        next_results[0].click()
      else:
        for result in next_results:
          text_element = result.find_element(By.CSS_SELECTOR, '.text')
          if dong in text_element.text:
              result.click()


def get_report_by_type(driver,ho):


  print('여기')




def apply_buildingInfo(driver,dong,ho):
    wait = WebDriverWait(driver, 10)

    if(dong or ho):
      jeonyubu_tab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#__layout > div > div:nth-child(1) > div > div.container > div.pdT-medium.base-side > div.mgT-medium > div.folder-list.js-btnRdo > button.folder-list_btn.color5.js-btn')))
      jeonyubu_tab.click()

      rows = driver.find_elements(By.CSS_SELECTOR, '.js-tblData tbody tr')

      # 각 행을 순회하며 조건에 맞는지 확인
      for row in rows:
          ho_name = row.find_element(By.XPATH, './/td[4]').text
          if ho in ho_name:
              # 체크박스 클릭
              checkbox = row.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
              checkbox.click()
              break



    result_field=wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"container\"]/div[2]/div/div[2]/div[1]/div[3]")))

    if(result_field):
      driver.switch_to.window(driver.window_handles[0])
      rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ag-center-cols-container .ag-row')))
      first_tab_condition_met = False

      if(dong or ho):
        jeonyubu_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.complaintSelTab li.st5')))
        jeonyubu_tab.click()

        driver.execute_script("document.querySelector('.ag-center-cols-viewport').scrollTop = document.querySelector('.ag-center-cols-viewport').scrollHeight")
        
        scroll_to_bottom(driver)
        rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ag-center-cols-container .ag-row')))


        print(len(rows))
        for row in rows:
            try:
                if dong:
                  dong_cell = row.find_element(By.CSS_SELECTOR, '[col-id="dongNm"]')
                  if dong not in dong_cell.text:
                      continue

                ho_cell = row.find_element(By.CSS_SELECTOR, '[col-id="hoNm"]')
                if ho in ho_cell.text:
                    checkbox = row.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
                    if not checkbox.is_selected():
                        checkbox.click()
                    break
            except:
                continue


      add=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btnAddCart')))
      add.click()
      sleep(2)

      get_building=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/div[2]/div/div[2]/div[2]/button')))
      get_building.click()

      sleep(2)

      reportSearchBtn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div/div[5]/button[2]')))
      reportSearchBtn.click()

    try:
      print('pass')   

    except Exception as e:
      print("부동산 상세 정보 조회 중 에러 발생:", e)
      return None



def get_report(driver):
    sleep(5)
    print('발급')
    wait = WebDriverWait(driver, 10)
    try:
        reportBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#container > div.content > div > div.bbsWrap.mt40 > table > tbody > tr:nth-child(1) > td:nth-child(5) > a')))
        reportBtn.click()
    except UnexpectedAlertPresentException:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("Unexpected alert accepted")
        except NoAlertPresentException:
            pass
        # 재시도 로직
        try:
            reportBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#container > div.content > div > div.bbsWrap.mt40 > table > tbody > tr:nth-child(1) > td:nth-child(5) > a')))
            reportBtn.click()
        except TimeoutException:
            print("Failed to click the report button after alert was accepted")
    return "Report generation attempted"


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
    address="서후센타시아"
    dong=""
    ho="411"

    actions = [{
        "action": login,
        "args": [driver, my_username, my_password]
      },
      {"action":search_building,"args":[driver,address,dong]},
      {"action":apply_buildingInfo,"args":[driver,dong,ho]},
      {"action":get_report,"args":[driver]}]

    for action in actions:
      if isinstance(action, dict):
          result = action["action"](*action["args"])
      else:
          result = action(driver)
      print(result)
