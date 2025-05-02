function renderQuestion(index) {
    const questionData = questions[index];
    const qQuestion = document.getElementById("quiz-question");
    const qOptions = document.getElementById("quiz-options");
    qQuestion.textContent = index + 1 + ") " + questionData.question;
    qOptions.innerHTML = "";

    questionData.options.forEach((option, i) => {
        const container = document.createElement("div");
        const input = document.createElement("input");

        input.type = "radio";
        input.name = "multiple-choice";
        input.id = `question-${index}-option-${i}`;
        input.value = option;

        const label = document.createElement("label");
        label.setAttribute("for", input.id);
        label.textContent = option;

        input.addEventListener("change", () => {
            userAnswers[index] = input.value;
        });

        // Seçilen cevabı göster
        if (userAnswers[index] === option) {
            input.checked = true;
        }

        container.appendChild(input);
        container.appendChild(label);
        qOptions.appendChild(container);
    });
}

let currentQuestionIndex = 0;
let quiz_id = null;
let questions = null;
let userAnswers = [];
let correctAnswers = [];

fetch("/get-quiz-questions", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
})
    .then((response) => response.json())
    .then((data) => {
        quiz_id = data.quiz_id;
        questions = data.questions;
        correctAnswers = questions.map(q => q.correct_answer);
        userAnswers = new Array(questions.length).fill(" "); // default olarak hepsini " " şeklinde ekliyoruz
        renderQuestion(currentQuestionIndex);
    })
    .catch((error) => {
        console.error("Error fetching quiz questions:", error);
        contentDiv.innerHTML += "<div>An error occurred while fetching quiz questions.</div>";
    });

const timer = document.getElementById("time-left");
let timeLeft = 600;

timer.textContent = `${Math.floor(timeLeft / 60)}:${timeLeft % 60 < 10 ? '0' : ''}${timeLeft % 60}`;

const timerInterval = setInterval(() => {
    const min = Math.floor(timeLeft / 60);
    const sec = timeLeft % 60;

    timer.textContent = `${min}:${sec < 10 ? '0' : ''}${sec}`;
    timeLeft--;

    if (timeLeft < 5) {
        timer.style.color = "red";
    }

    if (timeLeft < 0) {
        clearInterval(timerInterval);
        submitQuiz();
    }
}, 1000);

function BackQuestion(event) {
    event.preventDefault();
    const backButton = document.getElementById("back-button");
    const nextButton = document.getElementById("nextButton");
    const submitButton = document.getElementById("submit-button");

    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderQuestion(currentQuestionIndex);
        nextButton.style.display = "block";
        submitButton.style.display = "none";
        submitButton.disabled = true;
        nextButton.disabled = false;
    }
    if (currentQuestionIndex == 0) {
        backButton.style.display = "none";
        backButton.disabled = true;
    }
}

function nextQuestion(event) {
    event.preventDefault();
    const nextButton = document.getElementById("nextButton");
    const backButton = document.getElementById("back-button");
    const submitButton = document.getElementById("submit-button");

    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        renderQuestion(currentQuestionIndex);
        backButton.style.display = "block";
        backButton.disabled = false;

        if (currentQuestionIndex === questions.length - 1) {
            submitButton.style.display = "block";
            submitButton.disabled = false;
            nextButton.style.display = "none";
            nextButton.disabled = true;
        }
    }
}

function submitQuiz(event) {
    if (event) event.preventDefault();
    clearInterval(timerInterval);

    let correct = 0;
    for (let i = 0; i < questions.length; i++) {
        if (userAnswers[i] === correctAnswers[i]) {
            correct++;
        }

        console.log(`Question ${i + 1}:`);
        console.log(`User Answer: ${userAnswers[i]}`);
        console.log(`Correct Answer: ${correctAnswers[i]}`);
    }

    const scorePercentage = correct * 10;
    const passingScore = 7;
    //const point = correct;
    const result = {
        quiz_id: quiz_id,
        score: scorePercentage,
        point: correct,
        passed: correct >= passingScore,
        userAnswers: userAnswers,
        correctAnswers: correctAnswers,
    };
    fetch('http://127.0.0.1:5000/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result),
    })
    .then(res => res.json())
    .then(data => {
        console.log("Submitted to DB:", data);
        window.location.href = `http://127.0.0.1:5000/quiz_result`;
    })
    .catch(err => {
        console.error("Error submitting:", err);
    });
    //localStorage.setItem("isSumbittedChatID" + chatId, true);
}
