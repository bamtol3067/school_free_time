import cv2
import numpy as np
import sqlite3
import os
import time

# --- DB 연결 ---
conn = sqlite3.connect("seats.sqlite")
cursor = conn.cursor()

# 테이블 생성 (없으면 생성)
cursor.execute("""
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY,
    occupied INTEGER,
    posX INTEGER,
    posY INTEGER
)
""")
conn.commit()
conn.close()

# 이미지 불러오기
while True:
    if os.path.exists("./img/seat.jpg"):
        print("seat처리시작")
        conn = sqlite3.connect("seats.sqlite")
        cursor = conn.cursor()
        img = cv2.imread("./img/seat.jpg")
        if img is None:
            print("무언가 잘못되었습니다.")
            conn.close()
            os.remove("./img/seat.jpg")
            continue
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        gray_lower = np.array([0, 0, 50])
        gray_upper = np.array([180, 50, 200])

        cursor.execute("SELECT id, posX, posY FROM seats LIMIT 188")
        rows = cursor.fetchall()

        for seat_id, x, y in rows:
            w, h = 20, 20  # 박스 크기 (수정 가능)
            roi = hsv[y:y+h, x:x+w]
            mean_color = cv2.mean(roi)[:3]

            # 상태 판별
            if (gray_lower <= mean_color).all() and (mean_color <= gray_upper).all():
                occupied = 1
            else:
                occupied = 0  # unknown

            # DB 갱신
            cursor.execute("""
            UPDATE seats SET occupied=? WHERE id=?
            """, (occupied, seat_id))

            print(f"좌석 {seat_id}: 상태={occupied}, 좌표=({x},{y})")

        conn.commit()
        conn.close()
        os.remove("./img/seat.jpg")
        print("seat처리완료")
    time.sleep(1)
