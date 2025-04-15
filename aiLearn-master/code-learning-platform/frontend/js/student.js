document.getElementById("content").innerHTML = `
<ul>
  <li><a href="chat.html">AI 问答</a></li>
  <li><a href="student_submit.html">提交作业</a></li>
  <li><a href="student_grades.html">查看成绩</a></li>
</ul>

  <div id="student-section"></div>
`;

function showSubmitAssignment() {
  document.getElementById("student-section").innerHTML = `
    <h3>提交作业</h3>
    <form id="assignmentForm">
      <label>作业编号：</label><input type="number" id="assignmentId" required><br>
      <label>答案：</label><br><textarea id="solution" rows="5" cols="50" required></textarea><br>
      <button type="submit">提交</button>
    </form>
    <div id="submitMessage"></div>
  `;

  document.getElementById("assignmentForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const assignmentId = document.getElementById("assignmentId").value;
    const solution = document.getElementById("solution").value;

    fetch("/api/student/submit_assignment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ assignment_id: assignmentId, solution: solution })
    })
      .then(res => res.json())
      .then(data => {
        document.getElementById("submitMessage").innerText = data.message || data.error;
      });
  });
}

function showGrades() {
  document.getElementById("student-section").innerHTML = `<h3>成绩列表</h3><div id="gradesList">加载中...</div>`;

  fetch("/api/student/grades")
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById("gradesList").innerText = data.error;
        return;
      }

      const list = data.map(item => `
        <div style="margin-bottom: 10px;">
          <strong>作业编号：</strong>${item.assignment_id}<br>
          <strong>答案：</strong>${item.solution}<br>
          <strong>成绩：</strong>${item.grade ?? "未评分"}<br>
          <strong>反馈：</strong>${item.feedback || "暂无反馈"}
        </div>
      `).join("");

      document.getElementById("gradesList").innerHTML = list || "暂无提交记录";
    });
}
