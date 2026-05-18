# Node.js 20 이상 사용 (sqlite36 패키지 요구사항 충족)
FROM node:20

# Python 설치 + 가상환경 준비
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

WORKDIR /app

# Node 패키지 설치
COPY package*.json ./
RUN npm install

# 전체 코드 복사
COPY . .

# Python 가상환경 생성 후 패키지 설치
RUN python3 -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install opencv-python numpy flask flask-cors

EXPOSE 3000

# Node 서버와 Python 스크립트 실행 시 가상환경 Python 사용
CMD ["sh", "-c", "node app.js & /app/venv/bin/python seat_check.py & /app/venv/bin/python recommend.py && tail -f /dev/null"]
