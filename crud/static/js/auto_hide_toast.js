setTimeout(() => {
    const successToastMessage = document.getElementById('toast-success');
    if (successToastMessage) {
        successToastMessage.style.transition = 'opacity 0.5s';
        successToastMessage.style.opacity = '0';
        setTimeout(() => {
            successToastMessage.style.display = 'none';
        }, 500);
    }
}, 3000);