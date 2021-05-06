import requests

resp = requests.post("http://localhost/", json={"op":"2", "aluno":"Silva", "livro": "Sample Book"})
print(resp.text)
