// For Journal Feature

function summarizeJournal(journalId) {
  fetch(`get-journal-content/${journalId}`)
    .then(res => res.json())
    .then(data => {
      if (data.journal_texts) {
        const chatBox = document.getElementById("ai-chat-box");
        if (!chatBox.classList.contains("open")) {
          chatBox.classList.add("open");
        }

        const input = document.getElementById("ai-chat-input");
        input.value = `Summarize my journal:- \n\n${data.journal_texts}`;

        sendMessage(); // auto-send
      } else {
        alert("⚠️ Could not fetch journal content.");
      }
    })
    .catch(err => {
      console.error("Summarization error:", err);
      alert("⚠️ Something went wrong while summarizing.");
    });
}

// For Notes Feature

function summarizeNotes(noteId) {
  fetch(`get-notes-content/${noteId}`)
    .then(res => res.json())
    .then(data => {
      if (data.notes) {
        const chatBox = document.getElementById("ai-chat-box");
        if (!chatBox.classList.contains("open")) {
          chatBox.classList.add("open");
        }

        const input = document.getElementById("ai-chat-input");
        input.value = `Summarize my notes:- \n\n${data.notes}`;

        sendMessage(); // auto-send
      } else {
        alert("⚠️ Could not fetch notes content.");
      }
    })
    .catch(err => {
      console.error("Summarization error:", err);
      alert("⚠️ Something went wrong while summarizing.");
    });
}