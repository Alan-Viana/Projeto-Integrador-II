/**
 * PopInfo — interações globais da interface.
 */
(function () {
    "use strict";

    var botaoTopo = document.getElementById("btn-voltar-topo");

    function atualizarVisibilidadeBotaoTopo() {
        if (!botaoTopo) { return; }
        botaoTopo.classList.toggle("visivel", window.scrollY > 400);
    }

    if (botaoTopo) {
        botaoTopo.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
        window.addEventListener("scroll", atualizarVisibilidadeBotaoTopo);
        atualizarVisibilidadeBotaoTopo();
    }

    document.addEventListener("click", function (event) {
        var link = event.target.closest("a");
        if (!link || link.origin !== window.location.origin) { return; }

        var destino = new URL(link.href);
        if (destino.pathname !== window.location.pathname) { return; }

        var comportamento = window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "auto"
            : "smooth";

        event.preventDefault();
        if (destino.hash) {
            var secao = document.querySelector(destino.hash);
            if (!secao) { return; }

            var menu = document.getElementById("navbarPopInfo");
            var rolarAteSecao = function () {
                secao.scrollIntoView({ behavior: comportamento, block: "start" });
            };

            if (menu && menu.classList.contains("show") && window.bootstrap) {
                menu.addEventListener("hidden.bs.collapse", rolarAteSecao, { once: true });
                window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
            } else {
                rolarAteSecao();
            }
        } else {
            window.scrollTo({ top: 0, behavior: comportamento });
        }
        window.history.pushState(null, "", destino.hash || destino.pathname);
    });
})();
