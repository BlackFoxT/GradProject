document.addEventListener("DOMContentLoaded", function () {
  console.log("Document loaded");

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
      if (data.contentVisible || chatHistory.length > 0) {
        contentDiv.style.display = "block";

        // Display all stored chats
        if (chatHistory && chatHistory.length > 0) {
          contentDiv.innerHTML = ""; // Clear existing content
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
      } else {
        // If no content is visible, maybe inform the user or keep the section hidden
        //contentDiv.innerHTML = "<div>No chat history available.</div>";
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
      if (sidebar.classList.contains("d-none")) {
        console.log(1);
        sidebar.classList.remove("d-none");
      } else {
        console.log(2);
        sidebar.classList.add("d-none");
      }
    });
  }

  const contentDiv = document.getElementById("hiddenContent");
  const chatDiv = document.getElementById("content");
  const header = document.getElementById("header");
  const askButton = document.getElementById("askButton");
  const textarea = document.getElementById("exampleFormControlTextarea1");

  // Add event listener to the form submission
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
    contentDiv.innerHTML += `<div class="chat-item">
          <div class="chat-question"><strong></strong> ${message}</div></div>`;
    contentDiv.style.display = "block";
    header.style.display = "none";
    chatDiv.style.marginTop = "10px";

    // Store the message in localStorage
    // localStorage.setItem('contentVisible', 'true');
    //localStorage.setItem('message', message);
    // Check the server to persist the visibility state and chat history

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
            contentDiv.innerHTML = ""; // Clear current content
            // Retrieve and display all chats stored in localStorage
            chatHistory.forEach((chat) => {
              contentDiv.innerHTML += `
              <div class="chat-item">
                <div class="chat-question"><strong></strong> ${chat.question}</div>
                <div><strong></strong> ${chat.response}</div><hr> </div>`;
            });
          } else {
            // Display the updated chat history
            contentDiv.innerHTML = ""; // Clear current content
            data.chats.forEach((chat) => {
              contentDiv.innerHTML += `
          <div class="chat-item">
            <div class="chat-question"><strong></strong> ${chat.question}</div>
            <div><strong></strong> ${chat.response}</div><hr> </div>`;
            }); //<div><em>${chat.timestamp}</em></div>
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
