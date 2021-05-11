"""
Modulo que contem o wrapping da execucao de um serviço sem
recorrer a um navegador

Dependências externas necessárias:
    - 'requests': `pip install requests` # https://pypi.org/project/requests/
"""

import requests

# Fazer pedidos HTTP Post

# Exemplo: Cafe curto com 15 de acucar
response = requests.post("http://localhost/mt1", data={"op": "1", "sugar": "15"})
print(response.text)

# Exemplo: Cafe Longo com 30 de acucar
response = requests.post("http://localhost/mt1", data={"op": "2", "sugar": "30"})
print(response.text)

# Exemplo: Cafe Americano
response = requests.post("http://localhost/mt1", data={"op": "3"})
print(response.text)
