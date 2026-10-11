-- =============================================
-- Campus Forum Database - campus_forum_db
-- MySQL 建表脚本（所有表以 sys_ 开头）
-- =============================================

CREATE DATABASE IF NOT EXISTS `campus_forum_db`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `campus_forum_db`;

-- 按外键依赖顺序删除表（反向）
DROP TABLE IF EXISTS `sys_chat_message`;
DROP TABLE IF EXISTS `sys_chat_conversation`;
DROP TABLE IF EXISTS `sys_like`;
DROP TABLE IF EXISTS `sys_comment`;
DROP TABLE IF EXISTS `sys_post`;
DROP TABLE IF EXISTS `sys_category`;
DROP TABLE IF EXISTS `sys_user`;
DROP TABLE IF EXISTS `sys_role`;

-- -------------------------------------------
-- 1. 角色表 sys_role
-- -------------------------------------------
CREATE TABLE `sys_role` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '角色ID',
    `name`        VARCHAR(50)     NOT NULL        COMMENT '角色名称',
    `code`        VARCHAR(50)     NOT NULL        COMMENT '角色编码',
    `description` VARCHAR(255)    DEFAULT NULL COMMENT '角色描述',
    `is_active`   TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '是否启用 1-是 0-否',
    `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- -------------------------------------------
-- 2. 用户表 sys_user
-- -------------------------------------------
CREATE TABLE `sys_user` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID（主键）',
    `role_id`     BIGINT UNSIGNED NOT NULL DEFAULT 2 COMMENT '角色ID，默认普通用户',
    `phone`       VARCHAR(20)     DEFAULT NULL COMMENT '手机号',
    `email`       VARCHAR(255)    DEFAULT NULL COMMENT '邮箱',
    `password`    VARCHAR(255)    NOT NULL        COMMENT '密码哈希',
    `nickname`    VARCHAR(50)     DEFAULT NULL COMMENT '昵称',
    `avatar`      VARCHAR(500)    DEFAULT NULL COMMENT '头像URL',
    `is_active`   TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '是否激活 1-是 0-否',
    `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_phone` (`phone`),
    UNIQUE KEY `uk_email` (`email`),
    KEY `idx_role_id` (`role_id`),
    CONSTRAINT `fk_user_role` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- -------------------------------------------
-- 3. 帖子分类表 sys_category
-- -------------------------------------------
CREATE TABLE `sys_category` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
    `name`        VARCHAR(50)     NOT NULL        COMMENT '分类名称',
    `icon`        VARCHAR(500)    DEFAULT NULL COMMENT '分类图标URL',
    `sort_order`  INT             NOT NULL DEFAULT 0 COMMENT '排序序号',
    `is_active`   TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '是否启用 1-是 0-否',
    `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子分类表';

-- -------------------------------------------
-- 4. 帖子表 sys_post
-- -------------------------------------------
CREATE TABLE `sys_post` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '帖子ID',
    `user_id`     BIGINT UNSIGNED NOT NULL        COMMENT '发帖用户ID',
    `category_id` BIGINT UNSIGNED DEFAULT NULL    COMMENT '分类ID',
    `title`       VARCHAR(200)    NOT NULL        COMMENT '帖子标题',
    `content`     TEXT            NOT NULL        COMMENT '帖子内容',
    `view_count`  INT UNSIGNED    NOT NULL DEFAULT 0 COMMENT '浏览次数',
    `like_count`  INT UNSIGNED    NOT NULL DEFAULT 0 COMMENT '点赞数',
    `comment_count` INT UNSIGNED  NOT NULL DEFAULT 0 COMMENT '评论数',
    `is_top`      TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '是否置顶 1-是 0-否',
    `is_deleted`  TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '是否删除 1-是 0-否',
    `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_category_id` (`category_id`),
    KEY `idx_created_at` (`created_at`),
    CONSTRAINT `fk_post_user` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_post_category` FOREIGN KEY (`category_id`) REFERENCES `sys_category` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子表';

-- -------------------------------------------
-- 5. 评论表 sys_comment
-- -------------------------------------------
CREATE TABLE `sys_comment` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '评论ID',
    `post_id`     BIGINT UNSIGNED NOT NULL        COMMENT '帖子ID',
    `user_id`     BIGINT UNSIGNED NOT NULL        COMMENT '评论用户ID',
    `parent_id`   BIGINT UNSIGNED DEFAULT NULL    COMMENT '父评论ID（回复评论时使用）',
    `content`     VARCHAR(1000)   NOT NULL        COMMENT '评论内容',
    `like_count`  INT UNSIGNED    NOT NULL DEFAULT 0 COMMENT '点赞数',
    `is_deleted`  TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '是否删除 1-是 0-否',
    `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_post_id` (`post_id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_parent_id` (`parent_id`),
    CONSTRAINT `fk_comment_post` FOREIGN KEY (`post_id`) REFERENCES `sys_post` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_comment_user` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_comment_parent` FOREIGN KEY (`parent_id`) REFERENCES `sys_comment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

