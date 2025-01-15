document.addEventListener('DOMContentLoaded', function() {
    const sidebar       = document.getElementById('sidebar');
    const overlay       = document.getElementById('overlay');
    const closeSidebar  = document.getElementById('closeSidebar');
  
    // Grab BOTH hamburger buttons
    const hamburgerBtns = [
      document.getElementById('hamburgerBtnDesktop'),
      document.getElementById('hamburgerBtnMobile')
    ];
  
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
  
    // Add the “click” event to each hamburger
    hamburgerBtns.forEach(btn => {
      if (btn) {
        btn.addEventListener('click', openDrawer);
      }
    });
  
    // Close drawer when clicking “×” or the overlay
    closeSidebar.addEventListener('click', closeDrawer);
    overlay.addEventListener('click', closeDrawer);
  });
  