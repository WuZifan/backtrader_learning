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

 Date: 09/10/2021 15:40:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for TradingInfo
-- ----------------------------
DROP TABLE IF EXISTS `TradingInfo`;
CREATE TABLE `TradingInfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(100) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `open` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `volume` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_TradingInfo_time` (`time`),
  KEY `ix_TradingInfo_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=74138643 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
