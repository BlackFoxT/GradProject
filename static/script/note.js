document.addEventListener("DOMContentLoaded", function () {

    const addNoteButton = document.getElementById("add-note");
    const container = document.getElementById("note-container");
    const noteContainer = document.getElementsByClassName("note");
    
    addNoteButton.addEventListener("click", function () {
        const allRows = container.querySelectorAll(".note-row");
        let targetRow = allRows[allRows.length - 1]; // Get the last row
        const notesInRow = targetRow.querySelectorAll(".note").length;

        let maxNotesInRow = 3;
        

        // If the last row already has the maximum number of notes (4), create a new row
        if (notesInRow >= maxNotesInRow) {
            // Create a new row
            const newRow = document.createElement("div");
            newRow.classList.add("note-row");

            const notes = document.querySelectorAll('.note');
            const noteCount = notes.length+1;
            const id = "note" + noteCount;
            // Create and add the new note
            const newNote = document.createElement("div");
            
            newNote.classList.add("note");
            newNote.id = id;
            newNote.addEventListener("click", function(event) {
                openNote(event, noteCount);
            });

           // newNote.contentEditable = "true";
            newNote.innerText = "Click here to type...";
            newRow.appendChild(newNote);
            
            // Remove the add button from the old row
            targetRow.removeChild(addNoteButton);

            // Append the add button to the new row
            newRow.appendChild(addNoteButton);
            
            // Append the new row to the container
            container.appendChild(newRow);
        } else {
            const notes = document.querySelectorAll('.note');
            const noteCount = notes.length+1;
            const id = "note" + noteCount;
            const newNote = document.createElement("div");
            newNote.id = id;
            newNote.classList.add("note");
            newNote.addEventListener("click", function(event) {
                openNote(event, noteCount);
            });
            newNote.innerText = "Click here to type...";
            targetRow.insertBefore(newNote, addNoteButton);
        }
    });
});

function openNote(event, number){
    const noteElement = event.currentTarget;
    const allNotes = document.querySelectorAll('.note');

    allNotes.forEach(note => {
        if (note !== noteElement) {
            note.style.display = "none"; 
        }
    });
    noteElement.classList.remove("note");
    noteElement.classList.add("openedNote");
    document.getElementById("add-note").style.display="none";
    document.getElementById("closeNote").style.display="block";
    document.getElementById("closeNote").addEventListener("click", function () {
        closeNote(number);
    });
    
    noteElement.contentEditable = "true";
    scrollToTop()
}

function closeNote(number){
    const id = "note" + number;
    const noteElement = document.getElementById(id);
    if (noteElement) {

        noteElement.classList.remove("openedNote");
        noteElement.classList.add("note");
        noteElement.contentEditable = "false";
        document.getElementById("closeNote").style.display="none";
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
  
  