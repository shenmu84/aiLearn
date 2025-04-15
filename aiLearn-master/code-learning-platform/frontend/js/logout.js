// logout.js - 提供“退出登录”按钮功能

function logout() {
  fetch('/api/logout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(response => response.json())
    .then(data => {
      if (data.message === '已退出登录') {
        localStorage.removeItem('user');
        window.location.href = "login.html";  // 修改为你的登录页面路径
      } else {
        alert("退出失败，请重试");
      }
    }).catch(error => {
      console.error("退出出错：", error);
      alert("退出失败，请检查网络连接");
    });
}

function renderLogoutButton(containerSelector = "body") {
  const container = document.querySelector(containerSelector);
  if (!container) return;

  const div = document.createElement("div");
  div.style.position = "fixed";
  div.style.top = "10px";
  div.style.right = "10px";
  div.style.zIndex = "1000";

  const button = document.createElement("button");
  button.textContent = "🚪 退出登录";
  button.style.padding = "10px 20px";
  button.style.backgroundColor = "red";
  button.style.color = "white";
  button.style.border = "none";
  button.style.cursor = "pointer";
  button.style.fontSize = "16px";
  button.onclick = logout;

  div.appendChild(button);
  container.appendChild(div);
}
