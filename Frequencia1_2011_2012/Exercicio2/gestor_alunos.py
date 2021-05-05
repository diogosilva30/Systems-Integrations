import os

from gestor_base import GestorBase


class GestorAlunos(GestorBase):
    """
    Classe que faz a gestão dos alunos
    """

    def _listar_alunos(self):
        # Limpar consola
        os.system("cls")
        self.cursor.callproc("listar_alunos")
        for result in self.cursor.stored_results():
            print(result.fetchone())
        input("Pressione alguma tecla para continuar")

    def _adicionar_aluno(self):
        # Limpar consola
        os.system("cls")
        nome = input("Insira o nome do aluno: ")
        endereco = input("Insira o endereço do aluno: ")
        # Não faço ideia do que seja "garantia"...
        garantia = input("Insira a garantia do aluno: ")
        # Executar stored procedure
        self.cursor.callproc("adicionar_aluno", args=[nome, endereco, garantia])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _atualizar_aluno(self):
        # Limpar consola
        os.system("cls")
        numero = input("Qual o número do aluno a atualizar?")

        nome_new = input("Qual o novo nome?")
        endereco_new = input("Qual o novo endereço?")
        garantia_new = input("Qual a nova garantia?")

        # Chamar procedimento
        self.cursor.callproc(
            "atualizar_aluno", args=[numero, nome_new, endereco_new, garantia_new]
        )
        # Commit para guardar alteracoes
        self.connection.commit()

    def _apagar_aluno(self):
        # Limpar consola
        os.system("cls")

        numero = input("Qual o número do aluno a apagar?")

        # Chamar procedimento
        self.cursor.callproc("apagar_aluno", args=[numero])
        # Commit para guardar alteracoes
        self.connection.commit()

    def run(self):

        while True:

            # limpar consola
            os.system("cls")

            # Apresentar menu
            print("Gestão de alunos:")
            print("\t1 - Listar alunos")
            print("\t2 - Adicionar aluno")
            print("\t3 - Atualizar aluno")
            print("\t4 - Apagar aluno")

            print("q - Sair")

            opt = input("Opção: ")

            # Se for 'q' fechar app
            if opt == "q":
                break
            elif opt == "1":
                self._listar_alunos()

            elif opt == "2":
                self._adicionar_aluno()

            elif opt == "3":
                self._atualizar_aluno()

            elif opt == "4":
                self._apagar_aluno()

        # Fechar conexoes
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    """
    Entrypoint do script
    """
    # Instanciamos um gestor de alunos com as credenciais corretas
    # deste serviço e corremos o gestor
    GestorAlunos("gestor_alunos", "password").run()
