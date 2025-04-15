document.getElementById("assignment-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const assignment_id = document.getElementById("assignment_id").value;
  const solution = document.getElementById("solution").value;

  const res = await fetch("/api/student/submit_assignment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ assignment_id, solution })
  });

  const data = await res.json();
  document.getElementById("result").innerText = data.message || data.error;
});
