-- --------------------------------------------------------
-- 主机:                           192.168.2.103
-- 服务器版本:                        5.5.57-0+deb8u1 - (Raspbian)
-- 服务器操作系统:                      debian-linux-gnu
-- HeidiSQL 版本:                  9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 vendor_machine 的数据库结构
CREATE DATABASE IF NOT EXISTS `vendor_machine` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `vendor_machine`;

-- 导出  表 vendor_machine.tbl_vm_status 结构
CREATE TABLE IF NOT EXISTS `tbl_vm_status` (
  `machine_name` char(9) COLLATE utf8_bin NOT NULL,
  `machine_status` tinyint(4) NOT NULL,
  `last_response_date` datetime DEFAULT NULL,
  `db_insert_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Vendor machine status';

-- 数据导出被取消选择。
-- 导出  表 vendor_machine.tbl_vm_txn_his 结构
CREATE TABLE IF NOT EXISTS `tbl_vm_txn_his` (
  `machine_name` char(9) COLLATE utf8_bin NOT NULL,
  `block_no` int(11) NOT NULL,
  `txn_no` int(11) NOT NULL,
  `pay_method` char(50) COLLATE utf8_bin DEFAULT NULL,
  `sold_price` int(11) DEFAULT NULL,
  `cost` int(11) DEFAULT NULL,
  `item_name` char(50) COLLATE utf8_bin DEFAULT NULL,
  `item_amount` int(11) DEFAULT NULL,
  `txn_date` datetime DEFAULT NULL,
  `transfer_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Transaction hisotry of vendor machine';

-- 数据导出被取消选择。
-- 导出  视图 vendor_machine.vw_profit 结构
-- 创建临时表以解决视图依赖性错误
CREATE TABLE `vw_profit` (
	`machine_name` CHAR(9) NOT NULL COLLATE 'utf8_bin',
	`block_no` INT(11) NOT NULL,
	`txn_no` INT(11) NOT NULL,
	`pay_method` CHAR(50) NULL COLLATE 'utf8_bin',
	`sold_price` INT(11) NULL,
	`cost` INT(11) NULL,
	`item_name` CHAR(50) NULL COLLATE 'utf8_bin',
	`item_amount` INT(11) NULL,
	`txn_date` DATETIME NULL,
	`transfer_date` DATETIME NULL,
	`sold_price - cost` BIGINT(12) NULL
) ENGINE=MyISAM;

-- 导出  视图 vendor_machine.vw_profit 结构
-- 移除临时表并创建最终视图结构
DROP TABLE IF EXISTS `vw_profit`;
CREATE ALGORITHM=UNDEFINED DEFINER=`pi`@`%` SQL SECURITY DEFINER VIEW `vw_profit` AS select `tbl_vm_txn_his`.`machine_name` AS `machine_name`,`tbl_vm_txn_his`.`block_no` AS `block_no`,`tbl_vm_txn_his`.`txn_no` AS `txn_no`,`tbl_vm_txn_his`.`pay_method` AS `pay_method`,`tbl_vm_txn_his`.`sold_price` AS `sold_price`,`tbl_vm_txn_his`.`cost` AS `cost`,`tbl_vm_txn_his`.`item_name` AS `item_name`,`tbl_vm_txn_his`.`item_amount` AS `item_amount`,`tbl_vm_txn_his`.`txn_date` AS `txn_date`,`tbl_vm_txn_his`.`transfer_date` AS `transfer_date`,(`tbl_vm_txn_his`.`sold_price` - `tbl_vm_txn_his`.`cost`) AS `sold_price - cost` from `tbl_vm_txn_his`;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
