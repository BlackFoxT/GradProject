document.addEventListener("DOMContentLoaded", function () {

    const addNoteButton = document.getElementById("add-note");
    const container = document.getElementById("note-container");

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

            // Create and add the new note
            const newNote = document.createElement("div");
            
            newNote.classList.add("note");
            newNote.contentEditable = "true";
            newNote.innerText = "Click here to type...";
            newRow.appendChild(newNote);
            
            // Remove the add button from the old row
            targetRow.removeChild(addNoteButton);

            // Append the add button to the new row
            newRow.appendChild(addNoteButton);
            
            // Append the new row to the container
            container.appendChild(newRow);
        } else {
            // Insert the new note before the add button in the current row
            const newNote = document.createElement("div");
            newNote.classList.add("note");
            newNote.contentEditable = "true";
            newNote.innerText = "Click here to type...";
            targetRow.insertBefore(newNote, addNoteButton);
        }
    });
});