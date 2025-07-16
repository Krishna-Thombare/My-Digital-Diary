function toggleChat() {
  const chatBox = document.getElementById("ai-chat-box");
  chatBox.classList.toggle("open");

  // Show suggestions only when chat is opened and no message yet
  const suggestions = document.getElementById("ai-chat-suggestions");
  const messages = document.getElementById("ai-chat-messages");

  // Checks if any actual messages exist (excludes suggestion box)
  const hasMessages = Array.from(messages.children).some(child => child.id !== "ai-chat-suggestions");
  
  // Shows suggestions only when chat is opened and no actual messages exist
  if (chatBox.classList.contains("open") && !hasMessages) {
    suggestions.style.display = "flex";  // original layout
  } else {
    suggestions.style.display = "none";
  }
}

function insertSuggestion(text) {
  const input = document.getElementById("ai-chat-input");
  input.value = text;
  input.focus();
}

function sendMessage() {
  const input = document.getElementById("ai-chat-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";

  // Hide suggestions after first message
  const suggestions = document.getElementById("ai-chat-suggestions");
  if (suggestions) suggestions.style.display = "none";

  // Show typing/loading animation
  appendMessage("assistant", "Typing...", true);

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
  .then(res => res.json())
  .then(data => {
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
  msgDiv.innerHTML = marked.parse(text);   // Markdown to HTML

  if (isTyping) msgDiv.classList.add("typing-placeholder");
  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function removeTypingPlaceholder() {
  const placeholders = document.querySelectorAll(".typing-placeholder");
  placeholders.forEach(p => p.remove());
}

function clearChat() {
  const messages = document.getElementById("ai-chat-messages");
  
  // Remove all messages except suggestions
  Array.from(messages.children).forEach(child => {
    if (child.id !== "ai-chat-suggestions") {
      child.remove();
    }
  });

  // Show suggestions again
  const suggestions = document.getElementById("ai-chat-suggestions");
  if (suggestions) {
    suggestions.style.display = "flex";
  }

  // Scroll to top to make suggestions visible
  messages.scrollTop = 0;
}

// Make insertSuggestion globally accessible
window.insertSuggestion = insertSuggestion;
