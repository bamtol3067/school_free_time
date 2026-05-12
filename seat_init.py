import cv2
import sqlite3

# --- DB 초기화 ---
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

# 이미지 불러오기
img = cv2.imread("./img/seat.jpg")

if img is None:
    raise FileNotFoundError("이미지를 불러올 수 없습니다. 경로와 파일명을 확인하세요.")

# 보기 편하게 리사이즈
scale = 800 / img.shape[0]
resized = cv2.resize(img, (int(img.shape[1]*scale), 800))

seat_coords = {}

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        seat_id = len(seat_coords) + 1
        orig_x = int(x / scale)
        orig_y = int(y / scale)
        seat_coords[seat_id] = (orig_x, orig_y, 20, 20)  # 20x20 박스

        # DB에 INSERT OR IGNORE
        cursor.execute("""
        INSERT OR IGNORE INTO seats (id, occupied, posX, posY)
        VALUES (?, ?, ?, ?)
        """, (seat_id, 0, orig_x, orig_y))

        # UPDATE (좌표 갱신)
        cursor.execute("""
        UPDATE seats SET posX=?, posY=? WHERE id=?
        """, (orig_x, orig_y, seat_id))

        conn.commit()

        print(f"좌석 {seat_id} 저장 완료 → ({orig_x}, {orig_y})")

        # 클릭 위치 표시
        cv2.circle(resized, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(resized, str(seat_id), (x+5, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
        cv2.imshow("image", resized)

cv2.imshow("image", resized)
cv2.setMouseCallback("image", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

conn.close()