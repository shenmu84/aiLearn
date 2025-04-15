const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const loadingIndicator = document.getElementById('loading-indicator');

function appendMessage(text, isUser = true) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message', isUser ? 'user' : 'bot');
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.onclick = async () => {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, true);
  userInput.value = "";
  userInput.disabled = true;
  sendBtn.disabled = true;
  loadingIndicator.classList.remove("hidden");

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    appendMessage(data.response, false);
  } catch (error) {
    appendMessage("发生错误，请稍后再试", false);
  } finally {
    loadingIndicator.classList.add("hidden");
    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.focus();
  }
};

// 回车发送
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendBtn.click();
  }
});
