
/* =========================================
   EMAILJS CONFIGURATION
========================================= */

const EMAILJS_PUBLIC_KEY = "*zsCA67b0X9-S_GZ*";
const EMAILJS_SERVICE_ID = "service_gjby0rb";
const EMAILJS_TEMPLATE_ID = "template_2yz4t1l";

const YOUR_NAME = "Keem";
const YOUR_EMAIL = "hakeemonest@gmail.com";

// Initialize EmailJS
if (window.emailjs) {
  emailjs.init({
    publicKey: EMAILJS_PUBLIC_KEY
  });
}

/* =========================================
   ELEMENTS AND STATE
========================================= */

const yesBtn = document.getElementById("yesBtn");
const noBtn = document.getElementById("noBtn");
const buttonArea = document.getElementById("buttonArea");
const hint = document.getElementById("hint");
const attemptMessage = document.getElementById("attemptMessage");
const success = document.getElementById("success");
const emailStatus = document.getElementById("emailStatus");

let noAttempts = 0;
let accepted = false;
let noHidden = false;

const MAX_NO_ATTEMPTS = 10;

/* =========================================
   NO BUTTON: RUN AWAY
========================================= */

function moveNoButton() {
  if (accepted || noHidden) return;

  noAttempts++;

  if (noAttempts >= MAX_NO_ATTEMPTS) {
    noBtn.style.display = "none";
    noHidden = true;

    attemptMessage.textContent =
      "The No button disappeared! 😭💕 Now it's just you and YES!";

    hint.textContent = "Maybe it's a sign! 💘";
    return;
  }

  noBtn.classList.add("running");

  const padding = 15;
  const maxX = Math.max(
    padding,
    window.innerWidth - noBtn.offsetWidth - padding
  );
  const maxY = Math.max(
    padding,
    window.innerHeight - noBtn.offsetHeight - padding
  );

  const x = padding + Math.random() * (maxX - padding);
  const y = padding + Math.random() * (maxY - padding);

  noBtn.style.left = `${x}px`;
  noBtn.style.top = `${y}px`;

  const messages = [
    "Hehe, too slow! 😝",
    "Are you sure about that? 🥹💕",
    "Catch me if you can! 🏃‍♀️",
    "Give YES a chance! 💗",
    "Don't break my heart! 😭💔",
    "You know which button to choose! 😏💘",
    "Not so fast! 🙈",
    "YES is looking cute, though! 💖"
  ];

  hint.textContent =
    messages[Math.floor(Math.random() * messages.length)];

  attemptMessage.textContent =
    `${noAttempts} of ${MAX_NO_ATTEMPTS} attempts 🙈`;
}

// Desktop hover
noBtn.addEventListener("pointerenter", (event) => {
  if (event.pointerType === "mouse") {
    moveNoButton();
  }
});

// Mobile touch
noBtn.addEventListener("touchstart", (event) => {
  event.preventDefault();
  moveNoButton();
}, { passive: false });

// Fallback click
noBtn.addEventListener("click", (event) => {
  event.preventDefault();
  moveNoButton();
});

// Keep the button within the screen when resized
window.addEventListener("resize", () => {
  if (noBtn.classList.contains("running") && !noHidden) {
    const maxX = Math.max(
      0, window.innerWidth - noBtn.offsetWidth
    );
    const maxY = Math.max(
      0, window.innerHeight - noBtn.offsetHeight
    );

    noBtn.style.left =
      `${Math.min(parseFloat(noBtn.style.left) || 0, maxX)}px`;

    noBtn.style.top =
      `${Math.min(parseFloat(noBtn.style.top) || 0, maxY)}px`;
  }
});

/* =========================================
   YES BUTTON: CELEBRATION + EMAIL
========================================= */

yesBtn.addEventListener("click", async () => {
  if (accepted) return;

  accepted = true;
  yesBtn.disabled = true;

  noBtn.style.display = "none";
  hint.textContent = "";
  attemptMessage.textContent = "";
  buttonArea.classList.add("hidden");

  // Reveal the romantic success message
  success.classList.remove("hidden");

  // Launch fireworks
  startFireworks();

  // Check EmailJS is available
  if (!window.emailjs) {
    emailStatus.textContent =
      "She said YES! 🎉 EmailJS did not load. Check your internet connection.";
    return;
  }

  emailStatus.textContent = "Sending your notification... 💌";

  try {
    await emailjs.send(
      EMAILJS_SERVICE_ID,
      EMAILJS_TEMPLATE_ID,
      {
        to_email: YOUR_EMAIL,
        to_name: YOUR_NAME,
        from_name: "Neveah",
        response: "YES 💖",
        message:
          "Neveah clicked YES! 💖 She agreed to be your girlfriend!",
        reply_to: YOUR_EMAIL
      }
    );

    emailStatus.textContent =
      "Your YES notification has been sent! 💌 Check your inbox.";
  } catch (error) {
    console.error("EmailJS error:", error);

    emailStatus.textContent =
      "She said YES! 🎆 But the email failed. Check your EmailJS template settings.";
  }
});

/* =========================================
   FIREWORKS
========================================= */

const canvas = document.getElementById("fireworks");
const ctx = canvas.getContext("2d");

let particles = [];
let animationRunning = false;
let fireworkEnd = 0;

function resizeCanvas() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  canvas.width = window.innerWidth * dpr;
  canvas.height = window.innerHeight * dpr;

  canvas.style.width = `${window.innerWidth}px`;
  canvas.style.height = `${window.innerHeight}px`;

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

resizeCanvas();
window.addEventListener("resize", resizeCanvas);

function burst(x, y) {
  const colors = [
    "#ff5da2",
    "#ffd166",
    "#ffffff",
    "#c77dff",
    "#ff8fab",
    "#7bf1a8"
  ];

  const color =
    colors[Math.floor(Math.random() * colors.length)];

  for (let i = 0; i < 75; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 1.5 + Math.random() * 5;

    particles.push({
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 1,
      decay: 0.008 + Math.random() * 0.014,
      size: 1.5 + Math.random() * 3,
      color
    });
  }
}

function startFireworks() {
  fireworkEnd = performance.now() + 7000;

  burst(
    window.innerWidth * 0.25,
    window.innerHeight * 0.3
  );

  burst(
    window.innerWidth * 0.75,
    window.innerHeight * 0.3
  );

  burst(
    window.innerWidth * 0.5,
    window.innerHeight * 0.2
  );

  if (!animationRunning) {
    animationRunning = true;
    requestAnimationFrame(animateFireworks);
  }
}

function animateFireworks(now) {
  ctx.clearRect(
    0, 0, window.innerWidth, window.innerHeight
  );

  if (now < fireworkEnd && Math.random() < 0.09) {
    burst(
      window.innerWidth * (0.1 + Math.random() * 0.8),
      window.innerHeight * (0.1 + Math.random() * 0.45)
    );
  }

  particles = particles.filter(p => p.life > 0);

  for (const p of particles) {
    p.x += p.vx;
    p.y += p.vy;
    p.vy += 0.035;
    p.vx *= 0.99;
    p.life -= p.decay;

    ctx.globalAlpha = Math.max(0, p.life);
    ctx.fillStyle = p.color;

    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.globalAlpha = 1;

  if (now < fireworkEnd || particles.length > 0) {
    requestAnimationFrame(animateFireworks);
  } else {
    ctx.clearRect(
      0, 0, window.innerWidth, window.innerHeight
    );

    animationRunning = false;
  }
}
