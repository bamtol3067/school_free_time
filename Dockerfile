FROM node:18

# Python 설치
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

# Node 패키지 설치
COPY package*.json ./
RUN npm install

# 전체 코드 복사
COPY . .

# 필요한 Python 패키지 직접 설치
RUN pip3 install opencv-python numpy flask flask-cors

EXPOSE 3000

CMD ["sh", "-c", "node app.js & python3 seat_check.py & python3 recommend.py && tail -f /dev/null"]
