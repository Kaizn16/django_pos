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
const changePasswordBtn = profileDropdown.querySelector('button');
const changePasswordModal = document.getElementById('changePasswordModal');
const cancelChangePasswordBtn = document.getElementById('cancelChangePassword');


profileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    profileDropdown.classList.toggle('hidden');
});


changePasswordBtn.addEventListener('click', () => {
    changePasswordModal.classList.remove('hidden');
    profileDropdown.classList.add('hidden');
});


cancelChangePasswordBtn.addEventListener('click', () => {
    changePasswordModal.classList.add('hidden');
});


changePasswordModal.addEventListener('click', (e) => {
    if (e.target === changePasswordModal) {
        changePasswordModal.classList.add('hidden');
    }
});

document.addEventListener('click', (event) => {
    const isClickInsideSidebar = sidebar.contains(event.target);
    const isClickOnToggleBtn = toggleBtn.contains(event.target);
    const isClickInsideProfileBtn = profileBtn.contains(event.target);
    const isClickInsideProfileDropdown = profileDropdown.contains(event.target);

    if (!isClickInsideSidebar && !isClickOnToggleBtn) {
        closeSidebar();
    }

    if (!isClickInsideProfileBtn && !isClickInsideProfileDropdown) {
        profileDropdown.classList.add('hidden');
    }
});