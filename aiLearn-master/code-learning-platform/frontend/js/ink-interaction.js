// 登录界面交互
document.querySelectorAll('.ink-input').forEach(input => {
  input.addEventListener('focus', function() {
    this.parentNode.querySelector('.ink-bar').style.transform = 'scaleX(1)';
  });

  input.addEventListener('blur', function() {
    if(!this.value) {
      this.parentNode.querySelector('.ink-bar').style.transform = 'scaleX(0)';
    }
  });
});

// 注册界面密码强度
document.getElementById('password').addEventListener('input', function(e) {
  const strength = Math.min(4, Math.floor(e.target.value.length / 3));
  document.querySelector('.ink-meter').style.width = strength * 25 + '%';
});

// 404倒计时
let incenseTimer = 15;
const timerInterval = setInterval(() => {
  if(incenseTimer <= 0) {
    clearInterval(timerInterval);
    window.location.href = '/';
    return;
  }
  document.querySelector('.ash-progress').style.height =
    (100 - (incenseTimer/15)*100) + '%';
  incenseTimer--;
}, 1000);
