from abc import ABC, abstractmethod
import mysql.connector


class GestorBase(ABC):
    """
    Classe abstrata base que os gestores concretos devem
    implementar
    """

    def __init__(self, user, password):
        """
        Construtor Base de todos os gestores.
        É instanciada uma conexão à base de dados MySQL com as credenciais fornecidas.
        """
        # Instanciar conexao à base de dados
        self.connection = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="ex2",
        )
        self.cursor = self.connection.cursor()

    @abstractmethod
    def run(self):
        """
        Método abstracto para iniciar o gestor.
        """
