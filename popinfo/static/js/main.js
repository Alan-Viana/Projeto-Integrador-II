/**
 * PopInfo — script principal do front-end.
 *
 * Responsabilidades:
 *  - Alternar entre tema claro/escuro e persistir a preferência do usuário;
 *  - Exibir/ocultar o botão flutuante de "voltar ao topo" conforme o scroll.
 */
(function () {
    "use strict";

    var STORAGE_KEY = "popinfo-tema";
    var htmlElement = document.documentElement;
    var botaoTema = document.getElementById("btn-tema");

    function obterIconeTema(tema) {
        return tema === "dark" ? "bi-sun" : "bi-moon-stars";
    }

    function aplicarTema(tema) {
        htmlElement.setAttribute("data-bs-theme", tema);
        if (botaoTema) {
            var icone = botaoTema.querySelector("i");
            if (icone) {
                icone.className = "bi " + obterIconeTema(tema);
            }
        }
    }

    function inicializarTema() {
        var temaSalvo = window.localStorage.getItem(STORAGE_KEY);
        var preferenciaSistema = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        aplicarTema(temaSalvo || preferenciaSistema);
    }

    function alternarTema() {
        var temaAtual = htmlElement.getAttribute("data-bs-theme") === "dark" ? "dark" : "light";
        var novoTema = temaAtual === "dark" ? "light" : "dark";
        aplicarTema(novoTema);
        window.localStorage.setItem(STORAGE_KEY, novoTema);
    }

    if (botaoTema) {
        botaoTema.addEventListener("click", alternarTema);
    }

    inicializarTema();

    // ---------------------------------------------------------------------
    // Botão flutuante: voltar ao topo
    // ---------------------------------------------------------------------
    var botaoTopo = document.getElementById("btn-voltar-topo");

    function atualizarVisibilidadeBotaoTopo() {
        if (!botaoTopo) { return; }
        if (window.scrollY > 400) {
            botaoTopo.classList.add("visivel");
        } else {
            botaoTopo.classList.remove("visivel");
        }
    }

    if (botaoTopo) {
        botaoTopo.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
        window.addEventListener("scroll", atualizarVisibilidadeBotaoTopo);
        atualizarVisibilidadeBotaoTopo();
    }
})();
