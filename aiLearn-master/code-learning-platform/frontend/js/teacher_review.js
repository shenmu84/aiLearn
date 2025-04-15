// 文件名：teacher_review.js

async function fetchSubmissions() {
  const res = await fetch('/api/teacher/submissions');
  const data = await res.json();

  const container = document.getElementById('submissions');
  if (data.error) {
    container.innerText = data.error;
    return;
  }

  data.forEach(sub => {
    const div = document.createElement('div');
    div.innerHTML = `
      <p><strong>学生:</strong> ${sub.student}</p>
      <p><strong>作业内容:</strong> <pre>${sub.solution}</pre></p>
      <label>评分: <input type="number" id="score-${sub.assignment_id}" min="0" max="100" style="width: 80px;"></label>
      <label>反馈: <input type="text" id="feedback-${sub.assignment_id}"></label>
      <button onclick="submitFeedback(${sub.assignment_id}, '${sub.student}')">提交评分</button>
      <hr>
    `;
    container.appendChild(div);
  });
}

async function submitFeedback(assignmentId, student) {
  const score = document.getElementById(`score-${assignmentId}`).value;
  const feedback = document.getElementById(`feedback-${assignmentId}`).value;

  const res = await fetch('/api/teacher/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ assignment_id: assignmentId, student, feedback, score })
  });

  const result = await res.json();
  alert(result.message || result.error);
}

fetchSubmissions();
