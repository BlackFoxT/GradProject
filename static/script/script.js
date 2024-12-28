document.addEventListener("DOMContentLoaded", function () {
  console.log("Document loaded");
  
  // Fetch chat history when the document loads
  fetch("/get-chat-history", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      let chatHistory = null;
      if (!data.isUser) {
        chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];
      } else {
        chatHistory = data.chats;
      }

      // Show content if chat history or content is visible
      if (data.contentVisible || chatHistory.length > 0) {
        contentDiv.style.display = "block";

        // Display all stored chats
        if (chatHistory && chatHistory.length > 0) {
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
    })
    .catch((error) => {
      console.error("Error fetching chat history:", error);
      contentDiv.innerHTML +=
        "<div>An error occurred while fetching chat history.</div>";
    });

  const toggleSidebarButton = document.getElementById("toggle-sidebar");
  const sidebar = document.getElementById("sidebar");

  if (toggleSidebarButton && sidebar) {
    toggleSidebarButton.addEventListener("click", function () {
      sidebar.classList.toggle("show");
    });
  }

  const contentDiv = document.getElementById("hiddenContent");
  const chatDiv = document.getElementById("content");
  const header = document.getElementById("header");
  const textarea = document.getElementById("exampleFormControlTextarea1");

  // Event listener for form submission (sending messages)
  const messageForm = document.getElementById("messageForm");
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
        <div class="chat-question"><strong></strong> ${message}</div></div>`;
    contentDiv.style.display = "block";
    header.style.display = "none";
    chatDiv.style.marginTop = "10px";

    // Send the message to the Flask backend
    fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
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
            console.log("Stored chat in localStorage:", data.chat_entry);

            // Append new chat after displaying existing history
            chatHistory.forEach((chat) => {
              contentDiv.innerHTML += `
                <div class="chat-item">
                  <div class="chat-question"><strong></strong> ${chat.question}</div>
                  <div><strong></strong> ${chat.response}</div><hr></div>`;
            });
          } else {
            console.log(data.chats);
            contentDiv.innerHTML = ``;
            // Display the updated chat history
            data.chats.forEach((chat) => {
              contentDiv.innerHTML += `
                <div class="chat-item">
                  <div class="chat-question"><strong></strong> ${chat.question}</div>
                  <div><strong></strong> ${chat.response}</div><hr></div>`;
            });
          }
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
});
