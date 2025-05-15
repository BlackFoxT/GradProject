fetch("/quiz/result", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
})
    .then((response) => response.json())
    .then((data) => {
        const scoreEl = document.getElementById("score-table");
        const pointEl = document.getElementById("point-table");
        const passingScoreEl = document.getElementById("passing-score");
        const passingPointEl = document.getElementById("passing-point");
        const successCardEl = document.getElementById("succes-card");
        const failureCardEl = document.getElementById("failure-card");
        const tableBody = document.getElementById("answer-table-body");

        if (!scoreEl || !pointEl || !passingScoreEl || !passingPointEl || !successCardEl || !failureCardEl || !tableBody) return;

        const score = data.score;
        const point = data.point;
        const passed = data.passed;
        const userAnswers = data.userAnswers;
        const correctAnswers = data.correctAnswers;

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
    })
    .catch((error) => {
        console.error("Error fetching quiz result:", error);
    });