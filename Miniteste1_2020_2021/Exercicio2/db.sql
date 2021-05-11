DROP DATABASE IF EXISTS mt1;
create database mt1;
use mt1;



-- Garantir clean user
DROP USER IF EXISTS 'gestor_mytable'@'localhost' ;
-- Criar user
CREATE USER 'gestor_mytable'@'localhost' IDENTIFIED BY 'password'; 

-- Criar a tabela
CREATE TABLE MYTABLE(
	ISMT_ID integer,
    ISMT_Name varchar(255),
    ISMT_Weight float,
    PRIMARY KEY(ISMT_ID)
);


-- Criar procedures
DELIMITER $$

CREATE PROCEDURE adicionar (IN ismt_id_new integer, IN ismt_name_new varchar(255), IN ismt_weight_new float)
BEGIN
	INSERT INTO MYTABLE(ISMT_ID, ISMT_Name, ISMT_Weight)
    VALUES (ismt_id_new, ismt_name_new, ismt_weight_new);
END $$

CREATE PROCEDURE remover (IN ismt_id_delete integer)
BEGIN
	DELETE FROM MYTABLE
    WHERE ISMT_ID=ismt_id_delete;
END $$

CREATE PROCEDURE atualizar(IN ismt_id_atualizar integer, IN ismt_name_new varchar(255), IN ismt_weight_new float)
BEGIN 
	UPDATE MYTABLE
    SET ISMT_NAME=ismt_name_new, ISMT_Weight=ismt_weight_new
    WHERE ISMT_ID = ismt_id_atualizar;
END $$

DELIMITER ;

-- Damos permissoes ao utilizador "gestor_mytable" de executar estes procedures
-- Necessário correr as linhas abaixo para a aplicacao poder connectar à base de dados.
-- Este utilizador apenas terá permissoes para executar estes procedures e nada mais. Tem as
-- permissoes minimas necessarias
GRANT EXECUTE ON PROCEDURE adicionar TO 'gestor_mytable'@'localhost'; 
GRANT EXECUTE ON PROCEDURE remover TO 'gestor_mytable'@'localhost'; 
GRANT EXECUTE ON PROCEDURE atualizar TO 'gestor_mytable'@'localhost'; 



SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;





