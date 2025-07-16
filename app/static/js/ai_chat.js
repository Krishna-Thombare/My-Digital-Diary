function toggleChat() {
  const chatBox = document.getElementById("ai-chat-box");
  chatBox.classList.toggle("open");
}

function sendMessage() {
  const input = document.getElementById("ai-chat-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";

  // Show typing/loading animation
  appendMessage("assistant", "Typing...", true);

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: message })
  })
  .then(res => res.json())
  .then(data => {
    // Remove "Typing..." placeholder
    removeTypingPlaceholder();
    if (data.response) {
      appendMessage("assistant", data.response);
    } else {
      appendMessage("assistant", "⚠️ Error: " + (data.error || "Something went wrong"));
    }
  })
  .catch(err => {
    removeTypingPlaceholder();
    appendMessage("assistant", "⚠️ Error: " + err.message);
  });
}

function appendMessage(role, text, isTyping = false) {
  const container = document.getElementById("ai-chat-messages");
  const msgDiv = document.createElement("div");
  msgDiv.className = role;
  msgDiv.innerHTML = marked.parse(text); // Markdown to HTML

  if (isTyping) msgDiv.classList.add("typing-placeholder");
  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function removeTypingPlaceholder() {
  const placeholders = document.querySelectorAll(".typing-placeholder");
  placeholders.forEach(p => p.remove());
}
