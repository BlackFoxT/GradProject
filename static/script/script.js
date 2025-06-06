document.addEventListener("DOMContentLoaded", function () {
  
  // Fetch chat history when the document loads
  fetch("/get-chat-history", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if(contentDiv){
        let chatHistory = null;
      if (!data.isUser) {
        chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];
        contentDiv.style.marginTop = "80px";
      } else {
        chatHistory = data.chats;    
      }
      // Show content if chat history or content is visible
      if (data.contentVisible || chatHistory.length > 0) {
        contentDiv.style.display = "block";

        // Display all stored chats
        if (chatHistory && chatHistory.length > 0) {
          let chatLength = data.chatCount % 10;
          if (data.isUser) {
            document.getElementById("takeNoteButton").style.display = "block";
            if(data.isQuizStarted && chatLength == 0){
              chatLength = 0;
            }
            setProgressBar(chatHistory, chatLength,data.chatId);
            if(chatLength == 0 && data.extraChat == 0){
              textarea.disabled = true;
              document.getElementById("askButton").style.display = "none";
              document.getElementById("quizButton").style.display = "block";
            }
            if(data.isQuizSubmitted == true){
              document.getElementById("askButton").style.display = "block";
              document.getElementById("quizButton").style.display = "none";
              document.getElementById("exampleFormControlTextarea1").disabled = false;
            }
          }

          chatHistory.forEach((chat) => {
            contentDiv.innerHTML += `
              <div class="chat-item">
                <div class="chat-question"><strong></strong> ${chat.question}</div>
                <div><strong></strong> ${chat.response}</div><hr></div>
            `;
          });
        }
        header.style.display = "none";
        chatDiv.style.marginTop = "10px";
      }
      scrollToBottom();
      }
    })
    .catch((error) => {
      console.error("Error fetching chat history:", error);
      contentDiv.innerHTML +=
        "<div>An error occurred while fetching chat history.</div>";
    });

  const toggleSidebarButton = document.getElementById("toggle-sidebar");
const sidebar = document.getElementById("sidebar");
const chat = document.getElementById("chat");

if (sidebar) {
  sidebar.classList.add("show"); // Sidebar is shown by default

  if (toggleSidebarButton) {
    toggleSidebarButton.addEventListener("click", function () {
      sidebar.classList.toggle("show");

      // Center the chat when sidebar is toggled
      if (chat) {
        chat.classList.toggle("center-chat");
      }
    });
  }
}


  const contentDiv = document.getElementById("hiddenContent");
  
  const chatDiv = document.getElementById("content");
  const header = document.getElementById("header");
  const textarea = document.getElementById("exampleFormControlTextarea1");
  
  // Event listener for form submission (sending messages)
  const messageForm = document.getElementById("messageForm");
  if (messageForm) {
    messageForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission
      const message = textarea.value.trim();
      if (!message) {
        textarea.focus();
        return;
      }
      textarea.value = "";

      // Display the user's message immediately
      contentDiv.innerHTML += `
        <div class="chat-item">
          <div class="chat-question"><strong></strong> ${message}</div></div>
          <div><strong></strong> Waiting for response...</div><hr></div>`;
      contentDiv.style.display = "block";
      header.style.display = "none";
      chatDiv.style.marginTop = "10px";
      scrollToBottom();
      document.getElementById("askButton").disabled = true;

      // Send the message to the Flask backend
      fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message, chatTopic: localStorage.getItem("chatTopic")}),
      })
        .then((response) => response.json())
        .then((data) => {
          
          if (data.chats || data.chat_entry) {
            if (!data.isUser) {
              // For unauthenticated users, store chat in localStorage temporarily
              let chatHistory =
                JSON.parse(localStorage.getItem("chatHistory")) || [];
              chatHistory.push(data.chat_entry);
              localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
              contentDiv.innerHTML = ``;

              // Append new chat after displaying existing history
              chatHistory.forEach((chat) => {
                contentDiv.innerHTML += `
                  <div class="chat-item">
                    <div class="chat-question"><strong></strong> ${chat.question}</div>
                    <div><strong></strong> ${chat.response}</div><hr></div>`;
              });
            } else {
              localStorage.removeItem("chatTopic");
              document.getElementById("takeNoteButton").style.display = "block";
              let chatLength = data.chatCount % 10;

              if(chatLength == 0 && data.extraChat == 0){
                textarea.disabled = true;
                document.getElementById("askButton").style.display = "none";
                document.getElementById("quizButton").style.display = "block";
              }
              if (data.chats.length === 1) {
                window.location.href = `http://127.0.0.1:5000/?chat_id=${data.chatId}`;
              } else {
                contentDiv.innerHTML = ""; // Clear previous content

                data.chats.forEach((chat) => {
                  contentDiv.innerHTML += `
                    <div class="chat-item">
                      <div class="chat-question"><strong></strong> ${chat.question}</div>
                      <div><strong></strong> ${chat.response}</div>
                      <hr>
                    </div>`;
                });
                const lastChat = data.chats[data.chats.length - 1];

                if (lastChat.question.slice(1).localeCompare('userinfo') == 0 || lastChat.question.slice(1).localeCompare('quiz') == 0
                || lastChat.question.slice(1).localeCompare('note') == 0) {
                  directCommand(lastChat.question.slice(1),data.chatId);
                }               
              }
              
              setProgressBar(data.chats, chatLength, data.chatId, data.isQuizSubmitted);
            }
            scrollToBottom();
            document.getElementById("askButton").disabled = false;
          } else if (data.error) {
            contentDiv.innerHTML += `<div>Error: ${data.error}</div>`;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          contentDiv.innerHTML +=
            "<div>An error occurred. Please try again.</div>";
        });
    });
  }
});

