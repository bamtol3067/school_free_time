import os

def replace_slash_with_comma(file_path):
    # 1. 파일 내용 읽기
    try:
        # 엑셀에서 저장한 파일일 경우 'utf-8-sig'가 안전합니다.
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()

        # 2. '/'를 ','로 교체
        new_content = content.replace('/', ',')

        # 3. 변경된 내용을 동일한 파일(또는 새 파일)에 저장
        # 원본 보호를 위해 이름 끝에 _fixed를 붙입니다.
        new_file_path = file_path.replace('.csv', '_fixed.csv').replace('.txt', '_fixed.txt')
        
        with open(new_file_path, 'w', encoding='utf-8-sig') as file:
            file.write(new_content)

        print(f"변환 완료! 파일이 생성되었습니다: {new_file_path}")
        
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 변환하려는 파일명을 여기에 적어주세요.
replace_slash_with_comma("syu_basket_result.csv")