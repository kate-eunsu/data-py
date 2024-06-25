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
    # Open the login page
    driver.get('https://www.landvisor.net/intro.asp')

    # 로그인 버튼 클릭
    try:
      # 버튼이 로드될 때까지 최대 10초 대기
      login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btnLoginPop"))
      )
      login_button.click()
    except Exception as e:
      pass
    
    # 아이디와 비밀번호 입력 후 로그인
    try:
      print('로그인 시도')
      # 아이디 입력
      email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginId"))
      )
      email_field.send_keys(username)

      # 비밀번호 입력
      password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginPw"))
      )
      password_field.send_keys(password)

      # 로그인 버튼 클릭
      login_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btnLogin"))
      )
      login_submit_button.click()
    except Exception as e:
      pass

def get_point(driver):
    """
    Gets the user's points.
    
    Parameters:
        driver (webdriver): The selenium webdriver object.
    
    Returns:
        str: The amount of points the user has.
    """
    sleep(1)
    driver.get('https://www.landvisor.net/mypage/dashboard.asp')
    try:
        # 포인트 값을 포함하는 요소가 로드될 때까지 대기
        points_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cUserPointTxt"))
        )
        
        # 포인트 값을 추출
        points = points_element.text
        
        # 포인트 값을 리턴
        return f"Points: {points}"
    
    except Exception as e:
        print("포인트 값 추출 중 에러 발생:", e)
        return None
    
def get_land_list(driver):
    """
    Gets the list of lands.
    
    Parameters:
        driver (webdriver): The selenium webdriver object.
    
    Returns:
        list: The list of lands.
    """
    sleep(1)
    driver.get('https://www.landvisor.net/mypage/search.asp')
    try:
        # 부동산 목록을 포함하는 요소가 로드될 때까지 대기
        land_list_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        
        # 테이블의 모든 행을 찾음
        rows = land_list_table.find_elements(By.TAG_NAME, "tr")
        
        land_list = []
        for row in rows[1:]:  # 첫 번째 행은 헤더이므로 제외
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 0:
                land_info = {
                    "구분": cells[0].text,
                    "소재지": cells[1].text,
                    "추정시세": cells[2].text,
                    "검색일자": cells[3].text,
                    "재검색": cells[4].text,
                }
                land_list.append(land_info)
        
        return land_list
    
    except Exception as e:
        print("부동산 목록 추출 중 에러 발생:", e)
        return None

def get_land_detail(driver, address):
    """
    Gets the details of a specific land by searching for its address.
    
    Parameters:
        driver (webdriver): The selenium webdriver object.
        address (str): The address of the land to search for.
    
    Returns:
        dict: The details of the land.
    """
    sleep(1)
    driver.get('https://www.landvisor.net/mypage/dashboard.asp')
    try:
        # 주소 입력 필드가 로드될 때까지 대기
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "topSchInput"))
        )
        
        # 주소 입력
        search_input.send_keys(address)
        sleep(1)  # 검색 결과가 표시될 시간을 대기
        
        # 검색 결과 리스트 요소가 로드될 때까지 대기
        results_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "topSchList"))
        )
        
        # 검색 결과 리스트 내의 모든 항목을 찾음
        results_items = results_list.find_elements(By.TAG_NAME, "li")
        
        if len(results_items) == 1:
            # 검색 결과가 하나인 경우 해당 항목 클릭
            results_items[0].click()
        elif len(results_items) > 1:
            # 검색 결과가 여러 개인 경우 오류 발생
            return "Error: Multiple addresses found, please provide a more specific address."
        else:
            return "Error: No addresses found."
        
        #  특정 요소의 텍스트가 변경될 때까지 대기
        WebDriverWait(driver, 60).until(
         EC.visibility_of_element_located((By.ID, 'landy1'))
        )

        # 상세 정보 페이지 로드 대기
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "mapTopDiv"))
        )

        # 세부 정보 파싱
        details = {}

        # 추정시세
        try:
            est_price = driver.find_element(By.ID, "calPriceSum").text
            details['추정시세'] = est_price
        except:
            details['추정시세'] = None
        
        # 부동산 설명
        try:
            description = driver.find_element(By.ID, "landy1").text
            details['부동산 설명'] = description
        except:
            details['부동산 설명'] = None
        
        # 가격 범위 정보
        try:
            ranges = []
            range_elements = driver.find_elements(By.CSS_SELECTOR, ".boxInner.lineG dl")
            for elem in range_elements:
                range_info = {
                    "지역": elem.find_element(By.TAG_NAME, "dt").text,
                    "가격 범위": elem.find_element(By.CLASS_NAME, "fr").text
                }
                ranges.append(range_info)
            details['가격 범위'] = ranges
        except:
            details['가격 범위'] = None
        
        # 거래량 정보
        try:
            volumes = []
            volume_elements = driver.find_elements(By.CSS_SELECTOR, ".boxInner.lineG dl")
            for elem in volume_elements:
                volume_info = {
                    "연도": elem.find_element(By.TAG_NAME, "dt").text,
                    "건수": elem.find_element(By.CLASS_NAME, "fr").text
                }
                volumes.append(volume_info)
            details['거래량'] = volumes
        except:
            details['거래량'] = None
        
        # 가격 변동 정보
        try:
            price_changes = []
            price_change_elements = driver.find_elements(By.CSS_SELECTOR, ".boxInner.lineG dl")
            for elem in price_change_elements:
                price_change_info = {
                    "지역": elem.find_element(By.TAG_NAME, "dt").text,
                    "변동률": elem.find_element(By.CLASS_NAME, "fr").text
                }
                price_changes.append(price_change_info)
            details['가격 변동'] = price_changes
        except:
            details['가격 변동'] = None

        return details
    
    except Exception as e:
        print("부동산 상세 정보 조회 중 에러 발생:", e)
        return None


# Example usage:
if __name__ == "__main__":
    # 크롬 옵션 설정 (옵션은 필요에 따라 추가/삭제 가능)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('detach', True)

    # 크롬 드라이버 설정 및 브라우저 실행
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Replace these values with your login details and element ids
    my_username = ""
    my_password = ""

    # # case1 - 사용자 포인트 조회
    # actions = [{
    #    "action": login,
    #     "args": [driver, my_username, my_password]
    # }, {
    #     "action": get_point,
    #     "args": [driver]
    # }]

    # # case2 - 사용자 부동산 조회 목록
    # actions = [{
    #     "action": login,
    #     "args": [driver, my_username, my_password]
    # }, {
    #     "action": get_land_list,
    #     "args": [driver]
    # }]

    search_address = "서울특별시 종로구 숭인동 72-81"

    # # case3 - 신규 부동산 조회
    actions = [
        {
            "action": login,
            "args": [driver, my_username, my_password]
        },
        {
            "action": get_land_detail,
            "args": [driver, search_address]
        }
    ]

    for action in actions:
        if isinstance(action, dict):
            result = action["action"](*action["args"])
        else:
            result = action(driver)
        print(result)


    # Add any further actions or close the driver
    # driver.quit()