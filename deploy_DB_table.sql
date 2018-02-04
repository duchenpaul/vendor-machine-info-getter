CREATE DATABASE `vendor_machine` /*!40100 COLLATE 'utf8_bin' */;
SHOW DATABASES;
/* 进入会话 "Jupiter" */
USE `vendor_machine`;

CREATE TABLE `tbl_vm_status` (
	`machine_name` CHAR(9) NOT NULL,
	`machine_status` TINYINT NOT NULL,
	`last_response_date` DATETIME NULL,
	`db_insert_date` DATETIME NOT NULL
)
COMMENT='Vendor machine status'
COLLATE='utf8_bin'
ENGINE=InnoDB
;