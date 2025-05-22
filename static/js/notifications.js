const notificationBtn = document.getElementById('notificationBtn');
const notificationDropdown = document.getElementById('notificationDropdown');


notificationBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    notificationDropdown.classList.toggle('hidden');
});


document.addEventListener('click', (event) => {
    const isClickInsideNotificationBtn = notificationBtn.contains(event.target);
    const isClickInsideNotificationDropdown = notificationDropdown.contains(event.target);

    if (!isClickInsideNotificationBtn && !isClickInsideNotificationDropdown) {
        notificationDropdown.classList.add('hidden');
    }
});