function directCommand(command, chat_id) {

  if (command.localeCompare('userinfo') == 0) {

    window.location.href = `http://127.0.0.1:5000/profile`; // Redirects to the profile page
  }
  else if (command.localeCompare('quiz') == 0) {
    window.location.href = `http://127.0.0.1:5000/quiz_start`;
  }
  else if (command.localeCompare('note') == 0) {
    window.location.href = `http://127.0.0.1:5000/note?chat_id=${chat_id}`;
  }
}

function scrollToBottom() {
  var hiddenContent = document.getElementById("hiddenContent");
  if (hiddenContent) { 
    hiddenContent.scrollTop = hiddenContent.scrollHeight;
  }
}

function openTopic(event) {
  // Display the modal and backdrop
  const topicDiv = document.getElementById("enterTopic");
  const backdrop = document.getElementById("backdrop");
  const progressBar = document.getElementById("progressBarr");
  progressBar.style.zIndex = "-1";
  topicDiv.style.display = "block";  // Show the modal
  backdrop.style.display = "block";  // Show the backdrop

  // Disable interactions with the page
  document.body.classList.add("modal-open");
}

function startChat(event) {
  event.preventDefault(); // Prevent any unintended form submission

  const topicInput = document.getElementById("chatTopic").value.trim();
  document.getElementById("progressBarr").style.zIndex = "0";
  if (topicInput) {
      localStorage.setItem("chatTopic", topicInput); // Store in localStorage
      closeTopic(); // Hide the topic popup
      window.location.href = `http://127.0.0.1:5000/`;
  } else {
      alert("Please enter a topic before starting the chat."); // Validation message
  }
  
}

function closeTopic() {
  const topicDiv = document.getElementById("enterTopic");
  const backdrop = document.getElementById("backdrop");

  topicDiv.style.display = "none";  // Hide the modal
  backdrop.style.display = "none";  // Hide the backdrop
  document.getElementById("progressBarr").style.zIndex = "0";
  // Enable interactions with the page
  document.body.classList.remove("modal-open");
}

function takeNote(event) {
  window.location.href = `http://127.0.0.1:5000/note`;
}

function startQuizz(event) {
  // Disable entire page interaction
  document.body.style.pointerEvents = "none";
  document.body.style.opacity = "0.5";

  // Create a full-screen overlay message
  const overlay = document.createElement("div");
  overlay.id = "waitingOverlay";
  overlay.style.position = "fixed";
  overlay.style.top = "0";
  overlay.style.left = "0";
  overlay.style.width = "100%";
  overlay.style.height = "100%";
  overlay.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
  overlay.style.color = "white";
  overlay.style.display = "flex";
  overlay.style.alignItems = "center";
  overlay.style.justifyContent = "center";
  overlay.style.zIndex = "9999";
  overlay.style.fontSize = "2rem";
  overlay.innerText = "Waiting for the quiz to start...";
  document.body.appendChild(overlay);

  fetch("/prepareQuestions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  })
    .then((response) => response.json())
    .then((data) => {
      // Remove overlay and re-enable interaction
      document.getElementById("waitingOverlay").remove();
      document.body.style.pointerEvents = "auto";
      document.body.style.opacity = "1";

      setProgressBar(null, 0, true)
      window.location.href = `http://127.0.0.1:5000/quiz_start`;
    })
    .catch((error) => {
      console.error("Error:", error);

      // Remove overlay and re-enable interaction
      document.getElementById("waitingOverlay").remove();
      document.body.style.pointerEvents = "auto";
      document.body.style.opacity = "1";

      const contentDiv = document.getElementById("content");
      contentDiv.innerHTML += "<div style='color: red;'>An error occurred. Please try again.</div>";
    });
}

function setProgressBar(chatHistory,chatLength,chatId,isQuizStarted){
  const progressDiv = document.getElementById("progressBarr");
  progressDiv.innerHTML = '';
            progressDiv.style.backgroundColor = "white"; // Change background color
            const maxChatLength= 10; // maximum chat sayısı
            let progressBarPercentage = 0; 

            if(chatHistory){
              progressBarPercentage = chatLength*10;//burda percentage'in 100ü aşmadığından emin oluyoruz.
              if(chatLength != 0 && chatLength%10 == 0){
                progressBarPercentage = Math.min((10/maxChatLength)*100,100); 
              }
            }
            if(isQuizStarted == true){
              progressBarPercentage = 0;
            }
            
            function getProgressBarColor(percentage){ //percentage'i hsl e göre hesaplıyoruz
              let hue = 120-(percentage *1.2);
              return `hsl(${hue},100%,50%)`;
            }

            let progressBarColor = getProgressBarColor(progressBarPercentage);
            progressDiv.innerHTML += `
                <div id="progressBar" class="progress-bar" role="progressbar" 
                style="width: ${progressBarPercentage}%; background-color: ${progressBarColor}; height: 10px;" 
                aria-valuenow="${progressBarPercentage}" 
                aria-valuemin="0" aria-valuemax="100" display="block">
                </div>`;
}