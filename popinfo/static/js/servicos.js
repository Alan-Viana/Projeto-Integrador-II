/**
 * PopInfo — busca e filtros da página de Serviços consumindo a API REST
 * (/api/unidades/), sem recarregar a página.
 *
 * Sem JavaScript a página continua funcionando: o formulário e os links
 * de filtro/paginação fazem a requisição normal ao servidor.
 */
(function () {
    "use strict";

    var form = document.getElementById("form-busca");
    var lista = document.getElementById("lista-unidades");
    if (!form || !lista || !window.fetch) { return; }

    var apiUrl = form.dataset.apiUrl;
    var contador = document.getElementById("contador-resultados");
    var paginacao = document.getElementById("paginacao");
    var btnMais = document.getElementById("btn-carregar-mais");
    var campoTipo = form.elements.tipo;
    var campoBusca = form.elements.q;
    var paginaAtual = Number(btnMais.dataset.pagina);
    var totalPaginas = Number(btnMais.dataset.paginas);
    var temporizador = null;

    // Com JS ativo, troca a paginação por "Carregar mais"
    if (paginacao) { paginacao.classList.add("d-none"); }
    atualizarBotaoMais();

    function parametros(pagina) {
        var dados = new URLSearchParams(new FormData(form));
        dados.set("pagina", pagina);
        // Remove parâmetros vazios para deixar a URL limpa
        Array.from(dados.keys()).forEach(function (chave) {
            if (!dados.get(chave) || dados.get(chave) === "todos") { dados.delete(chave); }
        });
        return dados;
    }

    function elemento(tag, classe, texto) {
        var el = document.createElement(tag);
        if (classe) { el.className = classe; }
        if (texto !== undefined) { el.textContent = texto; }
        return el;
    }

    function linhaInfo(icone, conteudo) {
        var div = elemento("div", "servico-info");
        var i = elemento("i", "bi " + icone);
        i.setAttribute("aria-hidden", "true");
        div.appendChild(i);
        div.appendChild(conteudo);
        return div;
    }

    function resumir(texto, palavras) {
        var partes = (texto || "").split(/\s+/);
        return partes.length > palavras ? partes.slice(0, palavras).join(" ") + " …" : texto;
    }

    function criarCard(u) {
        var col = elemento("div", "col-lg-6");
        var link = elemento("a", "text-decoration-none card-link-wrapper");
        link.href = u.url;
        var card = elemento("article", "servico-card");

        card.appendChild(elemento("span", "badge-tipo", u.sigla));
        card.appendChild(elemento("h3", "servico-nome", u.nome));
        card.appendChild(elemento("p", "servico-descricao", resumir(u.descricao, 30)));

        var endereco = elemento("div");
        endereco.appendChild(elemento("div", "servico-endereco", u.endereco));
        endereco.appendChild(elemento("div", "servico-bairro", u.bairro_cidade));
        card.appendChild(linhaInfo("bi-geo-alt", endereco));
        card.appendChild(linhaInfo("bi-clock", elemento("div", "", u.horario_funcionamento || "Consulte a unidade")));
        card.appendChild(linhaInfo("bi-telephone", elemento("div", "", u.telefone || "Não informado")));

        if (u.acoes && u.acoes.length) {
            var tags = elemento("div", "servico-tags");
            u.acoes.forEach(function (acao) { tags.appendChild(elemento("span", "tag-pill", acao)); });
            card.appendChild(tags);
        }
        link.appendChild(card);
        col.appendChild(link);
        return col;
    }

    function mensagemVazia() {
        var col = elemento("div", "col-12");
        var caixa = elemento("div", "servicos-vazio text-center");
        var i = elemento("i", "bi bi-inbox");
        i.setAttribute("aria-hidden", "true");
        caixa.appendChild(i);
        caixa.appendChild(elemento("p", "", "Nenhum serviço encontrado para os filtros selecionados."));
        col.appendChild(caixa);
        return col;
    }

    function atualizarBotaoMais() {
        btnMais.classList.toggle("d-none", paginaAtual >= totalPaginas);
    }

    function buscar(pagina, acrescentar) {
        var params = parametros(pagina);
        lista.setAttribute("aria-busy", "true");
        btnMais.disabled = true;

        return fetch(apiUrl + "?" + params.toString(), { headers: { "Accept": "application/json" } })
            .then(function (resposta) {
                if (!resposta.ok) { throw new Error("HTTP " + resposta.status); }
                return resposta.json();
            })
            .then(function (dados) {
                if (!acrescentar) { lista.replaceChildren(); }
                dados.resultados.forEach(function (u) { lista.appendChild(criarCard(u)); });
                if (!dados.total) { lista.appendChild(mensagemVazia()); }

                paginaAtual = dados.pagina;
                totalPaginas = dados.paginas;
                contador.textContent = dados.total + (dados.total === 1 ? " unidade encontrada" : " unidades encontradas");
                atualizarBotaoMais();

                // Mantém a URL compartilhável (sem o número da página)
                params.delete("pagina");
                var query = params.toString();
                window.history.replaceState(null, "", window.location.pathname + (query ? "?" + query : ""));
            })
            .catch(function () {
                // Em caso de falha da API, recorre ao envio tradicional do formulário
                form.submit();
            })
            .finally(function () {
                lista.removeAttribute("aria-busy");
                btnMais.disabled = false;
            });
    }

    form.addEventListener("submit", function (evento) {
        evento.preventDefault();
        buscar(1, false);
    });

    if (form.elements.regiao) {
        form.elements.regiao.addEventListener("change", function () { buscar(1, false); });
    }

    // Busca enquanto digita (aguarda o usuário parar por 400 ms)
    campoBusca.addEventListener("input", function () {
        clearTimeout(temporizador);
        temporizador = setTimeout(function () { buscar(1, false); }, 400);
    });

    form.querySelectorAll(".chip[data-tipo]").forEach(function (chip) {
        chip.addEventListener("click", function (evento) {
            evento.preventDefault();
            form.querySelectorAll(".chip").forEach(function (c) {
                c.classList.remove("chip-active");
                c.removeAttribute("aria-current");
            });
            chip.classList.add("chip-active");
            chip.setAttribute("aria-current", "true");
            campoTipo.value = chip.dataset.tipo;
            form.elements.categoria.value = "";  // filtro de tipo substitui o de categoria
            buscar(1, false);
        });
    });

    btnMais.addEventListener("click", function () { buscar(paginaAtual + 1, true); });
})();
