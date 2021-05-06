DROP DATABASE IF EXISTS ex2;
create database ex2;
use ex2;

-- Garantir novos users
DROP USER IF EXISTS 'gestor_livros'@'localhost' ;
DROP USER IF EXISTS 'gestor_emprestimos'@'localhost' ;
DROP USER IF EXISTS 'gestor_alunos'@'localhost' ;


-- Primeiro criamos utilizadores
CREATE USER 'gestor_livros'@'localhost' IDENTIFIED BY 'password'; 
CREATE USER 'gestor_emprestimos'@'localhost' IDENTIFIED BY 'password'; 
CREATE USER 'gestor_alunos'@'localhost' IDENTIFIED BY 'password';


-- Criar Tabela "Aluno"
CREATE TABLE Aluno(
	numero_aluno integer NOT NULL AUTO_INCREMENT,
    nome varchar(255) NOT NULL,
    endereco varchar(255) NOT NULL,
    garantia integer not null,
    
    PRIMARY KEY (numero_aluno)
);

-- Dar permissoes ao utilizador criado

--
CREATE TABLE Livro(
	numero_livro integer NOT NULL AUTO_INCREMENT,
    titulo varchar(255) NOT NULL,
    autor varchar(255) NOT NULL,
    editor varchar(255) NOT NULL,
    data_compra datetime NOT NULL default now(),
    estado bit not null default 0,
    
    PRIMARY KEY (numero_livro)
);

CREATE TABLE Emprestimo(
	numero_aluno integer NOT NULL,
    numero_livro integer NOT NULL,
    data_requisicao datetime NOT NULL default now(),
    data_entrega datetime,
    
    FOREIGN KEY(numero_aluno) references Aluno(numero_aluno),
    FOREIGN KEY(numero_livro) references Livro(numero_livro),
    PRIMARY KEY(numero_aluno, numero_livro, data_requisicao)
);

-- PROCEDURES A CRIAR:
-- 1. CRUD Alunos; 2. CRUD Livros; 3. Emprestimo/Devolucao/Relatorio Livros
-- ===========================================================================================
-- Alunos
-- ===========================================================================================
DELIMITER $$


-- 1. Listar alunos
CREATE PROCEDURE listar_alunos ()
BEGIN
	SELECT * FROM Aluno;
END $$
-- 2. Adicionar novo aluno

CREATE PROCEDURE adicionar_aluno (IN nome_new text, IN endereco_new text, IN garantia_new text)
BEGIN
	INSERT INTO Aluno(nome, endereco, garantia)
    VALUES (nome_new, endereco_new, garantia_new);
END $$


-- 3. Update de um aluno

CREATE PROCEDURE atualizar_aluno (IN n_aluno integer, IN nome_new text, IN endereco_new text, IN garantia_new text)
BEGIN
	UPDATE Aluno
    SET nome=nome_new, endereco=endereco_new, garantia=garantia_new
    WHERE numero_aluno=n_aluno;
END $$

-- 4. Apagar um aluno
DELIMITER $$
CREATE PROCEDURE apagar_aluno (IN n_aluno integer)
BEGIN
	DELETE FROM Aluno
    WHERE numero_aluno=n_aluno;
END $$

-- Damos permissoes ao utilizador "gestor_alunos" de executar estes procedures
GRANT EXECUTE ON PROCEDURE listar_alunos TO 'gestor_alunos'@'localhost'; 
GRANT EXECUTE ON PROCEDURE adicionar_aluno TO 'gestor_alunos'@'localhost'; 
GRANT EXECUTE ON PROCEDURE atualizar_aluno TO 'gestor_alunos'@'localhost'; 
GRANT EXECUTE ON PROCEDURE apagar_aluno TO 'gestor_alunos'@'localhost'; 

-- ===========================================================================================
-- Livros
-- ===========================================================================================
-- 5. Listar livros
CREATE PROCEDURE listar_livros ()
BEGIN
	SELECT * FROM Livro;
END $$

-- 6. Criar um livro
CREATE PROCEDURE adicionar_livro(IN titulo_new varchar(255), IN autor_new varchar(255), IN editor_new varchar(255))
BEGIN
	INSERT INTO Livro(titulo, autor, editor)
    VALUES (titulo_new, autor_new, editor_new);
END $$

