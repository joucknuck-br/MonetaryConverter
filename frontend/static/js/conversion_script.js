function updateCurrencies() {
    document.querySelector(".loading-indicator").classList.add("is-active");

    fetch("http://127.0.0.1:8000/api/update-rates")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao atualizar cotações.");
            }

            return response.json();
        })
        .then(data => {
            document.querySelector(".loading-indicator").classList.remove("is-active");
            alert("Cotações atualizadas com sucesso!");
        })
        .catch(error => {
            document.querySelector(".loading-indicator").classList.remove("is-active");
            alert(error.message);
        });
}