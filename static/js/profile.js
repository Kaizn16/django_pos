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
    const isClickInsideProfileBtn = profileBtn.contains(event.target);
    const isClickInsideProfileDropdown = profileDropdown.contains(event.target);

    if (!isClickInsideProfileBtn && !isClickInsideProfileDropdown) {
        profileDropdown.classList.add('hidden');
    }
});