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

let hasGreeted = false;

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function showGreeting() {
  if (hasGreeted) return;
  hasGreeted = true;

  showTyping();
  await delay(1200);
  hideTyping();
  addMessage(
  "Hej! 👋 Jag är Studieassistenten, en AI-assistent för Högskolan på Åland.\n" +
  "Jag hjälper till med frågor om program, antagning och praktisk info , på svenska eller engelska. Jag kan ha fel ibland, så dubbelkolla viktiga datum, och dela inte personuppgifter här.",
  "bot"
  );

  showTyping();
  await delay(900);
  hideTyping();
  addMessage("Vad kan jag hjälpa dig med?", "bot");
}

launcherEl.addEventListener("click", () => {
  containerEl.classList.remove("hidden");
  launcherEl.classList.add("hidden");
  showGreeting();
});

async function sendMessage() {
  const query = inputEl.value.trim();
  if (!query) return;

  addMessage(query, "user");
  inputEl.value = "";
  sendEl.disabled = true;

  showTyping();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        language: "Swedish",
      }),
    });

    const data = await res.json();
    hideTyping();
    addMessage(data.answer, "bot");
  } catch (err) {
    hideTyping();
    addMessage("Något gick fel. Försök igen senare.", "bot");
  } finally {
    sendEl.disabled = false;
  }
}

sendEl.addEventListener("click", sendMessage);
inputEl.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function showTyping() {
  const div = document.createElement("div");
  div.className = "msg bot typing";
  div.id = "typing-indicator";
  div.innerHTML = `<span></span><span></span><span></span>`;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function hideTyping() {
  const typingEl = document.getElementById("typing-indicator");
  if (typingEl) typingEl.remove();
}