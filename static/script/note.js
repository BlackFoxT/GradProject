document.addEventListener("DOMContentLoaded", function () {
    fetch("/get-note-history")
    .then((response) => response.json())
    .then((notes) => {
        console.log(notes.length)
      notes.forEach((note) => {
        console.log(note.note_id)
        if(note.note_id >= 1){
            addNotes(note.note_id, note.text);
        }
        else{
            const noteDiv = document.getElementById("note" + note.note_id);
            if (noteDiv) {
              noteDiv.innerText = note.text;
            }
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching note history:", error);
      const contentDiv = document.getElementById("note-container");
      contentDiv.innerHTML +=
        "<div>An error occurred while fetching note history.</div>";
    });
  

    const addNoteButton = document.getElementById("add-note");
    
    
    addNoteButton.addEventListener("click", function () {
        addNotes();
    });
    /*const noteForm = document.getElementById("noteForm");
    noteForm.addEventListener("submit", function (event) {
        document.getElementById("submitNote").style.display="none";
        event.preventDefault();
        alert("Note saved: " + 2);
        localStorage.setItem("content", 2); // Store in localStorage
    });*/
    
    const form = document.getElementById("noteForm-1");
    if(form){
        form.addEventListener("submit", handleNoteSubmit(1));
    function handleNoteSubmit(noteCount) {
        return function(event) {
            event.preventDefault();
            const noteid = "note" + 1;
            const noteElement = document.getElementById(noteid);
            const content = noteElement.innerText.trim();
            alert("Note " + 1 + " saved: ");
            localStorage.setItem("note" + 1, content);
            const id = "submitNote" + 1;
            document.getElementById(id).style.display="none";
            closeNote(1);
            fetch("/saveNote", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({ content: content, number : 1}),
              })
                .then((response) => response.json())
                .then((data) => {
                    
        })
        .catch((error) => {
          console.error("Error:", error);
        });
        };
    }
    }
    
});

function addNotes(noteId, text){
    const addNoteButton = document.getElementById("add-note");
    const container = document.getElementById("note-container");
    const noteContainer = document.getElementsByClassName("note");
    const allRows = container.querySelectorAll(".note-row");
        let targetRow = allRows[allRows.length - 1]; // Get the last row
        if(targetRow.querySelectorAll(".note")) notesInRow = targetRow.querySelectorAll(".note").length;
        else notesInRow = 0
        console.log(notesInRow)
        

        let maxNotesInRow = 3;
        

        // If the last row already has the maximum number of notes (4), create a new row
        if (notesInRow >= maxNotesInRow) {
            // Create a new row
            const newRow = document.createElement("div");
            newRow.classList.add("note-row");

            const notes = document.querySelectorAll('.note');
            const noteCount = notes.length+1;
            //console.log(noteCount)
            const id = "note" + noteCount;
            // Create and add the new note
            const newNote = document.createElement("div");
            
            newNote.classList.add("note");
            newNote.id = id;
            newNote.addEventListener("click", function(event) {
                openNote(event, noteCount);
            });

           // newNote.contentEditable = "true";
           if(noteId) newNote.innerText = text
           else newNote.innerText = "Click here to type...";
            
            // Create the form and save button
            const form = document.createElement("form");
            form.id = "noteForm" + noteCount;

            const saveButton = document.createElement("button");
            saveButton.id = "submitNote" + noteCount;
            saveButton.type = "submit";
            saveButton.innerText = "Save";
            saveButton.style.display = "none";
            saveButton.className = "note-button";

            // Append note and button to the form
            form.appendChild(newNote);
            form.appendChild(saveButton);
            //console.log(noteCount)
            // Handle form submission
            form.addEventListener("submit", function (event) {
                saveNote(event, noteCount);
            });
            if(noteId){
                // === Delete Form ===
                const deleteForm = document.createElement("form");
                deleteForm.method = "POST";
                deleteForm.action = `/chat/delete/${noteId}`; // Replace with dynamic route if needed
                deleteForm.onsubmit = function () {
                    return confirm("Are you sure you want to delete this note?");
                };

                // Hidden method override input
                const hiddenInput = document.createElement("input");
                hiddenInput.type = "hidden";
                hiddenInput.name = "_method";
                hiddenInput.value = "DELETE";

                // Delete button
                const deleteButton = document.createElement("button");
                deleteButton.type = "submit";
                deleteButton.className = "btn btn-sm btn-white";
                deleteButton.innerText = "🗑️";

                // Append to delete form
                deleteForm.appendChild(hiddenInput);
                deleteForm.appendChild(deleteButton);

                // Append delete form after the note
                form.appendChild(deleteForm);
            }
        

            // Append form to the new row
            newRow.appendChild(form);

            // Remove the add button from the old row
            targetRow.removeChild(addNoteButton);

            // Append the add button to the new row
            newRow.appendChild(addNoteButton);

            // Append the new row to the container
            container.appendChild(newRow);
        } else {
            const notes = document.querySelectorAll('.note');
            const noteCount = notes.length+1;
            console.log(noteCount)
            const id = "note" + noteCount;
            const newNote = document.createElement("div");
            newNote.id = id;
            newNote.classList.add("note");
            newNote.addEventListener("click", function(event) {
                openNote(event, noteCount);
            });
            if(noteId) newNote.innerText = text
            else newNote.innerText = "Click here to type...";
            const form = document.createElement("form");
            form.id = "noteForm" + noteCount;
            // Create the save button
            const saveButton = document.createElement("button");
            saveButton.id = "submitNote" + noteCount;
            saveButton.type = "submit";
            saveButton.innerText = "Save";
            saveButton.style.display = "none";
            saveButton.className = "note-button";
            
            // Add note and button to form
            form.appendChild(newNote);
            form.appendChild(saveButton);
            form.addEventListener("submit", function (event) {
                saveNote(event, noteCount);
            });
            if(noteId){
                // === Delete Form ===
                const deleteForm = document.createElement("form");
                deleteForm.method = "POST";
                deleteForm.action = `/note/delete/${noteId}`; // Replace with dynamic route if needed
                deleteForm.onsubmit = function () {
                    return confirm("Are you sure you want to delete this note?");
                };

                // Hidden method override input
                const hiddenInput = document.createElement("input");
                hiddenInput.type = "hidden";
                hiddenInput.name = "_method";
                hiddenInput.value = "DELETE";

                // Delete button
                const deleteButton = document.createElement("button");
                deleteButton.type = "submit";
                deleteButton.className = "btn btn-sm btn-white";
                deleteButton.innerText = "🗑️";

                // Append to delete form
                deleteForm.appendChild(hiddenInput);
                deleteForm.appendChild(deleteButton);

                // Append delete form after the note
                form.appendChild(deleteForm);
            }
            // Add the form to the DOM
            targetRow.insertBefore(form, addNoteButton);
           // targetRow.insertBefore(newNote, addNoteButton);
        }
}

function saveNote(event, number){
    const form = document.getElementById("noteForm-" + number);
    //form.addEventListener("submit", handleNoteSubmit(1));
    //function handleNoteSubmit(noteCount) {
            event.preventDefault();
            const noteid = "note" + number;
            const noteElement = document.getElementById(noteid);
            const content = noteElement.innerText.trim();
            alert("Note " + number + " saved: ");
            //localStorage.setItem("note" + number, content);
            const id = "submitNote" + number;
            document.getElementById(id).style.display="none";
            closeNote(number);
            console.log(number)
            fetch("/saveNote", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({ content: content, number : number}),
              })
                .then((response) => response.json())
                .then((data) => {

        })
        .catch((error) => {
          console.error("Error:", error);
        });
    //}
}
function openNote(event, number){
    
    const noteElement = event.currentTarget;
    const allNotes = document.querySelectorAll('.note');
    localStorage.setItem("content", 1); // Store in localStorage
    console.log(number)
    allNotes.forEach(note => {
        if (note !== noteElement) {
            note.style.display = "none"; 
        }
    });
    noteElement.classList.remove("note");
    noteElement.classList.add("openedNote");
    document.getElementById("add-note").style.display="none";
    document.getElementById("closeNote").style.display="block";
    const id = "submitNote" + number;
    document.getElementById(id).style.display="block";
    document.getElementById("closeNote").addEventListener("click", function () {
        closeNote(number);
    });
    
    noteElement.contentEditable = "true";
    scrollToTop()
    const div = document.querySelector('.openedNote');
    if (div) { 
        div.scrollTop = div.scrollHeight;
    }
    if (div && div.scrollHeight > div.clientHeight) {
        // Scroll the div to its bottom
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth" // for a smooth scroll effect
          });
      }
}

function closeNote(number){
    const id = "note" + number;
    const noteElement = document.getElementById(id);
    if (noteElement) {

        noteElement.classList.remove("openedNote");
        noteElement.classList.add("note");
        noteElement.contentEditable = "false";
        document.getElementById("closeNote").style.display="none";
        document.getElementById("submitNote" + number).style.display="none";
        const allNotes = document.querySelectorAll('.note');

        allNotes.forEach(note => {
            note.style.display = "block"; 
        });
        document.getElementById("add-note").style.display="flex";
    } else {
        console.error("Note element not found with ID:", id);
    }
}

function scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: "smooth" // for a smooth scroll effect
    });
  }
 /* function scrollToBottom() {
    console.log("12212")
    const div = document.querySelector('.openedNote');
    if (div) { 
        div.scrollTop = div.scrollHeight;
    }
  }*/
  
// Create a form to wrap the note and save button
/*const form = document.createElement("form");
form.onsubmit = function(e) {
    e.preventDefault();
    const content = newNote.innerText.trim();
    localStorage.setItem("content", 1); // Store in localStorage

    console.log(1)
    if (content) {
        alert("Note saved: " + content); // Replace with your saving logic
    }

};*/