
document.addEventListener('DOMContentLoaded', function () {
  console.log("Document loaded");

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



  const contentDiv = document.getElementById('hiddenContent');
  const chatDiv = document.getElementById('content');
  const header = document.getElementById('header');
  const askButton = document.getElementById('askButton');
  const textarea = document.getElementById('exampleFormControlTextarea1');

  // Check localStorage to persist the visibility state
  if (localStorage.getItem('contentVisible') === 'true') {
    contentDiv.style.display = 'block';
    const storedMessage = localStorage.getItem('message');
    const storedResponse = localStorage.getItem('response');
    if (storedMessage && storedResponse) {
      contentDiv.innerHTML = `
          <div><strong>User:</strong> ${storedMessage}</div>
          <div><strong>Response:</strong> ${storedResponse}</div>
        `;
    }
    header.style.display = 'none';
    chatDiv.style.marginTop = '10px';
  }

  // Add event listener to the form submission
  const messageForm = document.getElementById('messageForm');
  messageForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    const message = textarea.value.trim();
    if (!message) {
      textarea.focus();
      return;
    }
    textarea.value = "";
    // Display the user's message immediately
    contentDiv.innerHTML = `<div><strong>User:</strong> ${message}</div>`;
    contentDiv.style.display = 'block';
    header.style.display = 'none';
    chatDiv.style.marginTop = '10px';

    // Store the message in localStorage
    localStorage.setItem('contentVisible', 'true');
    localStorage.setItem('message', message);

    // Send the message to the Flask backend
    fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message })
    })
      .then(response => response.json())
      .then(data => {
        if (data.response) {
          // After getting the response, display both the message and response
          contentDiv.innerHTML += `<div><strong>Response:</strong> ${data.response}</div>`;
          localStorage.setItem('response', data.response); // Store the response in localStorage
        } else {
          contentDiv.innerHTML += `<div>Error: ${data.error}</div>`;
        }
      })
      .catch(error => {
        console.error('Error:', error);
        contentDiv.innerHTML += "<div>An error occurred. Please try again.</div>";
      });
  });
});