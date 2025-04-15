// navigation.js - 提供“返回主页”功能

function goHome() {
  const user = JSON.parse(localStorage.getItem('user'));
  if (!user || !user.role) {
    window.location.href = "login.html";
    return;
  }

  switch (user.role) {
    case "student":
      window.location.href = "student-dashboard.html";
      break;
    case "teacher":
      window.location.href = "teacher-dashboard.html";
      break;
    case "admin":
      window.location.href = "admin-dashboard.html";
      break;
    default:
      window.location.href = "login.html";
  }
}

function renderGoHomeButton(containerSelector = "body") {
  const container = document.querySelector(containerSelector);
  if (!container) return;

  const div = document.createElement("div");
  div.style.padding = "1rem";

  const button = document.createElement("button");
  button.textContent = "🏠 返回主页";
  button.classList.add("common-button");  // 添加通用按钮类
  button.onclick = goHome;

  div.appendChild(button);

  // 将“返回主页”按钮添加到“退出登录”按钮之后
  const logoutButton = document.getElementById('logout-button');
  if (logoutButton) {
    logoutButton.appendChild(div); // 将返回按钮添加到退出按钮的后面
  } else {
    container.appendChild(div); // 如果没有找到退出按钮，则放在容器末尾
  }
}

