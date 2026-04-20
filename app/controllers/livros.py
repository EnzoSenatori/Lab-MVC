from flask import Blueprint, request, render_template, redirect, url_for

from app.models.dados import livros
from app.models.livro import (
    buscar_livros,
    listar_unidades_disponiveis,
    obter_estoque,
    realizar_reserva,
)

livros_bp = Blueprint('livros', __name__)


def serializar_livro(livro: dict) -> dict:
    estoque = obter_estoque(livro)
    total_estoque = sum(estoque.values())
    unidades_disponiveis = listar_unidades_disponiveis(livro)

    if total_estoque == 0:
        badge = "Indisponível"
    elif total_estoque <= 2:
        badge = "Estoque limitado"
    else:
        badge = "Em estoque"

    return {
        "id": livro["id"],
        "titulo": livro["titulo"],
        "autor": livro["autor"],
        "editora": livro["editora"],
        "total_estoque": total_estoque,
        "badge": badge,
        "unidades_disponiveis": unidades_disponiveis,
    }


@livros_bp.get("/")
def index():
    return render_template("index.html")


@livros_bp.get("/busca")
def busca():
    termo = request.args.get("termo", "").strip()
    if not termo:
        return redirect(url_for("livros.index"))

    resultados = buscar_livros(termo)
    if resultados == "erro":
        return redirect(url_for("livros.index"))

    livros_serializados = []
    for livro in resultados:
        livros_serializados.append(serializar_livro(livro))

    return render_template("busca.html", termo=termo, livros=livros_serializados)


@livros_bp.get("/livros/<int:livro_id>")
def detalhe(livro_id: int):
    livro = None
    for item in livros:
        if item["id"] == livro_id:
            livro = item
            break

    if livro is None:
        return render_template("404.html"), 404

    estoque = obter_estoque(livro)
    unidades = []
    for loja, quantidade in sorted(estoque.items(), key=lambda item: item[1], reverse=True):
        if quantidade > 0:
            unidades.append({"nome": loja, "quantidade": quantidade})

    return render_template("livro.html", livro=serializar_livro(livro), unidades=unidades)


@livros_bp.post("/reservas")
def reservar():
    livro_id_str = request.form.get("livro_id", "").strip()
    unidade = request.form.get("unidade", "").strip()
    usuario = request.form.get("usuario", "").strip() or None
    data = request.form.get("data", "").strip() or None

    if not livro_id_str or not unidade:
        return redirect(url_for("livros.index"))

    try:
        livro_id = int(livro_id_str)
    except ValueError:
        return redirect(url_for("livros.index"))

    livro = None
    for item in livros:
        if item["id"] == livro_id:
            livro = item
            break

    if livro is None:
        return redirect(url_for("livros.index"))

    estoque = obter_estoque(livro)
    if estoque.get(unidade, 0) <= 0:
        return redirect(url_for("livros.detalhe", livro_id=livro_id))

    reserva = realizar_reserva(livro, unidade, usuario=usuario, data=data)

    return render_template("confirmacao.html", reserva=reserva, livro=livro, unidade=unidade)
