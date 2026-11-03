import sqlite3
from pathlib import Path
from decimal import Decimal, InvalidOperation


class Tecnico:
    def __init__(self, matricula, nome, email, setor):
        self._matricula = self._validar_texto(matricula, "Matrícula")
        self._nome = self._validar_texto(nome, "Nome")
        self._email = self._validar_texto(email, "E-mail")
        self._setor = self._validar_texto(setor, "Setor")

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} deve ser um texto preenchido.")
        return valor.strip()

    @property
    def matricula(self):
        return self._matricula

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @property
    def setor(self):
        return self._setor

    def apresentar(self):
        return f"Técnico: {self.nome} | Matrícula: {self.matricula}"


class Equipamento:
    def __init__(self, codigo_tag, descricao, fabricante, modelo):
        self._codigo_tag = self._validar_texto(codigo_tag, "Código")
        self._descricao = self._validar_texto(descricao, "Descrição")
        self._fabricante = self._validar_texto(fabricante, "Fabricante")
        self._modelo = self._validar_texto(modelo, "Modelo")

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} deve ser um texto preenchido.")
        return valor.strip()

    @property
    def codigo_tag(self):
        return self._codigo_tag

    @property
    def descricao(self):
        return self._descricao

    @property
    def fabricante(self):
        return self._fabricante

    @property
    def modelo(self):
        return self._modelo

    def apresentar(self):
        return (
            f"Equipamento: {self.descricao} | "
            f"Código: {self.codigo_tag}"
        )


class Medicao:
    def __init__(
        self,
        parametro_medido,
        valor_nominal,
        tolerancia_min,
        tolerancia_max,
        valor_obtido
    ):
        if (
            not isinstance(parametro_medido, str)
            or not parametro_medido.strip()
        ):
            raise ValueError("O parâmetro medido deve ser preenchido.")

        self._parametro_medido = parametro_medido.strip()
        self._valor_nominal = self._validar_numero(valor_nominal)
        self._tolerancia_min = abs(self._validar_numero(tolerancia_min))
        self._tolerancia_max = abs(self._validar_numero(tolerancia_max))
        self._valor_obtido = self._validar_numero(valor_obtido)

    @staticmethod
    def _validar_numero(valor):
        try:
            numero = Decimal(str(valor))
        except (InvalidOperation, ValueError):
            raise ValueError(
                "Informe um número válido, usando ponto decimal."
            )

        if not numero.is_finite():
            raise ValueError("O número deve ser finito.")

        return numero

    @property
    def parametro_medido(self):
        return self._parametro_medido

    @property
    def valor_nominal(self):
        return self._valor_nominal

    @property
    def tolerancia_min(self):
        return self._tolerancia_min

    @property
    def tolerancia_max(self):
        return self._tolerancia_max

    @property
    def valor_obtido(self):
        return self._valor_obtido

    @property
    def limite_minimo(self):
        return self.valor_nominal - self.tolerancia_min

    @property
    def limite_maximo(self):
        return self.valor_nominal + self.tolerancia_max

    def avaliar(self):
        if self.limite_minimo <= self.valor_obtido <= self.limite_maximo:
            return "APROVADO"
        return "REPROVADO"

    def apresentar(self):
        return (
            f"Parâmetro: {self.parametro_medido}\n"
            f"Limites: {self.limite_minimo} até {self.limite_maximo}\n"
            f"Valor obtido: {self.valor_obtido}\n"
            f"Resultado: {self.avaliar()}"
        )


