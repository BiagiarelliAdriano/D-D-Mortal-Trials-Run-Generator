document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".wild-surge-toggle").forEach(button => {
        button.addEventListener("click", () => {
            const content = button.nextElementSibling;
            const expanded = button.getAttribute("aria-expanded") === "true";

            button.setAttribute("aria-expanded", !expanded);
            content.classList.toggle("hidden");
        });
    });
});