function renderQuestion(index) {

    const questionData = questions[index];
    const qQuestion = document.getElementById("quiz-question");
    const qOptions = document.getElementById("quiz-options");
    qQuestion.textContent= index+1 +") "+ questionData.question;
    qOptions.innerHTML="";

    questionData.options.forEach((option,i) => {
        
        const container = document.createElement("div");
        const input = document.createElement("input");

        input.type = "radio";
        input.name = "multiple-choice";
        //////////////////// bunun alttaki iki satır
        input.id = `question-${index}-option-${i}`; // değiştirilebilir
        input.value = option;

        const label = document.createElement("label");
        label.setAttribute("for", `question-${index}-option-${i}`);
        label.textContent = option;

        container.appendChild(input);
        container.appendChild(label);
        qOptions.appendChild(container);
    });
}

let currentQuestionIndex=0;
let questions = null;

fetch("/get-quiz-questions", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
    })
    .then((response) => response.json())
    .then((data) => {
        questions = data.questions;
        renderQuestion(currentQuestionIndex);
    })
    .catch((error) => {
        console.error("Error fetching quiz questions:", error);
        contentDiv.innerHTML +=
        "<div>An error occurred while fetching quiz questions.</div>";
    });

// Flask tarafından gönderilen JSON verisini al
// const quizDataElement = document.getElementById("quiz-data");
// const quizQuestions = JSON.parse(quizDataElement.getAttribute("data-quiz"));

const timer=document.getElementById("time-left");
let timeLeft=600;

timer.textContent=`${Math.floor(timeLeft/60)}:${timeLeft%60 < 10 ? '0' : ''}${timeLeft%60}`;

const timerInterval = setInterval(()=>{
    const min= Math.floor(timeLeft/60);
    const sec= timeLeft%60;

    timer.textContent=`${min}:${sec < 10 ? '0' : ''}${sec}`;
    timeLeft--;

    if(timeLeft<5){
        timer.style.color="red";
    }

    if(timeLeft<0){
        clearInterval(timerInterval);
    }
},1000);

function BackQuestion() {
    const backButton = document.getElementById("back-button");
    const nextButton = document.getElementById("nextButton");
    const submitButton = document.getElementById("submit-button");
    if(currentQuestionIndex > 0){
        currentQuestionIndex--;
        renderQuestion(currentQuestionIndex);
        nextButton.style.display = "block";
        submitButton.style.display = "none";
    }
    if(currentQuestionIndex == 0){
        backButton.style.display="none";
    }
}

function nextQuestion() {
    const nextButton = document.getElementById("nextButton");
    const backButton = document.getElementById("back-button");
    const submitButton = document.getElementById("submit-button");
    if(currentQuestionIndex < questions.length - 1 ){
        currentQuestionIndex++;
        renderQuestion(currentQuestionIndex);
        backButton.style.display="block";

        if (currentQuestionIndex === questions.length - 1) {
            submitButton.style.display = "block";
            nextButton.style.display = "none";
        }
    }
  }

function submitQuiz() {
    window.location.href = `http://127.0.0.1:5000/quiz_result`;
}
