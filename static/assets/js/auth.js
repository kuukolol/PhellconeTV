console.log("auth.js loaded!");
document.addEventListener("DOMContentLoaded", () => {
    const flags = document.getElementById("flags");

    if (!flags) return;

    if (flags.dataset.registered === "true") {
        Swal.fire({
            title: "Registration Successful!",
            text: "Your account has been created. Click OK to login.",
            icon: "success",
            confirmButtonText: "OK"
        }).then(() => {
            window.location.href = "/login";
        });
    }

    if (flags.dataset.error === "true") {
        const msg = flags.dataset.message || "Something went wrong.";
        Swal.fire({
            title: "Registration Failed",
            text: msg,
            icon: "error",
            confirmButtonText: "OK"
        });
    }
});
