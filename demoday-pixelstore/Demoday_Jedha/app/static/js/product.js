// Sélecteur d'option (stockage) - externalisé pour respecter une CSP stricte
// (script-src 'self', sans 'unsafe-inline').
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".option-pill").forEach(function (pill) {
    pill.addEventListener("click", function () {
      this.closest(".option-pills")
        .querySelectorAll(".option-pill")
        .forEach(function (p) {
          p.classList.remove("active");
        });
      this.classList.add("active");
    });
  });
});
