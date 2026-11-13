# PopInfo — Central de Informações e Apoio ao Cidadão

Projeto Integrador (PI) — UNIVESP

Plataforma Web para divulgação unificada de informações sobre a prestação
de serviços socioassistenciais na cidade de São Paulo, desenvolvida em
parceria com uma ONG local.

> **Etapa atual do desenvolvimento:** estrutura de front-end (Django +
> Bootstrap 5), com a arquitetura em camadas já preparada para receber as
> próximas funcionalidades (persistência completa, API, testes,
> acessibilidade avançada, deploy em nuvem e, opcionalmente, análise de
> dados), conforme o cronograma do Plano de Ação.

---

## 1. Stack utilizada

| Camada                 | Tecnologia                             |
|------------------------|----------------------------------------|
| Framework Web          | Django 5 (Python)                      |
| Front-end              | Bootstrap 5.3 + Bootstrap Icons        |
| Script Web             | JavaScript (tema claro/escuro, scroll) |
| Banco de dados (dev)   | SQLite (via ORM do Django)             |
| Controle de versão     | Git                                    |

---

## 2. Arquitetura do projeto

O projeto segue uma **arquitetura em camadas**, mesmo nesta fase inicial
focada em front-end, para que a evolução do sistema (integração real com
banco de dados, API, testes automatizados etc.) não exija retrabalho:

```
Requisição HTTP
      │
      ▼
Controller (views.py)   → recebe a requisição, delega ao Service e
                          devolve a resposta. Não contém regra de negócio.
      │
      ▼
Service (services.py)   → concentra as regras de negócio da aplicação e
                          converte entidades em ViewModels (DTOs) para
                          os templates.
      │
      ▼
Repository (repositories.py) → única camada que acessa o ORM/banco de
                               dados diretamente.
      │
      ▼
Entity (models.py)      → representa a estrutura persistida no banco.
```

Essa separação está aplicada, por exemplo, no app `servicos/`:

```
servicos/
├── models.py          # Entity  (Categoria, Servico, Acao, Unidade)
├── repositories.py    # Repository (Categoria/Servico/UnidadeRepository)
├── services.py        # Service + ViewModels (Categoria/Servico/UnidadeService)
├── views.py           # Controller (UnidadeListView, UnidadeDetailView)
├── admin.py
├── urls.py
├── migrations/
│   ├── 0001_initial.py
│   └── 0002_dados_iniciais.py   # categorias + catálogo de tipos de serviço
└── templates/servicos/
    ├── lista.html
    └── unidade_detail.html
```

### Modelo de dados

```
Categoria 1 ── N Servico 1 ── N Acao
                     │
                     1 ── N Unidade
```

| Entidade    | O que representa | Exemplo |
|-------------|------------------|---------|
| `Categoria` | Agrupamento exibido na página inicial | Acolhimento |
| `Servico`   | **Tipo** de serviço (Tipificação Nacional do SUAS), com público-alvo, forma de acesso e documentos exigidos | CRAS, CREAS, CTA |
| `Acao`      | O que o tipo de serviço oferece (exibido como etiquetas no card) | Pernoite, Banho, Cadastro Único |
| `Unidade`   | **Local físico** de atendimento: endereço, região, telefone, horário, coordenadas do mapa e origem do dado | CRAS Butantã |

### Organização dos apps Django

- **`core/`** — páginas institucionais: Início (com a seção Categorias na
  mesma página, por rolagem), Sobre e Contato.
- **`servicos/`** — página "Serviços", com filtros e o template de card já
  pronto para receber os dados reais que serão cadastrados no banco de
  dados nas próximas etapas.
- **`accounts/`** — autenticação da "Área Restrita" (login/logout).

### Sobre os dados iniciais

A *migration* de dados `servicos/migrations/0002_dados_iniciais.py` cria
as 6 categorias da página inicial e o catálogo de tipos de serviço
(CRAS, CREAS, Centro POP, CA, NCI, CCA, CAPS, UBS, Bom Prato, Cate)
com suas ações. A migration `0003_importar_unidades.py` carrega as
**1.477 unidades reais** de `servicos/dados/unidades.csv` (fontes: SMADS
dados abertos dez/2025, CNES/Ministério da Saúde, páginas oficiais da
SMADS, Bom Prato e Cate).

> **Atenção (quem já tinha o banco local):** as migrations foram
> recriadas nesta versão. Apague o arquivo `db.sqlite3` e rode
> `python manage.py migrate` novamente.

---

## 3. Como executar o projeto localmente

### Pré-requisitos

- Python 3.11 ou superior instalado.

### Passo a passo

```bash
# 1. Clone o repositório e acesse a pasta do projeto
cd popinfo

# 2. Crie e ative um ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Aplique as migrações (cria o banco SQLite e os dados de exemplo)
python manage.py migrate

# 5. (Opcional) Crie um usuário para testar a Área Restrita.
#    Ao ser solicitado o "username", informe o mesmo valor do e-mail,
#    pois o login foi construído para autenticar por e-mail.
python manage.py createsuperuser

# 6. Rode o servidor de desenvolvimento
python manage.py runserver

```
Acesse **http://127.0.0.1:8000/** no navegador.

| Página              | URL                               |
|---------------------|-----------------------------------|
| Início / Categorias | `/`                               |
| Serviços            | `/servicos/`                      |
| Sobre               | `/sobre/`                         |
| Contato             | `/contato/`                       |
| Área Restrita       | `/conta/login/`                   |
| Admin do Django     | `/admin/`                         |

---

## 4. Execução dos Testes Automatizados
O projeto dispõe de testes unitários e de integração para validação da regra de negócio e integridade das views e models:

```
# Navegue até a pasta onde está o manage.py e execute:
python manage.py test
```

## 5. Próximos incrementos (desenvolvimento diário)

Conforme o Plano de Ação do PI, o projeto será evoluído em pequenos
incrementos. Itens previstos para as próximas etapas:

- [x] Testes automatizados (unitários e de integração);
- [ ] Cadastro completo dos serviços socioassistenciais no banco de dados;
- [ ] Página de detalhe de cada serviço + integração com mapa (API de geolocalização);
- [ ] API REST (Django REST Framework) para consumo dos dados;
- [ ] Autenticação completa da Área Restrita com permissões por perfil;
- [ ] Revisão de acessibilidade (WCAG 2.1: contraste, `aria-label`, navegação por teclado);
- [ ] Deploy em ambiente de nuvem;
- [ ] (Opcional) Painel de análise de dados dos serviços cadastrados.

---

## 6. Convenções de código

- Nomes de classes, métodos e variáveis em português, para manter a
  consistência com o domínio do projeto (assistência social).
- Cada camada tem uma única responsabilidade (princípio da
  responsabilidade única), evitando lógica de negócio em `views.py` e
  consultas ao ORM fora de `repositories.py`.
- Templates HTML organizados por app, com `base.html` e parciais
  (`navbar.html`, `footer.html`) reaproveitados em todas as páginas.
