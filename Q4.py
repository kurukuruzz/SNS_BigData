from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os
import time

def download_pdf(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
        
keyword = input("크롤링할 키워드는 무엇입니까?: ")
num = int(input("크롤링 할 건수는 몇건입니까?: "))
f_dir = input("파일이 저장될 경로만 쓰세요: ")

os.makedirs(f_dir, exist_ok=True)

driver = webdriver.Chrome()

try:
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(keyword + " filetype:pdf")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    count = 0
    while count < num:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.endswith('.pdf'):
                print(href)
                pdf_url = href
                try:
                    file_name = os.path.join(f_dir, f"{count+1}.pdf")
                    download_pdf(pdf_url, file_name)
                    print(f"{count+1}번째 PDF 파일 다운로드 완료")
                    count += 1
                    if count >= num:
                        break
                except Exception as e:
                    print(f"PDF 파일 다운로드 실패: {str(e)}")
                    continue

        if count >= num:
            break

        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"다음 페이지로 이동 실패: {str(e)}")
            break

finally:
    # 브라우저 종료
    driver.quit()

print("PDF 파일 다운로드 완료")