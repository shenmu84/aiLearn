// 可选：可在此添加闪烁文字效果、跳点等动画增强
const loadingText = document.getElementById("loading-indicator");

let dots = 0;
let loadingInterval = setInterval(() => {
  if (!loadingText) return;
  dots = (dots + 1) % 4;
  loadingText.textContent = 'AI 正在思考' + '.'.repeat(dots);
}, 500);
