DROP DATABASE IF EXISTS ex2;
create database ex2;
use ex2;

CREATE TABLE Aluno(
	numero_aluno integer NOT NULL AUTO_INCREMENT,
    nome varchar(255) NOT NULL,
    endereco varchar(255) NOT NULL,
    garantia integer not null,
    
    PRIMARY KEY (numero_aluno)
);

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

-- 1. Adicionar novo aluno

CREATE PROCEDURE adicionar_aluno (IN nome_new text, IN endereco_new text, IN garantia_new text)
BEGIN
	INSERT INTO Aluno(nome, endereco, garantia)
    VALUES (nome_new, endereco_new, garantia_new);
    
    -- Agora temos que dar return do id gerado para o aluno 
    SELECT LAST_INSERT_ID() INTO @Alun;
END $$


-- 2. Update de um aluno

CREATE PROCEDURE atualizar_aluno (IN n_aluno integer, IN nome_new text, IN endereco_new text, IN garantia_new text)
BEGIN
	UPDATE Aluno
    SET nome=nome_new, endereco=endereco_new, garantia=garantia_new
    WHERE numero_aluno=n_aluno;
END $$

-- 3. Apagar um aluno
DELIMITER $$
CREATE PROCEDURE apagar_aluno (IN n_aluno integer)
BEGIN
	DELETE FROM Aluno
    WHERE numero_aluno=n_aluno;
END $$

-- ===========================================================================================
-- Livros
-- ===========================================================================================
-- 4. Criar um livro
CREATE PROCEDURE adicionar_livro(IN titulo_new varchar(255), IN autor_new varchar(255), IN editor_new varchar(255))
BEGIN
	INSERT INTO Livro(titulo, autor, editor)
    VALUES (titulo_new, autor_new, editor_new);
END $$

-- 5. Update de um livro
CREATE PROCEDURE atualizar_livro(IN n_livro integer, IN titulo_new varchar(255), IN autor_new varchar(255), IN editor_new varchar(255))
BEGIN 
	UPDATE Livro
    SET titulo=titulo_new, autor=autor_new, editor=editor_new
    WHERE numero_livro = n_livro;
END $$

-- 6. Apagar um livro
CREATE PROCEDURE apagar_livro(IN n_livro integer)
BEGIN
	DELETE FROM Livro
    WHERE numero_livro = n_livro;
END $$

-- ===========================================================================================
-- Empréstimos
-- ===========================================================================================

-- 7. Criar emprestimo
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
DELIMITER ;


