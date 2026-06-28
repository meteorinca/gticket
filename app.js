// app.js
const ticketWrap = document.getElementById("ticketWrap");
const ticket = document.getElementById("ticket");
const messageBox = document.getElementById("ticketMessage");
const openBtn = document.getElementById("openBtn");
const shineBtn = document.getElementById("shineBtn");
const flipBtn = document.getElementById("flipBtn");

const fallbackMessage = `
# Milly Monka’s Golden Ticket

This ticket grants one curious human entry into a world of chocolate rivers, impossible doors, fizzy inventions, and one very serious rule:

**Never stop wondering.**

- Admit one dreamer
- Bring imagination
- Leave ordinary at the gate
`;

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderMarkdown(markdown) {
  const lines = markdown.trim().split("\n");
  let html = "";
  let inList = false;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (!line) {
      if (inList) {
        html += "</ul>";
        inList = false;
      }
      continue;
    }

    if (line.startsWith("# ")) {
      if (inList) {
        html += "</ul>";
        inList = false;
      }
      html += `<h1>${formatInline(line.slice(2))}</h1>`;
      continue;
    }

    if (line.startsWith("## ")) {
      if (inList) {
        html += "</ul>";
        inList = false;
      }
      html += `<h2>${formatInline(line.slice(3))}</h2>`;
      continue;
    }

    if (line.startsWith("- ")) {
      if (!inList) {
        html += "<ul>";
        inList = true;
      }
      html += `<li>${formatInline(line.slice(2))}</li>`;
      continue;
    }

    if (inList) {
      html += "</ul>";
      inList = false;
    }

    html += `<p>${formatInline(line)}</p>`;
  }

  if (inList) {
    html += "</ul>";
  }

  return html;
}

function formatInline(text) {
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>");
}

async function loadMessage() {
  try {
    const response = await fetch("message.md", { cache: "no-store" });

    if (!response.ok) {
      throw new Error("Could not load message.md");
    }

    const markdown = await response.text();
    messageBox.innerHTML = renderMarkdown(markdown);
  } catch (error) {
    messageBox.innerHTML = renderMarkdown(fallbackMessage);
  }
}

function createSparkles(amount = 70) {
  for (let i = 0; i < amount; i++) {
    const sparkle = document.createElement("span");
    sparkle.className = "sparkle";

    const size = Math.random() * 4 + 2;
    const x = Math.random() * 100;
    const y = Math.random() * 105 + 5;
    const dx = (Math.random() * 180 - 90).toFixed(1);
    const duration = Math.random() * 7 + 5;
    const delay = Math.random() * -12;

    sparkle.style.setProperty("--s", `${size}px`);
    sparkle.style.setProperty("--x", `${x}vw`);
    sparkle.style.setProperty("--y", `${y}vh`);
    sparkle.style.setProperty("--dx", `${dx}px`);
    sparkle.style.setProperty("--d", `${duration}s`);
    sparkle.style.animationDelay = `${delay}s`;

    document.body.appendChild(sparkle);
  }
}

function setPointerLight(event) {
  const rect = ticketWrap.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  const px = x / rect.width;
  const py = y / rect.height;

  const rotateY = (px - 0.5) * 14;
  const rotateX = (0.5 - py) * 10;

  document.documentElement.style.setProperty("--mx", `${event.clientX}px`);
  document.documentElement.style.setProperty("--my", `${event.clientY}px`);
  ticketWrap.style.setProperty("--ry", `${rotateY}deg`);
  ticketWrap.style.setProperty("--rx", `${rotateX}deg`);
}

function resetTilt() {
  ticketWrap.style.setProperty("--ry", "0deg");
  ticketWrap.style.setProperty("--rx", "0deg");
}

function openTicket() {
  ticketWrap.classList.remove("ticket-opened");
  void ticketWrap.offsetWidth;
  ticketWrap.classList.add("ticket-opened");
}

function replayShine() {
  ticketWrap.classList.remove("shine-run");
  void ticketWrap.offsetWidth;
  ticketWrap.classList.add("shine-run");

  setTimeout(() => {
    ticketWrap.classList.remove("shine-run");
  }, 1200);
}

function flipTicket() {
  ticketWrap.classList.toggle("ticket-flipped");
}

ticketWrap.addEventListener("pointermove", setPointerLight);
ticketWrap.addEventListener("pointerleave", resetTilt);
ticketWrap.addEventListener("click", openTicket);

ticketWrap.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    openTicket();
  }
});

openBtn.addEventListener("click", openTicket);
shineBtn.addEventListener("click", replayShine);
flipBtn.addEventListener("click", flipTicket);

window.addEventListener("pointermove", (event) => {
  document.documentElement.style.setProperty("--mx", `${event.clientX}px`);
  document.documentElement.style.setProperty("--my", `${event.clientY}px`);
});

loadMessage();
createSparkles();
setTimeout(openTicket, 600);