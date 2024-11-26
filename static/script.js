document.getElementById("toggle-sidebar").addEventListener("click", function () {
    var sidebar = document.getElementById("sidebar");

    // Burada giriş yapınca sol üstteki ilk ikonu basınca sidebarı açma kapamayı denedim console çalışıyor ama gerisi yok
    if (sidebar.classList.contains("d-none")) {
        console.log(1);
        sidebar.classList.remove("d-none");
    } else {
        console.log(2);
        sidebar.classList.add("d-none");
    }
});
