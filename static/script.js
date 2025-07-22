let deleteUrl = "";
let sun = document.querySelector(".sun");
let botao = document.querySelectorAll("button");
let botaoEnviar = document.querySelector(".btn-diario");
let sunToMoon = document.querySelector(".sun");

window.addEventListener("DOMContentLoaded", () => {
  const modoSalvo = localStorage.getItem("modo");

    if (modoSalvo === "dark") {
        document.body.classList.add("dark-mode");
        sun.classList.add("active");
        sun.src = "../static/img/moon.png"
        botoes.forEach((btn) => {
            btn.style.border = "double 10px blue";
        });
    } else {
        sun.src = "../static/img/new_sun.png";
    }
}
);

function openModal(texto) {
    document.getElementById("modal-texto").innerText = texto;
    document.getElementById("modal").style.display = "inline-flex";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

function askDelete(url) {
    deleteUrl = url;
    document.getElementById("confirmModal").style.display = "inline-flex";
}

function closeConfirmModal() {
    document.getElementById("confirmModal").style.display = "none";
    deleteUrl = "";
}

document.getElementById("confirmDelete").addEventListener("click", function () {
    window.location.href = deleteUrl;
});

sunToMoon.addEventListener("click", function () {
    if (sunToMoon.src.includes("new_sun.png")) {
        sunToMoon.src = "../static/img/moon.png";
    } else {
        sunToMoon.src = "../static/img/new_sun.png";
    }
});

sun.addEventListener("click", function () {
    if (sun.classList.contains("active")) {
        sun.classList.remove("active");
        document.body.classList.remove("dark-mode");
        localStorage.setItem("modo", "light");
    } else {
        sun.classList.add("active");
        document.body.classList.add("dark-mode");
        localStorage.setItem("modo", "dark");
    }
});