import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. 브라우저 옵션 설정 (차단 방지 및 수동 조작용)
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def main():
    try:
        # 타겟 URL 접속
        url = "https://lecture.syu.kr/timetable"
        driver.get(url)
        
        print("\n" + "="*50)
        print("1. 브라우저 창에서 학과 선택 및 스크롤을 끝까지 수행하세요.")
        print("2. 데이터 로딩이 모두 완료되었다면 이 창(터미널)에서 Enter를 누르세요.")
        print("="*50)
        
        # 사용자 대기
        input(">> 모든 준비가 끝났다면 [Enter]를 입력하세요...")

        print("\n데이터 수집을 시작합니다...")
        
        # 2. 요소 추출
        # 질문하신 구조: .course-items > .course-item
        items = driver.find_elements(By.CLASS_NAME, "course-item")
        
        extracted_data = []
        seen_nums = set()  # 중복 방지용 셋

        for item in items:
            try:
                # first-line 안의 course-name
                name_els = item.find_elements(By.CSS_SELECTOR, ".first-line .course-name")
                # second-line 안의 course-num, course-time
                num_els = item.find_elements(By.CSS_SELECTOR, ".second-line .course-num")
                time_els = item.find_elements(By.CSS_SELECTOR, ".second-line .course-time")

                # 데이터가 존재할 경우에만 텍스트 추출
                name = name_els[0].text.strip() if name_els else "N/A"
                num = num_els[0].text.strip().replace("강좌번호:", "").strip() if num_els else "N/A"
                ctime = time_els[0].text.strip() if time_els else "N/A"

                # 중복되지 않은 강좌번호만 리스트에 추가
                if num != "N/A" and num not in seen_nums:
                    extracted_data.append({
                        "강의명": name,
                        "강좌번호": num,
                        "시간": ctime
                    })
                    seen_nums.add(num)
                    
            except Exception as e:
                print(f"항목 추출 중 오류 발생: {e}")
                continue

        # 3. CSV 저장
        if extracted_data:
            df = pd.DataFrame(extracted_data)
            file_name = "syu_timetable_result.csv"
            
            # utf-8-sig: 엑셀에서 한글 깨짐 방지
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
            
            print("\n" + "="*50)
            print(f"저장 완료: {file_name}")
            print(f"총 수집된 강의 수: {len(df)}개")
            print("="*50)
        else:
            print("\n추출된 데이터가 없습니다. 페이지 구조를 다시 확인해주세요.")

    except Exception as e:
        print(f"\n프로그램 실행 중 오류: {e}")
        
    finally:
        print("\n브라우저를 종료합니다.")
        driver.quit()

if __name__ == "__main__":
    main()