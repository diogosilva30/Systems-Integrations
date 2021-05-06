"""
Modulo ETL que coloca um observer à escuta de alterações de ficheiros
numa determinada diretoria. Sempre que um novo ficheiro '.csv' é criado
nesta diretoria, este é lido e os dados são atualizados numa base de dados NoSQL (MongoDB)

Bibliotecas externas necessárias à execução:
    - pandas: `pip install pandas`. Necessário para ler e fazer parsing de ficheiros '.csv'.
    - watchdog: `pip install watchdog`. Necessário para notificar de alterações numa determinada diretoria.
    - pymongo: `pip install pymongo`. Driver necessário para a conexão do programa com a base de dados MongoDB.

Suposições para o funcionamento:
    - Pré-Criação de uma base de dados em MongoDB chamada "ex2-ETL"
    - Pré-Criação de uma "Collection" (dentro da base de dados "ex2-ETL") chamada de "Aluno".
"""
import os
import time
import datetime

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import pandas as pd

from pymongo import MongoClient


class AlunoHandler(FileSystemEventHandler):
    """
    Classe observer que fica a escuta de alteracoes no ficheiro exportado 'aluno.csv'
    Como o MySQL nao permite nomes dinamicos no ficheiro exportado e não permite dar overwrite
    no ficheiro, sempre que este for lido deve ter o seu nome alterado.
    Após a leitura do ficheiro, os dados são inseridos numa base de dados MongoDB.
    """

    def __init__(self, *args, **kwargs):
        # Instanciar conexão à base de dados MongoDB
        self.client = MongoClient(host="localhost", port=27017)
        # Instanciar base de dados
        self.database = self.client["ex2-ETL"]

        # Chamar parent constructor
        super().__init__(*args, **kwargs)

    def _adicionar_aluno(self, dict_values):
        """
        Adiciona 1 aluno à base de dados MongoDB.
        """
        # inserir na base de dados Mongo, coluna "Aluno"
        self.database["Aluno"].insert_one(dict_values)

    def _atualizar_aluno(self, dados: pd.DataFrame):
        """
        Atualiza 1 aluno da base de dados MongoDB.
        """
        self.database["Aluno"].update_one(dict_values)

    def _apagar_aluno(self, dict_values):
        """
        Apaga 1 aluno da basede dados MongoDB.

        """
        # Apagar da tabela Aluno
        self.database["Aluno"].delete_one(dict_values)

    def on_created(self, event):
        """
        Evento disparado sempre que é criado o ficheiro.
        """
        # Primeiro mudamos o nome do ficheiro para um nome unico (para evitar clashes)
        # Para isso marcamos o ficheiro com um timestamp
        new_name = (
            event.src_path.split("/aluno.csv")[0]
            + f"/aluno_{datetime.datetime.now().timestamp()}.csv"
        )
        # Fazemos entao o rename para um nome unico
        os.rename(event.src_path, new_name)

        # lemos o novo ficheiro .csv com o pandas
        # usamos iloc[0] para ir buscar a primeira row apenas
        # (pois o ficheiro apenas contem 1 linha)
        # Lemos tudo como tipo string para os números nao serem
        # lidos como numpy, pois o pymongo nao sabe lidar com numeros numpy
        df = pd.read_csv(new_name, dtype="str").iloc[0]

        # Primeiro verificamos qual a ação a efetuar
        # (e retiramos do df)
        action = df.pop("Action")

        # Converter para dicionario (formato nativo do MongoDB)
        dict_values = df.to_dict()
        # Log para a consola
        print(f"ALTERAÇÕES DETETADAS {new_name}:")
        print(f"\tAction: {action}")
        print(f"\tValores: {dict_values}")

        # Agora decidimos o que fazer com base na acao
        if action == "create":
            self._adicionar_aluno(dict_values)
        elif action == "update":
            self._atualizar_aluno(dict_values)
        elif action == "delete":
            self._apagar_aluno(dict_values)


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