class BancoDados:
    def __init__(self):
        pasta = Path(__file__).resolve().parent
        self._caminho_banco = pasta / "schulz_mvp.db"
        self._caminho_sql = pasta / "03_banco.sql"

    def conectar(self):
        conexao = sqlite3.connect(self._caminho_banco)
        conexao.execute("PRAGMA foreign_keys = ON;")
        conexao.row_factory = sqlite3.Row
        return conexao

    def criar_tabelas(self):
        script = self._caminho_sql.read_text(encoding="utf-8-sig")
        conexao = self.conectar()

        try:
            conexao.executescript(script)
            conexao.commit()
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def cadastrar_tecnico(self, tecnico):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                """
                INSERT INTO tecnico (
                    nome_tecnico, matricula, email, setor
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    tecnico.nome,
                    tecnico.matricula,
                    tecnico.email,
                    tecnico.setor
                )
            )
            conexao.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def buscar_tecnico_por_matricula(self, matricula):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                """
                SELECT id_tecnico, nome_tecnico, matricula, email, setor
                FROM tecnico
                WHERE matricula = ?
                """,
                (matricula,)
            )
            return cursor.fetchone()
        finally:
            conexao.close()

    def cadastrar_equipamento(self, equipamento):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                """
                INSERT INTO equipamento (
                    codigo_tag, nome_equipamento, fabricante, modelo
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    equipamento.codigo_tag,
                    equipamento.descricao,
                    equipamento.fabricante,
                    equipamento.modelo
                )
            )
            conexao.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def buscar_equipamento_por_codigo(self, codigo_tag):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                """
                SELECT id_equipamento, codigo_tag, nome_equipamento,
                       fabricante, modelo
                FROM equipamento
                WHERE codigo_tag = ?
                """,
                (codigo_tag,)
            )
            return cursor.fetchone()
        finally:
            conexao.close()

    def cadastrar_medicao(self, medicao, id_tecnico, id_equipamento):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                """
                INSERT INTO medicao (
                    id_equipamento,
                    id_tecnico,
                    parametro_medido,
                    valor_nominal,
                    tolerancia_min,
                    tolerancia_max,
                    valor_obtido,
                    status_resultado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_equipamento,
                    id_tecnico,
                    medicao.parametro_medido,
                    str(medicao.valor_nominal),
                    str(medicao.tolerancia_min),
                    str(medicao.tolerancia_max),
                    str(medicao.valor_obtido),
                    medicao.avaliar()
                )
            )
            conexao.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def buscar_medicao_por_id(self, id_medicao):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                "SELECT * FROM medicao WHERE id_medicao = ?",
                (id_medicao,)
            )
            return cursor.fetchone()
        finally:
            conexao.close()

    def listar_medicoes(self):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                """
                SELECT
                    m.id_medicao,
                    m.parametro_medido,
                    m.valor_nominal,
                    m.tolerancia_min,
                    m.tolerancia_max,
                    m.valor_obtido,
                    m.status_resultado,
                    m.data_medicao,
                    t.nome_tecnico,
                    t.matricula,
                    e.codigo_tag,
                    e.nome_equipamento
                FROM medicao AS m
                JOIN tecnico AS t
                    ON m.id_tecnico = t.id_tecnico
                JOIN equipamento AS e
                    ON m.id_equipamento = e.id_equipamento
                ORDER BY m.id_medicao
                """
            )
            return cursor.fetchall()
        finally:
            conexao.close()

    def atualizar_medicao(self, id_medicao, medicao):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                """
                UPDATE medicao
                SET parametro_medido = ?,
                    valor_nominal = ?,
                    tolerancia_min = ?,
                    tolerancia_max = ?,
                    valor_obtido = ?,
                    status_resultado = ?
                WHERE id_medicao = ?
                """,
                (
                    medicao.parametro_medido,
                    str(medicao.valor_nominal),
                    str(medicao.tolerancia_min),
                    str(medicao.tolerancia_max),
                    str(medicao.valor_obtido),
                    medicao.avaliar(),
                    id_medicao
                )
            )
            conexao.commit()
            return cursor.rowcount
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def excluir_medicao(self, id_medicao):
        conexao = self.conectar()

        try:
            cursor = conexao.execute(
                "DELETE FROM medicao WHERE id_medicao = ?",
                (id_medicao,)
            )
            conexao.commit()
            return cursor.rowcount
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

            