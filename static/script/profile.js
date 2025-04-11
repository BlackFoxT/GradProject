const toggleSidebarButton = document.getElementById("toggle-sidebar");
const sidebar = document.getElementById("sidebar");

  if (sidebar) {
    sidebar.classList.add("show");
    if (toggleSidebarButton && sidebar) {
      toggleSidebarButton.addEventListener("click", function () {
        sidebar.classList.toggle("show");
      });
    }
  }