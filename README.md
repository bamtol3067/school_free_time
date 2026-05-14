# school_free_time
2023100973 서승준 - 조장, 개발
2020100346 표훈 - 자료분석, ppt 
2025100      박민우
2025100

# How to run
## 1. 사전 준비

### Node.js 설치
이미 설치되어 있다면 터미널에서 버전 확인:
```
node -v
```

### Python 설치
이미 설치되어 있다면 터미널에서 버전 확인:
```
python --version
```

---

## 2. 코드 다운로드
GitHub에서 프로젝트를 다운로드합니다.

---

## 3. 프로젝트 폴더로 이동
다운로드한 파일 위치는 사람마다 다르므로 먼저 확인 후 이동합니다.
```
cd school_free_time
```
> ⚠️ 세부 파일 안으로 들어가지 말고 `school_free_time` 폴더까지만 이동

---

## 4. 패키지 설치
```
npm install
pip install opencv-python numpy flask flask-cors
```

---

## 5. 서버 실행
```
node app.js
```

---

## 6. 접속
터미널에 아래와 같이 뜨면 성공:
```
서버 실행 중: http://localhost:3000
```
터미널에 표시된 주소(`http://localhost:3000`)로 브라우저에서 접속합니다.

---

## 7. Python 실행 2개 (별도 터미널)
새 터미널 창을 2개 열고 아래 명령어 입력:
```bash
python seat_check.py
```

```bash
python recommend.py
```

---

> 💡 터미널을 끄면 서버도 꺼집니다. 다시 실행하려면 **3 → 5 → 6 → 7 단계**를 반복하세요.
