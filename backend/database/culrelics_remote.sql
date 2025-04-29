/*
 Navicat Premium Data Transfer

 Source Server         : mysql2201
 Source Server Type    : MySQL
 Source Server Version : 80027 (8.0.27)
 Source Host           : 123.56.47.51:3308
 Source Schema         : cultural_relics

 Target Server Type    : MySQL
 Target Server Version : 80027 (8.0.27)
 File Encoding         : 65001

 Date: 27/04/2025 20:02:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment_like
-- ----------------------------
DROP TABLE IF EXISTS `comment_like`;
CREATE TABLE `comment_like`  (
  `comment_id` bigint UNSIGNED NOT NULL COMMENT '评论id',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户id',
  PRIMARY KEY (`comment_id`, `user_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '评论点赞表';

-- ----------------------------
-- Records of comment_like
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for complaint_feedback
-- ----------------------------
DROP TABLE IF EXISTS `complaint_feedback`;
CREATE TABLE `complaint_feedback`  (
  `feedback_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '反馈ID',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户ID',
  `feedback_type` tinyint UNSIGNED NOT NULL COMMENT '反馈类型，1：投诉，2：建议，3：错误报告，4：其他',
  `feedback_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '反馈内容',
  `contact_info` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系方式（邮箱/电话）',
  `process_status` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '处理状态，0：未处理，1：处理中，2：已处理，3：已关闭',
  `process_remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '处理备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间|反馈时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间|处理时间',
  PRIMARY KEY (`feedback_id`) USING BTREE,
  INDEX `idx_user`(`user_id` ASC) USING BTREE COMMENT '用户维度筛选',
  INDEX `idx_status`(`process_status` ASC) USING BTREE COMMENT '状态维度筛选',
  INDEX `idx_type`(`feedback_type` ASC) USING BTREE COMMENT '类型维度筛选'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户投诉反馈表';

-- ----------------------------
-- Records of complaint_feedback
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for cultural_relic
-- ----------------------------
DROP TABLE IF EXISTS `cultural_relic`;
CREATE TABLE `cultural_relic`  (
  `relic_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '文物id',
  `museum_id` bigint UNSIGNED NOT NULL COMMENT '博物馆id',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文物名称',
  `dynasty` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文物朝代',
  `type` int NULL DEFAULT NULL COMMENT '文物类型(标签)',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '文物介绍',
  `likes_count` bigint UNSIGNED NULL DEFAULT 0 COMMENT '点赞数',
  `views_count` bigint UNSIGNED NULL DEFAULT 0 COMMENT '阅读量',
  `author` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '作者',
  `region` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地区',
  `theme` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '主题',
  `time` int NULL DEFAULT NULL COMMENT '文物时间（年份，负数为公元前）',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`relic_id`) USING BTREE,
  INDEX `idx_museum_id`(`museum_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文物表';

-- ----------------------------
-- Records of cultural_relic
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for image
-- ----------------------------
DROP TABLE IF EXISTS `image`;
CREATE TABLE `image`  (
  `image_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '图片id',
  `feature_value` int NULL DEFAULT NULL COMMENT '图片特征值',
  PRIMARY KEY (`image_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '图片表';

-- ----------------------------
-- Records of image
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for museum
-- ----------------------------
DROP TABLE IF EXISTS `museum`;
CREATE TABLE `museum`  (
  `museum_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '博物馆Id',
  `museum_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '博物馆名字',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '博物馆介绍',
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '博物馆线下地址',
  `website_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '博物馆网站链接',
  `booking_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '博物馆预约链接',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`museum_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '博物馆表';

-- ----------------------------
-- Records of museum
-- ----------------------------
BEGIN;
INSERT INTO `museum` (`museum_id`, `museum_name`, `description`, `address`, `website_url`, `booking_url`, `create_time`, `update_time`) VALUES (1, '2', NULL, NULL, NULL, NULL, '2025-04-27 02:39:58', '2025-04-27 02:40:37');
COMMIT;

-- ----------------------------
-- Table structure for museum_notice
-- ----------------------------
DROP TABLE IF EXISTS `museum_notice`;
CREATE TABLE `museum_notice`  (
  `notice_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '公告id',
  `museum_id` bigint UNSIGNED NOT NULL COMMENT '博物馆id',
  `notice_title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告标题',
  `notice_time` datetime NOT NULL COMMENT '公告时间',
  `notice_author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公告作者',
  `notice_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告内容',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`notice_id`) USING BTREE,
  INDEX `idx_museum_id`(`museum_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '博物馆公告表';

-- ----------------------------
-- Records of museum_notice
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for relic_comment
-- ----------------------------
DROP TABLE IF EXISTS `relic_comment`;
CREATE TABLE `relic_comment`  (
  `comment_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '评论id',
  `relic_id` bigint UNSIGNED NOT NULL COMMENT '文物id',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户id',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '评论内容',
  `parent_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '父评论ID（为NULL表示顶级评论）',
  `like_count` int UNSIGNED NULL DEFAULT 0 COMMENT '点赞数',
  `reply_count` int UNSIGNED NULL DEFAULT 0 COMMENT '回复数',
  `is_deleted` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '删除标记（0：未删除，1：已删除）',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间，也作为评论时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录修改时间，如果删除可作为删除时间',
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `idx_relic_id`(`relic_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_parent_id`(`parent_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文物评论表';

-- ----------------------------
-- Records of relic_comment
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for relic_like
-- ----------------------------
DROP TABLE IF EXISTS `relic_like`;
CREATE TABLE `relic_like`  (
  `relic_id` bigint UNSIGNED NOT NULL COMMENT '文物id',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户id',
  PRIMARY KEY (`relic_id`, `user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文物点赞表';

-- ----------------------------
-- Records of relic_like
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for relic_video
-- ----------------------------
DROP TABLE IF EXISTS `relic_video`;
CREATE TABLE `relic_video`  (
  `video_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '视频ID（自增主键）',
  `relic_id` bigint UNSIGNED NOT NULL COMMENT '文物ID',
  `video_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '视频地址（不为null则是第三方url，为null表示本地存储）',
  `is_official` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '官方标记（0：用户上传；1：官方发布）',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '视频标题',
  `duration` int UNSIGNED NULL DEFAULT NULL COMMENT '视频时长（秒）',
  `view_count` int UNSIGNED NULL DEFAULT 0 COMMENT '播放次数',
  `status` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '状态（0：下架；1：正常；2：审核中）',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间，也作为上传时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`video_id`) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE COMMENT '状态筛选'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文物讲解视频表';

-- ----------------------------
-- Records of relic_video
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '电话号码',
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `id_number` char(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '身份证号',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户简介',
  `gender` tinyint(1) NULL DEFAULT NULL COMMENT '用户性别，0：女，1：男',
  `age` tinyint UNSIGNED NULL DEFAULT NULL COMMENT '年龄',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地址',
  `wechat` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '微信号',
  `qq` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'qq号',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '用户状态, 0:禁用,1:启用',
  `role_type` tinyint NOT NULL DEFAULT 0 COMMENT '用户角色, 0:用户,1:管理员',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表';

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` (`user_id`, `phone_number`, `password`, `id_number`, `name`, `description`, `gender`, `age`, `address`, `wechat`, `qq`, `status`, `role_type`, `create_time`, `update_time`) VALUES (1, '13566666666', 'c8837b23ff8aaa8a2dde915473ce0991', '', '测试账户01', NULL, NULL, NULL, NULL, NULL, NULL, 1, 1, '2025-04-20 02:12:09', '2025-04-20 02:12:09');
COMMIT;

-- ----------------------------
-- Table structure for user_browsing_history
-- ----------------------------
DROP TABLE IF EXISTS `user_browsing_history`;
CREATE TABLE `user_browsing_history`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户ID',
  `relic_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '文物ID（可为空，非所有浏览都关联文物）',
  `museum_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '博物馆ID（可为空，非所有浏览都关联博物馆）',
  `browse_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user`(`user_id` ASC) USING BTREE COMMENT '用户维度查询',
  INDEX `idx_time`(`browse_time` ASC) USING BTREE COMMENT '时间范围查询'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户浏览记录表';

-- ----------------------------
-- Records of user_browsing_history
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_favorite
-- ----------------------------
DROP TABLE IF EXISTS `user_favorite`;
CREATE TABLE `user_favorite`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户ID',
  `museum_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '博物馆ID',
  `relic_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '文物ID',
  `favorite_type` tinyint UNSIGNED NOT NULL COMMENT '收藏类型：0：博物馆，1：文物',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user`(`user_id` ASC) USING BTREE COMMENT '用户维度查询',
  INDEX `idx_favorite_type`(`favorite_type` ASC) USING BTREE COMMENT '类型维度查询'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户收藏记录表';

-- ----------------------------
-- Records of user_favorite
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_search_history
-- ----------------------------
DROP TABLE IF EXISTS `user_search_history`;
CREATE TABLE `user_search_history`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户ID',
  `relic_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '关联文物ID',
  `search_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '搜索关键词或内容',
  `image_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '搜图关联的图片ID',
  `search_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '搜索时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE COMMENT '用户维度筛选',
  INDEX `idx_time`(`search_time` ASC) USING BTREE COMMENT '时间范围查询'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户搜索记录表';

-- ----------------------------
-- Records of user_search_history
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
