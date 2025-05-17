const sidebar = document.getElementById('mobileSidebar');
const toggleBtn = document.getElementById('sidebarToggle');
const closeBtn = document.getElementById('closeSidebar');

function openSidebar() {
    sidebar.classList.remove('-translate-x-full');
    toggleBtn.classList.add('hidden');
}

function closeSidebar() {
    sidebar.classList.add('-translate-x-full');
    toggleBtn.classList.remove('hidden');
}

toggleBtn.addEventListener('click', openSidebar);
closeBtn.addEventListener('click', closeSidebar);

const profileBtn = document.getElementById('profileBtn');
const profileDropdown = document.getElementById('profileDropdown');

profileBtn.addEventListener('click', () => {
    profileDropdown.classList.toggle('hidden');
});

document.addEventListener('click', (event) => {
    const isClickInsideSidebar = sidebar.contains(event.target);
    const isClickOnToggleBtn = toggleBtn.contains(event.target);

    if (!isClickInsideSidebar && !isClickOnToggleBtn) {
        closeSidebar();
    }
});