import requests

resp = requests.post("http://localhost/", data={"op":"2", "aluno":"Silva", "livro": "Sample Book"})
print(resp.text)