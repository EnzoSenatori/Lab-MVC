# Lab-MVC | Livraria

MVP de livraria refatorado com arquitetura MVC clássica usando Flask e Jinja2.

## Estrutura

```
main.py                  — ponto de entrada
app/
├── __init__.py          — app factory
├── controllers/
│   └── livros.py        — rotas e lógica de apresentação
├── models/
│   ├── dados.py         — dados mock (livros e reservas)
│   └── livro.py         — regras de negócio
└── views/               — templates Jinja2
    ├── base.html
    ├── index.html
    ├── busca.html
    ├── livro.html
    ├── confirmacao.html
    └── 404.html
static/
└── styles.css
teste_busca.py           — testes de unidade
```

## Como rodar

**1. Instalar dependências**

```bash
pip install -r requirements.txt
```

**2. Iniciar o servidor**

```bash
python main.py
```

Acesse em: http://127.0.0.1:5000

**3. Rodar os testes**

```bash
pytest teste_busca.py -v
```

## Funcionalidades

- Busca de livros por título, autor ou editora
- Listagem de unidades com estoque disponível
- Reserva de livro em uma unidade específica com geração de QR code
