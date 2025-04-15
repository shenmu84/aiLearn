// 文件名：student_grades.js

window.onload = async () => {
  const res = await fetch("/api/student/grades");
  const grades = await res.json();

  const tbody = document.getElementById("grades-table");
  tbody.innerHTML = "";

  if (grades.length === 0) {
    tbody.innerHTML = "<tr><td colspan='4'>暂无成绩</td></tr>";
    return;
  }

  grades.forEach(g => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${g.assignment_id}</td>
      <td><pre>${g.solution}</pre></td>
      <td>${g.feedback || '暂无反馈'}</td>
      <td>${g.grade || '未评分'}</td>
    `;
    tbody.appendChild(tr);
  });
};
