import "./style.css";

const API_URL = "http://127.0.0.1:8000/chat";
let isFirstMessage = true;

const launcherEl = document.getElementById("chat-launcher");
const containerEl = document.getElementById("chat-container");
const closeEl = document.getElementById("chat-close");
const messagesEl = document.getElementById("chat-messages");
const inputEl = document.getElementById("chat-input");
const sendEl = document.getElementById("chat-send");

// Open/close toggle
launcherEl.addEventListener("click", () => {
  containerEl.classList.remove("hidden");
  launcherEl.classList.add("hidden");
});

closeEl.addEventListener("click", () => {
  containerEl.classList.add("hidden");
  launcherEl.classList.remove("hidden");
});

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "msg " + sender;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage() {
  const query = inputEl.value.trim();
  if (!query) return;

  addMessage(query, "user");
  inputEl.value = "";
  sendEl.disabled = true;

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        language: "Swedish",
        is_first_message: isFirstMessage,
      }),
    });

    const data = await res.json();
    addMessage(data.answer, "bot");
    isFirstMessage = false;
  } catch (err) {
    addMessage("Något gick fel. Försök igen senare.", "bot");
  } finally {
    sendEl.disabled = false;
  }
}

sendEl.addEventListener("click", sendMessage);
inputEl.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});