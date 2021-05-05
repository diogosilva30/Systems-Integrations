<?php
 $operacao = $_POST['op'] ;
 if($operacao=='1' || $operacao=='2'){
 $email = $_POST['aluno'] ;
 $message = $_POST['livro'] ;
 }
 switch($operacao){
case('1'):
	echo "OPERACAO 1 (Processar emprestimo) | ALUNO: $email | LIVRO: $message!";
// processar emprestimo
break;
case('2'):
	echo "OPERACAO 2 (Processar devolucao) | ALUNO: $email | LIVRO: $message!";
// processar devolução
break;
case('3'):
	echo "OPERACAO 3 (Processar relatorio)";
// processar relatorio
break;
default:
echo "operação nao suportada";
}
?>