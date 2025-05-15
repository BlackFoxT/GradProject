document.addEventListener("DOMContentLoaded", function () {
    fetch("/get-note-history")
    .then((response) => response.json())
    .then((notes) => {
      notes.forEach((note) => {
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
    
});

function addNotes(noteId, text){
        
        const notes = document.querySelectorAll('.note');
        let noteCount = notes.length+1;

        if(noteId){
            addNoteDiv(noteId, 0, text)
        } 
        else{
            fetch("/askForNote", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({ number : noteCount}),
              })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data.number)
                    noteCount = data.number;
                    addNoteDiv(null, noteCount, null)
    
        })
        .catch((error) => {
          console.error("Error:", error);
        });
        }
        
}

let index = 0;

function addNoteDiv(noteId, noteCount, text){
    const addNoteButton = document.getElementById("add-note");
    const container = document.getElementById("note-container");
    const noteContainer = document.getElementsByClassName("note");
    const allRows = container.querySelectorAll(".note-row");
    let targetRow = allRows[allRows.length - 1]; // Get the last row
    if(targetRow.querySelectorAll(".note")) notesInRow = targetRow.querySelectorAll(".note").length;
    else notesInRow = 0

    const notes = document.querySelectorAll('.note');
    let maxNotesInRow = 3;
    if (notesInRow >= maxNotesInRow) {
        // Create a new row
        const newRow = document.createElement("div");
        newRow.classList.add("note-row");
        let id = "note" + noteCount;

        while (document.getElementById(id)) {
            noteCount++;
            id = "note" + noteCount;
          }
        
        if (document.getElementById(id)) {
            index++;
        }
        
        const newNote = document.createElement("div");
        
        newNote.classList.add("note");
        newNote.id = id;
        newNote.addEventListener("click", function(event) {
            openNote(event, noteCount, index);
        });
        
       if(noteId) newNote.innerText = text
       else newNote.innerText = "Write something...";
        
        // Create the form and save button
        const form = document.createElement("form");
        form.id = "noteForm" + noteCount;
        
        const saveButton = document.createElement("button");
        if(noteId){
            saveButton.id = "submitNote" + noteId;
        }
        else{
            saveButton.id = "submitNote" + noteCount;
        }
        
        saveButton.type = "submit";
        saveButton.innerText = "Save";
        saveButton.style.display = "none";
        saveButton.className = "note-button";

        // Append note and button to the form
        form.appendChild(newNote);
        form.appendChild(saveButton);
        
        // Handle form submission
        form.addEventListener("submit", function (event) {
            saveNote(event, noteCount);
        });

        if(noteId){
            // === Delete Form ===
            const deleteForm = document.createElement("form");
            deleteForm.id = "deleteform" + noteCount;
            deleteForm.classList.add("deleteform");
            deleteForm.method = "POST";
            deleteForm.action = `/chat/delete/${noteId}`; 
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

        if(noteId){
            noteCount = noteId;
        } 

        let id = "note" + noteCount;
        
        while (document.getElementById(id)) {
            noteCount++;
            id = "note" + noteCount;
          }
          
        const newNote = document.createElement("div");
        newNote.id = id;
        
        newNote.classList.add("note");
        newNote.addEventListener("click", function(event) {
            openNote(event, noteCount, index);
        });

        if(noteId) newNote.innerText = text
        else newNote.innerText = "Write something...";

        const form = document.createElement("form");
        form.id = "noteForm" + noteCount;
        // Create the save button
        const saveButton = document.createElement("button");

        if(noteId){
            saveButton.id = "submitNote" + noteId;
        }
        else{
            saveButton.id = "submitNote" + noteCount;
        }
        
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
            deleteForm.id = "deleteform" + noteCount;
            deleteForm.classList.add("deleteform");
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
            event.preventDefault();
            const noteid = "note" + number;
            const noteElement = document.getElementById(noteid);
            const content = noteElement.innerText.trim();
            alert("Note " + number + " saved: ");

            const id = "submitNote" + number;
            document.getElementById(id).style.display="none";
            const allDeleteForm = document.querySelectorAll('.deleteform');
            allDeleteForm.forEach(form => {
                form.style.display = "block"; 
        
            });

            closeNote(number);

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
        location.reload();
}
function openNote(event, number, indext){
    
    const noteid = "note" + number;
    const noteElement = document.getElementById(noteid);
    const allNotes = document.querySelectorAll('.note');
    localStorage.setItem("content", 1); // Store in localStorage
    const notesArray = Array.from(allNotes); // convert to array
    const matches = notesArray.filter(note => note === noteElement);

        allNotes.forEach(note => {
            
            if (note !== noteElement) {
                note.style.display = "none";
            }
            
        }); 

        noteElement.classList.remove("note");
    noteElement.classList.add("openedNote");
    document.getElementById("add-note").style.display="none";
    document.getElementById("closeNote").style.display="block";

    const allDeleteForm = document.querySelectorAll('.deleteform');
    allDeleteForm.forEach(form => {
            form.style.display = "none"; 
        
    });

    const id = "submitNote" + number;

    document.getElementById(id).style.display="block";
    document.getElementById("closeNote").addEventListener("click", function () {
        console.log(number)
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
        const allDeleteForm = document.querySelectorAll('.deleteform');
        allDeleteForm.forEach(form => {
            form.style.display = "block"; 
        
        });

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