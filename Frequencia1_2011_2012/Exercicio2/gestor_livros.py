import os
from gestor_base import GestorBase


class GestorLivros(GestorBase):
    """
    Classe que faz a gestão dos livros
    """

    def _listar_livros(self):
        # Limpar consola
        os.system("cls")
        self.cursor.callproc("listar_livros")
        for result in self.cursor.stored_results():
            print(result.fetchone())

        input("Pressione alguma tecla para continuar")

    def _adicionar_livro(self):
        # Limpar consola
        os.system("cls")

        titulo = input("Insira o titulo do livro: ")
        autor = input("Insira o autor do livro: ")
        editor = input("Insira o editor do livro: ")

        # Chamar procedimento
        self.cursor.callproc("adicionar_livro", args=[titulo, autor, editor])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _atualizar_livro(self):
        # limpar consola
        os.system("cls")

        numero = input("Qual o número do livro a atualizar?")

        titulo_new = input("Qual o novo titulo?")
        autor_new = input("Qual o novo autor?")
        editor_new = input("Qual o novo editor?")

        # Chamar procedimento
        self.cursor.callproc(
            "atualizar_livro", args=[numero, titulo_new, autor_new, editor_new]
        )
        # Commit para guardar alteracoes
        self.connection.commit()

    def _apagar_livro(self):
        # Limpar consola
        os.system("cls")

        numero = input("Qual o número do livro a apagar?")

        # Chamar procedimento
        self.cursor.callproc("apagar_livro", args=[numero])
        # Commit para guardar alteracoes
        self.connection.commit()

    def run(self):

        while True:

            # limpar consola
            os.system("cls")

            # Apresentar menu
            print("Gestor de livros:")
            print("\t1 - Listar livros")
            print("\t2 - Adicionar livro")
            print("\t3 - Atualizar livro")
            print("\t4 - Apagar livro")

            print("q - Sair")

            opt = input("Opção: ")

            # Se for 'q' fechar app
            if opt == "q":
                break
            elif opt == "1":
                self._listar_livros()

            elif opt == "2":
                self._adicionar_livro()

            elif opt == "3":
                self._atualizar_livro()

            elif opt == "4":
                self._apagar_livro()

        # Fechar conexoes
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    """
    Entrypoint do script
    """
    # Instanciamos um gestor de livros com as credenciais corretas
    # deste serviço e corremos o gestor
    GestorLivros("gestor_livros", "password").run()