-- 7. Update de um livro
CREATE PROCEDURE atualizar_livro(IN n_livro integer, IN titulo_new varchar(255), IN autor_new varchar(255), IN editor_new varchar(255))
BEGIN 
	UPDATE Livro
    SET titulo=titulo_new, autor=autor_new, editor=editor_new
    WHERE numero_livro = n_livro;
END $$

-- 8. Apagar um livro
CREATE PROCEDURE apagar_livro(IN n_livro integer)
BEGIN
	DELETE FROM Livro
    WHERE numero_livro = n_livro;
END $$

-- Damos permissoes ao utilizador "gestor_livros" de executar estes procedures
GRANT EXECUTE ON PROCEDURE listar_livros TO 'gestor_livros'@'localhost'; 
GRANT EXECUTE ON PROCEDURE adicionar_livro TO 'gestor_livros'@'localhost'; 
GRANT EXECUTE ON PROCEDURE atualizar_livro TO 'gestor_livros'@'localhost'; 
GRANT EXECUTE ON PROCEDURE apagar_livro TO 'gestor_livros'@'localhost'; 

-- ===========================================================================================
-- Empréstimos
-- ===========================================================================================

-- . Criar emprestimo
CREATE PROCEDURE adicionar_emprestimo(IN n_aluno integer, IN n_livro integer)
BEGIN
	-- So fazemos emprestimo se livro estiver disponivel
    IF (SELECT estado FROM Livro WHERE numero_livro=n_livro)=0 THEN
		INSERT INTO Emprestimo(numero_aluno, numero_livro)
		VALUES (n_aluno, n_livro);
		
		-- Colocar o livro como requisitado
		UPDATE Livro
		SET estado=1
		WHERE numero_livro=n_livro;
	END IF;
END $$

-- 8. Devolver livro
CREATE PROCEDURE devolver_livro(IN n_aluno integer, IN n_livro integer, IN d_requisicao integer)
BEGIN
	UPDATE Emprestimo
    SET data_entrega=now()
    WHERE numero_aluno=n_aluno and numero_livro=n_livro and data_requisicao=d_requisicao;
    
    -- Colocar estado do livro a normal
    UPDATE Livro
    SET estado=0
    WHERE numero_livro=n_livro;
    
END $$

-- 9. Relatório de livros não entregues
CREATE PROCEDURE relatorio_livros_nao_entregues(IN n_aluno integer)
BEGIN
	-- O relatorio pode ser feito utilizando um numero de aluno para verificar 
    -- os livros nao entregues de um determinado aluno. Se for passado 'null'
    -- o relatorio é feito com todos os livros não entregues
    IF n_aluno IS NULL THEN
		-- Selecionamos todos os nao entregues
        SELECT * FROM Livro WHERE estado=1;
    ELSE
		-- Senão vamos buscar todos os numeros de livros que não estao entregues de um determinado utilizador
        -- e depois utilizamos essas chaves para filtrar a coluna Livro
		SELECT * From Livro WHERE numero_livro IN (SELECT numero_livro FROM Emprestimo WHERE data_entrega is null AND numero_aluno=n_aluno);
    END IF;
END $$


-- Damos permissoes ao utilizador "gestor_emprestimos" de executar estes procedures
GRANT EXECUTE ON PROCEDURE adicionar_emprestimo TO 'gestor_emprestimos'@'localhost' $$
GRANT EXECUTE ON PROCEDURE devolver_livro TO 'gestor_emprestimos'@'localhost' $$
GRANT EXECUTE ON PROCEDURE relatorio_livros_nao_entregues TO 'gestor_emprestimos'@'localhost' $$ 

-- ===========================================================================================
-- Triggers
-- ===========================================================================================

-- Em MySQL os triggers não podem ter código dinâmico, o que não permite nomes de ficheiro dinamicos.
-- MySQL também nao permite dar overwrite ao ficheiro exportado (senão dá erro). Vai ter que ser o watcher
-- a encarregar-se de mudar o nome de ficheiro quando detetar alteracoes

CREATE TRIGGER aluno_inserido
    AFTER INSERT
    ON Aluno FOR EACH ROW
BEGIN
    SELECT * FROM Aluno WHERE numero_aluno = NEW.numero_aluno  INTO OUTFILE 'C:/tmp/aluno.txt'
	FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
	LINES TERMINATED BY '\n';
END$$ 


DELIMITER ;

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;




