document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach((alert) => {
        setTimeout(() => {
            const btn = alert.querySelector(".btn-close");
            if (btn) btn.click();
        }, 5000);
    });
});
