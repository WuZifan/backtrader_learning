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

 Date: 09/10/2021 15:40:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stock_earning_report
-- ----------------------------
DROP TABLE IF EXISTS `stock_earning_report`;
CREATE TABLE `stock_earning_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` text,
  `earning_per_share` double DEFAULT NULL,
  `revenue` double DEFAULT NULL,
  `revenue_yoy_rise` double DEFAULT NULL,
  `revenue_sos_rise` double DEFAULT NULL,
  `net_profit` double DEFAULT NULL,
  `net_profit_yoy_rise` double DEFAULT NULL,
  `net_profit_sos_rise` double DEFAULT NULL,
  `return_on_equity` double DEFAULT NULL,
  `operating_cash_flow_per_share` double DEFAULT NULL,
  `gross_profit_ratio` double DEFAULT NULL,
  `year` bigint DEFAULT NULL,
  `date` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=276593 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
