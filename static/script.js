let deleteUrl = "";
let sun = document.querySelector(".sun");
let botaoEnviar = document.querySelector(".btn-diario");

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

sun.addEventListener("click", function () {
    if (sun.classList.contains("active")) {
        sun.classList.remove("active");
        document.body.style.backgroundColor = "#60c7c7";
        document.body.style.color = "#000";
        document.body.classList.remove("dark-mode");
        botaoEnviar.style.border = "double 10px #10d1f7";
    } else {
        sun.classList.add("active");
        document.body.style.backgroundColor = "#0a004cff";
        document.body.style.color = "#fff";
        document.body.classList.add("dark-mode");
        botaoEnviar.style.border = "double 10px blue";
    }
});