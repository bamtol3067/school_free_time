// ── 페이지 이동 ───────────────────────────────────────
document.getElementById('chat-card').addEventListener('click', () => {
  window.location.href = "/chat/index.html";
});
document.getElementById('liberary-card').addEventListener('click', () => {
  window.location.href = "/liberary/index.html";
});
document.getElementById('profile').addEventListener('click', (e) => {
  e.preventDefault();
  window.location.href = "/login/index.html";
});

// ── 혼잡도 데이터 (추후 API 연동 가능) ────────────────
const congestionData = {
  cafeteria: { label: "여유 있음", level: "low",   pct: 35 },
  library:   { label: "보통",     level: "medium", pct: 60 },
  cafe:      { label: "혼잡",     level: "high",   pct: 88 },
};
const predictedCount = 123;

function updateCongestion() {
  const cards = document.querySelectorAll('.cong-card');
  const keys = ['cafeteria', 'library', 'cafe'];

  keys.forEach((key, i) => {
    const data = congestionData[key];
    const card = cards[i];
    if (!card) return;

    const bar   = card.querySelector('.cong-bar');
    const badge = card.querySelector('.level');
    const pct   = card.querySelector('.cong-pct');

    if (bar)   { bar.style.width = data.pct + '%'; bar.className = `cong-bar ${data.level}`; }
    if (badge) { badge.textContent = data.label; badge.className = `level ${data.level}`; }
    if (pct)   { pct.textContent = data.pct + '%'; }
  });

  const numEl = document.getElementById('predictedCount');
  if (numEl) {
    // 숫자 카운트 업 애니메이션
    let count = 0;
    const target = predictedCount;
    const step = Math.ceil(target / 40);
    const timer = setInterval(() => {
      count = Math.min(count + step, target);
      numEl.textContent = count + '명';
      if (count >= target) clearInterval(timer);
    }, 30);
  }
}

// 페이지 로드 후 실행
window.addEventListener('DOMContentLoaded', updateCongestion);
