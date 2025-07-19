let deleteUrl = "";

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