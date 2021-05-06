from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
import datetime

from pymongo import MongoClient
import os


class AlunoHandler(FileSystemEventHandler):
    """
    Classe observer que fica a escuta de alteracoes no ficheiro exportado 'aluno.txt'
    Como o MySQL nao permite nomes dinamicos no ficheiro exportado e não permite dar overwrite
    no ficheiro, sempre que este for lido deve ter o seu nome alterado.
    Após a leitura do ficheiro, os dados são inseridos numa base de dados MongoDB.
    É necessário instalar o connector 'pymongo'

    Vamos fazer de conta que esta base de dados MongoDB é uma versão internacional
    da base dados MySQL. Ou seja o conteúdo estar em inglês.
    """

    def __init__(self, *args, **kwargs):
        # Instanciar conexão à base de dados MongoDB
        self.client = MongoClient(host="localhost", port=27017)
        # Instanciar base de dados
        self.database = self.client["ex2-ETL"]

        # Chamar parent constructor
        super().__init__(*args, **kwargs)

    def on_created(self, event):
        """
        Evento disparado sempre que é criado o ficheiro.
        """
        # Primeiro mudamos o nome do ficheiro para um nome unico (para evitar clashes)
        # Para isso marcamos o ficheiro com um timestamp

        new_name = (
            event.src_path.split("/aluno.txt")[0]
            + f"/aluno_{datetime.datetime.now().timestamp()}.txt"
        )
        # Fazemos entao o rename para um nome unico
        os.rename(event.src_path, new_name)

        # Agora lemos o novo ficheiro
        with open(new_name, "r") as myfile:
            # Lemos a primeira linha e separamos por ','
            data = myfile.read().splitlines()[0].split(",")

        # Agora temos a variavel 'data' que é uma lista com elementos
        # adicionados

        # Criamos entao um novo "documento" do mongo db
        # Aqui também poderiamos fazer algum tipo de transformacao dos dados... (Parte do transform)
        # Neste caso vamos fazer uma "transformacao" simples de guardar os valores com "colunas" (chaves em NoSQL) em ingles

        # Extrair nome e remover aspas
        name = data[1].replace('"', "")
        # Extrair morada e remover aspas
        address = data[2].replace('"', "")
        warranty = int(data[3])

        # preparar documento a inserir
        doc = {"name": name, "address": address, "warranty": warranty}

        # inserir na base de dados Mongo, coluna "Student"
        self.database["Student"].insert_one(doc)


if __name__ == "__main__":
    """
    Entrypoint do script. Coloca o watchdog à escuta de alterações
    https://stackoverflow.com/questions/18599339/watchdog-monitoring-file-for-changes
    """
    # Instanciar handler
    handler = AlunoHandler()

    observer = Observer()

    # Criar um observer da pasta onde é feito o dump dos ficheiros do MySQL
    observer.schedule(
        handler,
        path="C:/tmp/",
        recursive=False,
    )
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
