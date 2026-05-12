import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. 브라우저 설정
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def main():
    try:
        url = "https://sugang.syu.kr/basket"
        driver.get(url)
        
        all_data = []
        
        print("\n" + "="*60)
        print("1. 브라우저에서 로그인 후 장바구니 페이지로 이동하세요.")
        print("2. 매 페이지마다 [Enter]를 누르면 해당 페이지의 데이터를 수집합니다.")
        print("3. 모든 페이지(1~29) 수집이 끝나면 'exit'를 입력하세요.")
        print("="*60)

        page_count = 1
        while True:
            user_input = input(f"\n[{page_count}페이지] 수집하려면 Enter, 종료하려면 'exit' 입력: ")
            if user_input.lower() == 'exit':
                break

            # 현재 페이지의 행(row)들 찾기 (보통 테이블의 tr 또는 특정 클래스)
            # 수강신청 사이트 구조상 데이터가 들어있는 각 줄을 찾습니다.
            rows = driver.find_elements(By.CSS_SELECTOR, "tr") # 혹은 목록의 단위 클래스명

            page_items_count = 0
            for row in rows:
                try:
                    # 1. 학수번호 (col-courseNo > span)
                    course_no_els = row.find_elements(By.CSS_SELECTOR, ".col-courseNo span")
                    if not course_no_els: continue # 해당 클래스가 없는 행은 건너뜀
                    
                    course_no = course_no_els[0].text.strip()

                    # 2. 인원 정보 (col-count)
                    # span 내부 텍스트와 외부 텍스트 분리 로직
                    count_el = row.find_element(By.CLASS_NAME, "col-count")
                    
                    # span 안의 텍스트 (예: 현재인원)
                    span_el = count_el.find_element(By.TAG_NAME, "span")
                    span_text = span_el.text.strip()
                    
                    # span 밖의 텍스트 (예: / 전체정원)
                    # 전체 텍스트에서 span 텍스트를 제거하여 밖의 텍스트만 추출
                    full_text = count_el.text.strip()
                    outer_text = full_text.replace(span_text, "").strip()

                    all_data.append({
                        "페이지": page_count,
                        "학수번호": course_no,
                        "인원_내부(span)": span_text,
                        "인원_외부(텍스트)": outer_text
                    })
                    page_items_count += 1

                except Exception:
                    continue
            
            print(f">> {page_count}페이지에서 {page_items_count}개 수집 완료.")
            page_count += 1

        # 3. CSV 저장
        if all_data:
            df = pd.DataFrame(all_data)
            file_name = "syu_basket_result.csv"
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
            print("\n" + "="*60)
            print(f"최종 저장 완료: {file_name}")
            print(f"총 수집 데이터: {len(df)}건")
            print("="*60)
        else:
            print("\n수집된 데이터가 없습니다.")

    except Exception as e:
        print(f"\n오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()