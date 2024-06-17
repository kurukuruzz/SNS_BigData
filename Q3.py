import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# 사용자 입력 받기
keyword = input("크롤링할 이미지의 키워드는 무엇입니까? ")
num_images = int(input("크롤링할 건수는 몇 건입니까? "))

driver = webdriver.Chrome()

try:
    search_url = f"https://pixabay.com/ko/photos/search/{keyword}/"
    driver.get(search_url)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img")))

    images = driver.find_elements(By.CSS_SELECTOR, "img")

    for index, image in enumerate(images[:num_images], start=1):
        try:
            image = driver.find_elements(By.CSS_SELECTOR, "img")[index - 1]
            image_url = image.get_attribute('src')
            if not image_url:
                continue
                
            download_folder = './downloads' # 이미지 경로 설정
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            
            image_filename = os.path.join(download_folder, f"image_{index}.jpg")
            
            # 이미지 다운로드
            response = requests.get(image_url)
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"다운로드 완료: {image_filename}")
        
        except StaleElementReferenceException:
            print(f"발생: 이미지 {index} 처리 중")
            continue
finally:
    driver.quit()
