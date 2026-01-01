async function analyzeResume() {
  const resume = document.getElementById("resumeText").value;

  const res = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume })
  });

  const data = await res.json();

  // BULLETS
  const bulletsDiv = document.getElementById("bullets");
  const provDiv = document.getElementById("provability");
  bulletsDiv.innerHTML = "";
  provDiv.innerHTML = "";

  data.bullets.forEach(b => {
    bulletsDiv.innerHTML += `
      <div class="bullet">
        <strong>${b.text}</strong>
      </div>
    `;

    provDiv.innerHTML += `
      <div class="bullet">
        Provable:
        <span class="${b.provable ? "yes" : "no"}">
          ${b.provable ? "YES" : "NO"}
        </span>
        <div class="suggestion">
          ${b.provable ? "No suggestion needed." : b.suggestion}
        </div>
      </div>
    `;
  });

  // QUESTIONS
  const qDiv = document.getElementById("questions");
  qDiv.innerHTML = "";

  data.questions.forEach(q => {
  qDiv.innerHTML += `
    <div class="question-card">
      <div class="question-title">${q}</div>

      <input class="answer-box"
        placeholder="Type your answer and press Enter"
        onkeydown="if(event.key==='Enter') evaluateAnswer(this, '${q}')">

      <div class="evaluation"></div>
    </div>
  `;
});

}

async function evaluateAnswer(input, question) {
  const answer = input.value;
  const resultDiv = input.nextElementSibling;

  const res = await fetch("/evaluate-answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, answer })
  });

  const data = await res.json();
  resultDiv.innerText = data.evaluation;
}
document.getElementById("results").classList.remove("hidden");
