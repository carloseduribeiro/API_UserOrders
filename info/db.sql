CREATE DATABASE IF NOT EXISTS userorders_db;
USE userorders_db;

CREATE TABLE IF NOT EXISTS `user` (
	id INT AUTO_INCREMENT NOT NULL,
	name VARCHAR(150) NOT NULL,
	cpf VARCHAR(11) NOT NULL,
	email VARCHAR(100) NOT NULL,
	phone_number VARCHAR(20) NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME,
	PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `order` (
	id INT AUTO_INCREMENT NOT NULL,
	id_user INT NOT NULL,
	item_description TEXT CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
	item_quantity INT NOT NULL,
	item_price DECIMAL(65,2) NOT NULL,
	total_price DECIMAL(65,2) NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME,
	PRIMARY KEY (id),
	CONSTRAINT FK_UserOrder FOREIGN KEY (id_user) REFERENCES user(id)
) ENGINE=InnoDB;
