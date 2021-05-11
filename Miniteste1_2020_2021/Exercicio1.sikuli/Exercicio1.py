import sys


operacao = sys.argv[1]

if operacao=='calc':
    n1=sys.argv[2]
    op=sys.argv[3]
    n2=sys.argv[4]

    # Carregar menu windows
    click("1620382458265.png")

    wait(2)
    type("Calculator" + Key.ENTER)
    wait(4)
    # Agora é so digitar a operacao
    type(n1)
    type(op)
    type(n2)
    # E depois enter para mostrar resultado
    type(Key.ENTER)
elif operacao=='file':
    # Extrair texto
    texto=sys.argv[2]

    # Carregar menu windows
    click("1620382874722.png")
    wait(2)
    type("Notepad"+Key.ENTER)
    wait(2)
    # Agora escrever texto
    type(texto)

    click("1620383066305.png")
    wait(3)
    click("save.png")

    # Escrever nome ficheiro
    type("file")

    # Enter para guardar
    type(Key.ENTER)
    
    

    