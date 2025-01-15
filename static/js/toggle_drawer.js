document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const closeSidebar = document.getElementById('closeSidebar');
    const mainMenu = document.getElementById('mainMenu');
    const verticalMenu = document.getElementById('verticalMenu');

    // Function to open the drawer
    function openDrawer() {
        sidebar.classList.add('open');
        overlay.classList.add('show');
    }

    // Function to close the drawer
    function closeDrawer() {
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
    }

    // Add functionality to update the vertical menu dynamically
    mainMenu.addEventListener('click', function (event) {
        const category = event.target.getAttribute('data-category');
        if (category) {
            // Clear existing vertical menu items
            verticalMenu.innerHTML = '';

            // Populate vertical menu with new items
            if (submenuData[category]) {
                submenuData[category].forEach((item) => {
                    verticalMenu.innerHTML += item;
                });
            }

            // Update active state for horizontal menu
            document.querySelectorAll('#mainMenu .nav-link').forEach((link) => {
                link.classList.remove('active');
            });
            event.target.classList.add('active');
        }
    });

    // Event listeners for opening and closing the drawer
    const hamburgerBtns = [
        document.getElementById('hamburgerBtnDesktop'),
        document.getElementById('hamburgerBtnMobile'),
    ];

    hamburgerBtns.forEach((btn) => {
        if (btn) {
            btn.addEventListener('click', openDrawer);
        }
    });

    closeSidebar.addEventListener('click', closeDrawer);
    overlay.addEventListener('click', closeDrawer);
});
