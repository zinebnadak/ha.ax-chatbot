import "./style.css";

const API_URL = "https://ha-ax-chatbot.onrender.com/chat";
let currentLanguage = "Swedish";
let hasGreeted = false;
let greetedLanguages = new Set();

const launcherEl = document.getElementById("chat-launcher");
const containerEl = document.getElementById("chat-container");
const closeEl = document.getElementById("chat-close");
const messagesEl = document.getElementById("chat-messages");
const inputEl = document.getElementById("chat-input");
const sendEl = document.getElementById("chat-send");
const titleEl = document.getElementById("chat-title");
const langOptions = document.querySelectorAll(".lang-option");

updateHeaderTitle(currentLanguage);

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "msg " + sender;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

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

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function updateHeaderTitle(lang) {
  titleEl.textContent = lang === "English" ? "Study Assistant" : "Studieassistent";
}

async function greetInLanguage(lang) {
  const isEnglish = lang === "English";

  showTyping();
  await delay(1200);
  hideTyping();
  addMessage(
    isEnglish
      ? "Hi! 👋 I'm the Study Assistant, an AI assistant for Åland University of Applied Sciences.\nI help with questions about programmes, admissions, and practical info — in Swedish or English. I can sometimes be wrong, so double-check important dates, and don't share personal data here."
      : "Hej! 👋 Jag är Studieassistenten, en AI-assistent för Högskolan på Åland.\nJag hjälper till med frågor om program, antagning och praktisk info — på svenska eller engelska. Jag kan ha fel ibland, så dubbelkolla viktiga datum, och dela inte personuppgifter här.",
    "bot"
  );

  showTyping();
  await delay(900);
  hideTyping();
  addMessage(isEnglish ? "How can I help you?" : "Vad kan jag hjälpa dig med?", "bot");

  greetedLanguages.add(lang);
}

async function showGreeting() {
  if (hasGreeted) return;
  hasGreeted = true;
  await greetInLanguage("Swedish");
}

langOptions.forEach((option) => {
  option.addEventListener("click", async () => {
    const newLang = option.dataset.lang;
    if (newLang === currentLanguage) return;

    currentLanguage = newLang;
    updateHeaderTitle(newLang);
    langOptions.forEach((o) => o.classList.toggle("active", o.dataset.lang === newLang));

    if (!greetedLanguages.has(newLang)) {
      await greetInLanguage(newLang);
    }
  });
});

launcherEl.addEventListener("click", () => {
  containerEl.classList.remove("hidden");
  launcherEl.classList.add("hidden");
  showGreeting();
});

closeEl.addEventListener("click", () => {
  containerEl.classList.add("hidden");
  launcherEl.classList.remove("hidden");
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
        language: currentLanguage,
      }),
    });

    hideTyping();

    if (res.status === 429) {
      addMessage(
        currentLanguage === "English"
          ? "You're sending messages too quickly. Please wait a moment and try again."
          : "Du skickar meddelanden för snabbt. Vänta en stund och försök igen.",
        "bot"
      );
      return;
    }

    if (!res.ok) {
      throw new Error("Request failed");
    }

    const data = await res.json();
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