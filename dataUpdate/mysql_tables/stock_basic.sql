/*
 Navicat Premium Data Transfer

 Source Server         : Local_MySQL
 Source Server Type    : MySQL
 Source Server Version : 80020
 Source Host           : localhost:3306
 Source Schema         : road2rich2

 Target Server Type    : MySQL
 Target Server Version : 80020
 File Encoding         : 65001

 Date: 09/10/2021 15:40:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stock_basic
-- ----------------------------
DROP TABLE IF EXISTS `stock_basic`;
CREATE TABLE `stock_basic` (
  `code` varchar(100) NOT NULL,
  `symbol` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `market` varchar(100) DEFAULT NULL,
  `list_date` varchar(100) DEFAULT NULL,
  `circulating_market_cap` float DEFAULT NULL,
  `sw_l1` varchar(100) DEFAULT NULL,
  `sw_l3` varchar(100) DEFAULT NULL,
  `circulating_cap` float DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
