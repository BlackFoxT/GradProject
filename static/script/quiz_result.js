window.onload = function () {
    const scoreEl = document.getElementById("score-table");
    const pointEl = document.getElementById("point-table");
    const passingScoreEl = document.getElementById("passing-score");
    const passingPointEl = document.getElementById("passing-point");
    const successCardEl = document.getElementById("succes-card");
    const failureCardEl = document.getElementById("failure-card");
    const tableBody = document.getElementById("answer-table-body");

    if (scoreEl && pointEl && passingScoreEl && passingPointEl && successCardEl && failureCardEl && tableBody) {
        const score = localStorage.getItem("quiz_score");
        const point = localStorage.getItem("quiz_point");
        const passed = localStorage.getItem("quiz_passed") === 'true';

        scoreEl.textContent = `${score}%`;
        pointEl.textContent = `${point}`;

        const passingScore = 70;
        const passingPoint = 7;

        passingScoreEl.textContent = `PASSING SCORE: ${passingScore}%`;
        passingPointEl.textContent = `PASSING POINT: ${passingPoint}`;

        if (passed) {
            successCardEl.style.display = "block";
            failureCardEl.style.display = "none";
        } else {
            successCardEl.style.display = "none";
            failureCardEl.style.display = "block";
        }

        const userAnswers = JSON.parse(localStorage.getItem("user_answers") || "[]");
        const correctAnswers = JSON.parse(localStorage.getItem("correct_answers") || "[]");

        for (let i = 0; i < userAnswers.length; i++) {
            const tr = document.createElement("tr");

            const indexTd = document.createElement("td");
            indexTd.textContent = i + 1;

            const userTd = document.createElement("td");
            userTd.textContent = userAnswers[i];

            const correctTd = document.createElement("td");
            correctTd.textContent = correctAnswers[i];

            const resultTd = document.createElement("td");
            resultTd.innerHTML = userAnswers[i] === correctAnswers[i]
                ? '<span class="text-success fw-bold">✔</span>'
                : '<span class="text-danger fw-bold">✘</span>';

            tr.appendChild(indexTd);
            tr.appendChild(userTd);
            tr.appendChild(correctTd);
            tr.appendChild(resultTd);

            tableBody.appendChild(tr);
        }

        // localStorage temizliği
        setTimeout(() => {
            localStorage.removeItem("quiz_score");
            localStorage.removeItem("quiz_point");
            localStorage.removeItem("quiz_passed");
            localStorage.removeItem("user_answers");
            localStorage.removeItem("correct_answers");
        }, 1000);
    }
};
