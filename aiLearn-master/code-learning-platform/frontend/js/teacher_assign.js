// 📄 文件名：js/teacher_assign.js

document.getElementById('assign-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  const student = document.getElementById('student').value;
  const course = document.getElementById('course').value;

  const res = await fetch('/api/teacher/assignments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student, course, content })
  });

  const result = await res.json();
  document.getElementById('result').innerText = result.message || result.error;
});
