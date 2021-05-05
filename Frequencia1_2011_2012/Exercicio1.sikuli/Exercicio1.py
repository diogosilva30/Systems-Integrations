# Importar biblioteca de parsing de argumentos (nativa do Python, não é necessário instalar)
import argparse

# Criar parser de argumentos
parser = argparse.ArgumentParser()
# Adicionar argumento para email
parser.add_argument('--email', help='Email de destino', required=True)
# adicionar argumento para assunto
parser.add_argument('--assunto', help='Assunto do email a enviar', required=True)
# adicionar argumento para corpo
parser.add_argument('--corpo', help='Corpo da mensagem a enviar', required=True)

# Fazer o parsing
# Exemplo de uso: "java -jar caminho/para/o/sikuli -r caminho/projeto/ --args --email "sample@email.com" --assunto "Assunto de teste"
# --corpo "Mensagem do email de exemplo"
args=parser.parse_args()

# Primeiro abrimos o menu do windows
click("1620142186740.png")

wait(2)

# Pesquisar pelo MAIL do outlook
type("MAIL" + Key.ENTER)

# Carregar em "New mail"
click("1620142362639.png")

wait(3)
# Agora escrevemos o email e damos ENTER para confirmar a escrita do email,
# Para a caixa flutante dos contactos nao tapar a proxima linha
type(args.email + Key.ENTER)

# Agora clicamos em "Subject"
click("1620142843351.png")

type(args.assunto)
# Agora basta dar tab para trocar para o corpo da mensagem
type(Key.TAB + args.corpo)

# Depois clicamos em send
click("1620142711860.png")