-- -------------------------------------------
-- 6. 点赞表 sys_like
-- -------------------------------------------
CREATE TABLE `sys_like` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
    `user_id`     BIGINT UNSIGNED NOT NULL        COMMENT '用户ID',
    `target_id`   BIGINT UNSIGNED NOT NULL        COMMENT '目标ID（帖子ID或评论ID）',
    `target_type` TINYINT         NOT NULL        COMMENT '目标类型 1-帖子 2-评论',
    `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_target` (`user_id`, `target_id`, `target_type`),
    KEY `idx_target` (`target_id`, `target_type`),
    CONSTRAINT `fk_like_user` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='点赞表';

-- -------------------------------------------
-- 7. 聊天会话表 sys_chat_conversation
-- -------------------------------------------
CREATE TABLE `sys_chat_conversation` (
    `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '会话ID',
    `user1_id`      BIGINT UNSIGNED NOT NULL        COMMENT '用户1 ID（较小ID）',
    `user2_id`      BIGINT UNSIGNED NOT NULL        COMMENT '用户2 ID（较大ID）',
    `last_message`  VARCHAR(500)    DEFAULT NULL COMMENT '最后一条消息内容',
    `last_message_at` DATETIME      DEFAULT NULL COMMENT '最后消息时间',
    `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_pair` (`user1_id`, `user2_id`),
    KEY `idx_user1_id` (`user1_id`),
    KEY `idx_user2_id` (`user2_id`),
    KEY `idx_last_message_at` (`last_message_at`),
    CONSTRAINT `fk_conv_user1` FOREIGN KEY (`user1_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_conv_user2` FOREIGN KEY (`user2_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='聊天会话表';

-- -------------------------------------------
-- 8. 聊天消息表 sys_chat_message
-- -------------------------------------------
CREATE TABLE `sys_chat_message` (
    `id`              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '消息ID',
    `conversation_id` BIGINT UNSIGNED NOT NULL        COMMENT '会话ID',
    `sender_id`       BIGINT UNSIGNED NOT NULL        COMMENT '发送者ID',
    `receiver_id`     BIGINT UNSIGNED NOT NULL        COMMENT '接收者ID',
    `content`         VARCHAR(2000)   NOT NULL        COMMENT '消息内容',
    `is_read`         TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '是否已读 1-是 0-否',
    `created_at`      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_conversation_id` (`conversation_id`),
    KEY `idx_sender_id` (`sender_id`),
    KEY `idx_receiver_id` (`receiver_id`),
    KEY `idx_created_at` (`created_at`),
    CONSTRAINT `fk_msg_conversation` FOREIGN KEY (`conversation_id`) REFERENCES `sys_chat_conversation` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_msg_sender` FOREIGN KEY (`sender_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_msg_receiver` FOREIGN KEY (`receiver_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='聊天消息表';

-- -------------------------------------------
-- 初始化角色数据
-- -------------------------------------------
INSERT INTO `sys_role` (`name`, `code`, `description`) VALUES
    ('超级管理员', 'super_admin', '拥有系统所有权限'),
    ('普通用户', 'user', '普通注册用户，默认角色');

-- -------------------------------------------
-- 初始化分类数据
-- -------------------------------------------
INSERT INTO `sys_category` (`name`, `sort_order`) VALUES
    ('综合讨论', 1),
    ('技术交流', 2),
    ('求助问答', 3),
    ('校园生活', 4),
    ('资源分享', 5);