from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
    driver.get('https://www.eais.go.kr/moct/bci/aaa02/BCIAAA02L01')

    # 로그인 버튼 클릭
    try:
      # 버튼이 로드될 때까지 최대 10초 대기
      login_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"container\"]/div[2]/div/div[2]/button"))
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
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"container\"]/div[2]/div/div/div[1]/div[1]/button"))
      )
      login_submit_button.click()
    except Exception as e:
      print(e)
      pass


def apply_buildingInfo(driver,address):
    print(address)
    wait = WebDriverWait(driver, 10)
    sleep(1)
    driver.get('https://www.eais.go.kr/moct/bci/aaa02/BCIAAA02L01')

    multiselect_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id=\"eleasticSearch\"]/div/div'))  # 실제 CSS 셀렉터로 대체
    )
    multiselect_input.click()


    # 주소 입력 필드가 로드될 때까지 대기
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"eleasticSearch\"]/div/div/div[2]/input"))
    )
    search_input.send_keys(address) 

    sleep(2)

    # 검색 결과 리스트 요소가 로드될 때까지 대기
    results_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "multiselect__content-wrapper"))
  )
    
    select = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id=\"eleasticSearch\"]/div/div/div[3]/ul/li[1]/span')))
    select.click()

    search_btn=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btnSrch')))
    search_btn.click()

    print("검색입력")

    result_field=wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"container\"]/div[2]/div/div[2]/div[1]/div[3]")))


    try:
      print('pass')   

    except Exception as e:
      print("부동산 상세 정보 조회 중 에러 발생:", e)
      return None


if __name__ == "__main__":
    # 크롬 옵션 설정 (옵션은 필요에 따라 추가/삭제 가능)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('detach', True)

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    my_username = "es2006"
    my_password = "wngustkd1!"
    address="지봉로 85-14"

    actions = [{
        "action": login,
        "args": [driver, my_username, my_password]
    },
    {"action":apply_buildingInfo,"args":[driver,address]}]

    for action in actions:
      if isinstance(action, dict):
          result = action["action"](*action["args"])
      else:
          result = action(driver)
      print(result)
