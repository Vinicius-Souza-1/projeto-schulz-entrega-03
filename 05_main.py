import sqlite3
from decimal import Decimal
from importlib import import_module


# Importa as classes do arquivo cujo nome começa com números.
classes = import_module("04_classes")

Tecnico = classes.Tecnico
Equipamento = classes.Equipamento
Medicao = classes.Medicao
BancoDados = classes.BancoDados


def preparar_exemplos(banco):
    tecnico = Tecnico(
        matricula="TEC001",
        nome="Ana Souza",
        email="ana@example.com",
        setor="Metrologia"
    )

    equipamento = Equipamento(
        codigo_tag="EQ001",
        descricao="Paquímetro digital",
        fabricante="Fabricante de teste",
        modelo="Modelo A"
    )

    registro_tecnico = banco.buscar_tecnico_por_matricula(
        tecnico.matricula
    )

    if registro_tecnico is None:
        banco.cadastrar_tecnico(tecnico)
        print("Técnico de exemplo cadastrado.")
    else:
        print("Técnico de exemplo já cadastrado.")

    registro_equipamento = banco.buscar_equipamento_por_codigo(
        equipamento.codigo_tag
    )

    if registro_equipamento is None:
        banco.cadastrar_equipamento(equipamento)
        print("Equipamento de exemplo cadastrado.")
    else:
        print("Equipamento de exemplo já cadastrado.")

    registro_tecnico = banco.buscar_tecnico_por_matricula(
        tecnico.matricula
    )
    registro_equipamento = banco.buscar_equipamento_por_codigo(
        equipamento.codigo_tag
    )

    id_tecnico = registro_tecnico["id_tecnico"]
    id_equipamento = registro_equipamento["id_equipamento"]

    # Preenche as medições iniciais somente se não houver medições.
    if not banco.listar_medicoes():
        for valor in ("10.05", "10.20"):
            medicao = Medicao(
                parametro_medido="Comprimento (mm)",
                valor_nominal="10.00",
                tolerancia_min="0.10",
                tolerancia_max="0.10",
                valor_obtido=valor
            )

            banco.cadastrar_medicao(
                medicao,
                id_tecnico,
                id_equipamento
            )

        print("Duas medições de exemplo cadastradas.")
    else:
        print("Medições existentes preservadas.")

    return id_tecnico, id_equipamento


def demonstrar_crud(banco, id_tecnico, id_equipamento):
    print("\n--- DEMONSTRAÇÃO DO CRUD DE MEDIÇÕES ---")

    medicao_teste = Medicao(
        parametro_medido="Teste de CRUD (mm)",
        valor_nominal="10.00",
        tolerancia_min="0.10",
        tolerancia_max="0.10",
        valor_obtido="10.05"
    )

    id_teste = banco.cadastrar_medicao(
        medicao_teste,
        id_tecnico,
        id_equipamento
    )
    print(f"CREATE: medição de teste criada com ID {id_teste}.")

    try:
        registro = banco.buscar_medicao_por_id(id_teste)

        if registro is None:
            raise RuntimeError("A medição criada não foi encontrada.")

        print(f"READ: resultado inicial = {registro['status_resultado']}.")

        medicao_corrigida = Medicao(
            parametro_medido="Teste de CRUD (mm)",
            valor_nominal="10.00",
            tolerancia_min="0.10",
            tolerancia_max="0.10",
            valor_obtido="10.20"
        )

        alteradas = banco.atualizar_medicao(
            id_teste,
            medicao_corrigida
        )

        registro = banco.buscar_medicao_por_id(id_teste)

        if alteradas != 1 or registro is None:
            raise RuntimeError("Não foi possível confirmar a atualização.")

        print(
            f"UPDATE: {alteradas} registro alterado. "
            f"Resultado = {registro['status_resultado']}."
        )

    finally:
        # Remove somente a medição temporária criada neste teste.
        excluidas = banco.excluir_medicao(id_teste)
        print(f"DELETE: {excluidas} registro excluído.")

    ainda_existe = banco.buscar_medicao_por_id(id_teste) is not None
    print(f"Medição de teste ainda existe? {ainda_existe}")

    if ainda_existe:
        raise RuntimeError("A exclusão da medição não foi confirmada.")


def mostrar_relatorio(banco):
    medicoes = banco.listar_medicoes()

    print("\n" + "=" * 55)
    print("RELATÓRIO DE MEDIÇÕES — SCHULZ")
    print("=" * 55)

    if not medicoes:
        print("Nenhuma medição cadastrada.")
        return

    aprovadas = 0
    reprovadas = 0

    for medicao in medicoes:
        nominal = Decimal(str(medicao["valor_nominal"]))
        tolerancia_min = Decimal(str(medicao["tolerancia_min"]))
        tolerancia_max = Decimal(str(medicao["tolerancia_max"]))

        limite_minimo = nominal - tolerancia_min
        limite_maximo = nominal + tolerancia_max

        print(f"\nMedição: {medicao['id_medicao']}")
        print(f"Data registrada no banco (UTC): {medicao['data_medicao']}")
        print(
            f"Técnico: {medicao['nome_tecnico']} "
            f"| Matrícula: {medicao['matricula']}"
        )
        print(
            f"Equipamento: {medicao['nome_equipamento']} "
            f"| Código: {medicao['codigo_tag']}"
        )
        print(f"Parâmetro: {medicao['parametro_medido']}")
        print(f"Valor nominal: {nominal:.2f}")
        print(f"Limites: {limite_minimo:.2f} até {limite_maximo:.2f}")
        print(f"Valor obtido: {medicao['valor_obtido']:.2f}")
        print(f"Resultado: {medicao['status_resultado']}")
        print("-" * 55)

        if medicao["status_resultado"] == "APROVADO":
            aprovadas += 1
        elif medicao["status_resultado"] == "REPROVADO":
            reprovadas += 1

    print(f"\nTotal de medições: {len(medicoes)}")
    print(f"Aprovadas: {aprovadas}")
    print(f"Reprovadas: {reprovadas}")


def main():
    try:
        banco = BancoDados()
        banco.criar_tabelas()

        print("Banco de dados e tabelas preparados com sucesso.")

        id_tecnico, id_equipamento = preparar_exemplos(banco)

        demonstrar_crud(
            banco,
            id_tecnico,
            id_equipamento
        )

        mostrar_relatorio(banco)

    except ValueError as erro:
        print(f"Dados inválidos: {erro}")
    except sqlite3.IntegrityError as erro:
        print(f"Operação não permitida pelas regras do banco: {erro}")
    except (sqlite3.Error, OSError) as erro:
        print(f"Não foi possível concluir a operação: {erro}")
    except RuntimeError as erro:
        print(f"Falha na verificação: {erro}")


if __name__ == "__main__":
    main()

    