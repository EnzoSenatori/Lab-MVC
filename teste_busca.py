from app.models.livro import buscar_livros, listar_unidades_disponiveis, obter_estoque, consultar_estoque_por_unidade, realizar_reserva, gerar_qr_code
from app.models.dados_stub import reservas

def teste_busca_por_titulo():
    resultado = buscar_livros('Harry')
    assert len(resultado) > 0
    encontrou = False
    for livro in resultado:
        if "Harry Potter" in livro["titulo"]:
                encontrou = True
    assert encontrou == True

def teste_busca_por_autor():
    resultado = buscar_livros('Rowling')
    assert len(resultado) > 0
    encontrou = False
    for livro in resultado:
        if "Rowling" in livro["autor"]:
            encontrou = True
    assert encontrou == True

def teste_busca_por_editora():
    resultado = buscar_livros('Rocco')
    assert len(resultado) > 0
    encontrou = False
    for livro in resultado:
        if "Rocco" in livro["editora"]:
            encontrou = True
    assert encontrou == True

def teste_busca_sem_resultados():
    resultado = buscar_livros('livroQueNaoExiste')
    assert len(resultado) == 0

def teste_busca_vazia():
    resultado = buscar_livros("")
    assert resultado == "erro"

def teste_disponibilidade():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    estoque = livro["estoque"]
    for loja, quantidade in estoque.items():
        assert isinstance(quantidade, int)
        assert quantidade >= 0

def teste_quantidade_por_unidade():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    estoque = obter_estoque(livro)
    assert len(estoque) > 0
    for nome_loja, quantidade_disponivel in estoque.items():
        assert isinstance(quantidade_disponivel, int)
        assert quantidade_disponivel >= 0

def teste_filtrar_unidades_disponiveis():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    unidades = listar_unidades_disponiveis(livro)
    for loja in unidades:
        quantidade = livro["estoque"][loja]
        assert quantidade > 0

def teste_unidades_ordenadas_por_estoque():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    unidades = listar_unidades_disponiveis(livro)
    quantidades = []
    for loja in unidades:
        quantidade = livro["estoque"][loja]
        quantidades.append(quantidade)
    for i in range(len(quantidades) - 1):
        assert quantidades[i] >= quantidades[i + 1]

def teste_filtrar_por_unidade():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    unidade_escolhida = 'Loja Centro'
    quantidade = consultar_estoque_por_unidade(livro, unidade_escolhida)
    assert isinstance(quantidade, int)
    assert quantidade > 0

def teste_realizar_reserva():
    resultado = buscar_livros('Harry')
    livro = resultado[0]
    unidade = 'Loja Centro'
    reserva = realizar_reserva(livro, unidade)
    assert reserva['livro_id'] == livro['id']
    assert reserva['unidade'] == unidade
    assert reserva['status'] == 'reservado'

def teste_reserva_em_reservas():
    resultado = buscar_livros('Harry')
    livro = resultado[0]
    unidade = 'Loja Centro'
    reserva = realizar_reserva(livro, unidade)
    assert reserva in reservas

def teste_gerar_qr_code():
    resultado = buscar_livros('Harry')
    livro = resultado[0]
    unidade = 'Loja Centro'
    reserva = realizar_reserva(livro, unidade)
    qr_code = gerar_qr_code(reserva)
    assert isinstance(qr_code, str)
    assert len(qr_code) > 0

def teste_reserva_com_qr_code():
    resultado = buscar_livros('Harry')
    livro = resultado[0]
    unidade = 'Loja Centro'
    usuario = 'Enzo'
    data = '2026-03-29'
    reserva = realizar_reserva(livro, unidade, usuario, data)
    assert reserva in reservas
    assert 'qr_code' in reserva
    assert isinstance(reserva['qr_code'], str)
    assert len(reserva['qr_code']) > 0

