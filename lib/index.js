const socket = io();

socket.emit('getSeats');

socket.on('seatsUpdated', (seatLayout) => {
  const container = document.getElementById('seat-map');
  container.innerHTML = '';
  container.style.position = 'relative'; // 자유 배치

  seatLayout.forEach(cluster => {
    cluster.seats.forEach(seat => {
      const div = document.createElement('div');
      div.classList.add('seat');
      div.classList.add(seat.occupied ? 'occupied' : 'free');
      div.textContent = seat.id;

      // 좌표 기반 배치
      div.style.position = 'absolute';
      const TiltingX=-50;
      const TiltingY=-350;
      div.style.left = seat.posX+TiltingX + 'px';
      div.style.top = seat.posY+TiltingY + 'px';

      container.appendChild(div);
    });
  });


  // 추천 좌석 표시
  const recommended = recommendSeat(seatLayout);
  if (recommended) {
    const seatDivs = document.querySelectorAll('.seat');
    const target = Array.from(seatDivs).find(div => div.textContent == recommended.id);
    if (target) target.classList.add('recommended');
    document.getElementById('recommendation').textContent = `추천 좌석: ${recommended.id}번`;
  } else {
    document.getElementById('recommendation').textContent = '추천 가능한 좌석이 없습니다.';
  }
});

// 추천 알고리즘: 인접 회피 + 가운데 선호
function recommendSeat(seatLayout) {
  const allSeats = seatLayout.flatMap(c => c.seats);
  const available = allSeats.filter(s => !s.occupied);
  const candidates = available.filter(s => {
    const left = allSeats.find(x => x.id === s.id - 1);
    const right = allSeats.find(x => x.id === s.id + 1);
    return !(left && left.occupied) && !(right && right.occupied);
  });
  const mid = Math.floor(allSeats.length / 2);
  candidates.sort((a, b) => Math.abs(a.id - mid) - Math.abs(b.id - mid));
  return candidates[0] || null;
}
