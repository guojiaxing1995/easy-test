/*
 Navicat Premium Data Transfer

 Source Server         : docker-master
 Source Server Type    : MySQL
 Source Server Version : 50735
 Source Schema         : easy-test

 Target Server Type    : MySQL
 Target Server Version : 50735
 File Encoding         : 65001

 演示初始数据，清除所有数据后导入
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


-- ----------------------------
-- Records of case
-- ----------------------------
INSERT INTO `case` VALUES ('2020-03-30 19:50:19', '2020-03-30 19:50:19', NULL, 2, 'test14', NULL, '/v1/test5', 2, 2, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:50:25', '2020-03-30 19:50:25', NULL, 3, 'test1', NULL, '/v1/test5', 2, 1, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:50:35', '2020-03-30 19:50:35', NULL, 5, 'test3', '史蒂夫', '/v1/test5', 2, 2, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:50:42', '2020-03-30 19:50:42', NULL, 6, 'test4', NULL, '/v1/test5', 2, 1, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:50:45', '2020-03-30 19:50:45', NULL, 7, 'test5', NULL, '/v1/test5', 2, 1, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:50:54', '2020-03-30 19:50:54', NULL, 8, 'test6', NULL, '/v1/test6', 3, 2, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:50:58', '2020-03-30 19:50:58', NULL, 9, 'test7', NULL, '/v1/test6', 4, 1, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:51:02', '2020-03-30 19:51:02', NULL, 10, 'test8', NULL, '/v1/test6', 3, 1, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:51:08', '2020-03-30 19:51:08', NULL, 11, 'test9', NULL, '/v1/test6', 2, 2, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-03-30 19:51:13', '2020-03-30 19:51:13', NULL, 12, 'test10', NULL, '/v1/test6', 1, 1, 'header', 'data', 2, 'key,ke2', '', 1, 1, 7, 1, 1);
INSERT INTO `case` VALUES ('2020-05-02 11:16:31', '2020-06-05 16:02:00', NULL, 27, 'test_a', 'get nwnn    logsss', '/cms/test/a/${id}', 1, 1, NULL, NULL, 1, NULL, 'name,小明啊vvdv', 1, 1, 9, 1, 1);
INSERT INTO `case` VALUES ('2020-05-02 11:24:08', '2020-07-16 06:53:08', NULL, 28, 'test_b', 'post form', '/cms/test/b', 2, 2, '', '{\n\"age\": \"${age}\"\n}', 3, 'age,id time,new_time', 'owww', 4, 1, 9, 1, 6);
INSERT INTO `case` VALUES ('2020-05-02 14:53:18', '2020-05-29 15:52:55', NULL, 29, 'test_c', 'ert', '/cms/test/c', 3, 1, '{\n\"Content-Type\": \"application/json\"\n}', '{\n	\"address\": \"${address}\"\n}', 2, NULL, NULL, 5, 1, 9, 1, 1);
INSERT INTO `case` VALUES ('2020-05-02 14:57:00', '2020-05-03 15:48:52', NULL, 30, 'test_d', NULL, '/cms/test/d', 4, 1, NULL, NULL, 4, 'is(.*)!,address is(.*)!,double', 'sssd', 4, 1, 9, 1, 1);
INSERT INTO `case` VALUES ('2021-01-17 12:14:40', '2021-01-17 12:14:40', NULL, 50, '百度', NULL, '/', 1, 1, NULL, NULL, 1, NULL, NULL, 1, 1, 7, 6, 6);


-- ----------------------------
-- Records of case_group
-- ----------------------------
INSERT INTO `case_group` VALUES ('2020-03-21 15:59:23', '2020-03-28 11:06:05', NULL, 7, '小龙的分组', '龙');
INSERT INTO `case_group` VALUES ('2020-03-28 14:34:24', '2021-08-05 15:15:57', NULL, 9, '飞天萝卜', '');

-- ----------------------------
-- Records of config_copy
-- ----------------------------
INSERT INTO `config_copy` VALUES ('2020-05-02 19:31:00', '2020-07-28 12:31:12', NULL, 10, 8, 1, 1, 30, 'test_d', NULL, '/cms/test/d', 4, 1, NULL, NULL, 4, 'is(.*)!,address is(.*)!,double', 'sssdk', 4, 1);
INSERT INTO `config_copy` VALUES ('2020-05-02 19:31:00', '2020-05-02 23:49:38', NULL, 11, 8, 2, 1, 29, 'test_c', NULL, '/cms/test/c', 3, 1, '{\n\"Content-Type\": \"application/json\"\n}', '{\n	\"address\": \"${address}\"\n}', 2, NULL, NULL, 5, 1);
INSERT INTO `config_copy` VALUES ('2020-05-02 19:31:00', '2020-05-02 19:31:00', NULL, 12, 8, 3, 1, 28, 'test_b', 'post form', '/cms/test/b', 2, 2, '', '{\n\"age\": \"${age}\"\n}', 3, 'age,id time,new_time', 'ow', 3, 1);
INSERT INTO `config_copy` VALUES ('2020-05-02 19:31:00', '2020-05-02 19:54:06', NULL, 13, 8, 4, 1, 27, 'test_a', 'get ', '/cms/test/a/${id}', 1, 1, NULL, NULL, 1, NULL, 'name,小明啊5', 1, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 14, 8, 5, 1, 30, 'test_d', NULL, '/cms/test/d', 4, 1, NULL, NULL, 4, 'is(.*)!,address is(.*)!,double', 'sssd', 4, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 15, 8, 6, 1, 29, 'test_c', 'ert', '/cms/test/c', 3, 1, '{\n\"Content-Type\": \"application/json\"\n}', '{\n	\"address\": \"${address}\"\n}', 2, NULL, NULL, 5, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 16, 8, 7, 1, 28, 'test_b', 'post form', '/cms/test/b', 2, 2, '', '{\n\"age\": \"${age}\"\n}', 3, 'age,id time,new_time', 'owww', 4, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 17, 8, 8, 1, 27, 'test_a', 'get nwnn    logsss', '/cms/test/a/${id}', 1, 1, NULL, NULL, 1, NULL, 'name,小明啊vvdv', 1, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 18, 8, 9, 1, 30, 'test_d', NULL, '/cms/test/d', 4, 1, NULL, NULL, 4, 'is(.*)!,address is(.*)!,double', 'sssd', 4, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 19, 8, 10, 1, 29, 'test_c', 'ert', '/cms/test/c', 3, 1, '{\n\"Content-Type\": \"application/json\"\n}', '{\n	\"address\": \"${address}\"\n}', 2, NULL, NULL, 5, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 20, 8, 11, 1, 28, 'test_b', 'post form', '/cms/test/b', 2, 2, '', '{\n\"age\": \"${age}\"\n}', 3, 'age,id time,new_time', 'owww', 4, 1);
INSERT INTO `config_copy` VALUES ('2020-08-06 17:28:25', '2020-08-06 17:28:25', NULL, 21, 8, 12, 1, 27, 'test_a', 'get nwnn    logsss', '/cms/test/a/${id}', 1, 1, NULL, NULL, 1, NULL, 'name,小明啊vvdv', 1, 1);


-- ----------------------------
-- Records of config_relation
-- ----------------------------
INSERT INTO `config_relation` VALUES ('2020-05-02 15:18:15', '2020-05-02 19:27:17', NULL, 9, 7, 1, 1, 30);
INSERT INTO `config_relation` VALUES ('2020-05-02 15:18:15', '2020-05-02 19:27:17', NULL, 10, 7, 2, 1, 29);
INSERT INTO `config_relation` VALUES ('2020-05-02 15:18:15', '2020-05-02 19:27:17', NULL, 11, 7, 3, 1, 28);
INSERT INTO `config_relation` VALUES ('2020-05-02 15:18:15', '2020-05-04 20:15:49', NULL, 12, 7, 4, 0, 27);
INSERT INTO `config_relation` VALUES ('2021-01-17 12:15:38', '2021-01-17 12:15:38', NULL, 20, 7, 5, 1, 50);

-- ----------------------------
-- Records of lin_auth
-- ----------------------------
INSERT INTO `lin_auth` VALUES (13, 1, '用例分组', '测试用例');
INSERT INTO `lin_auth` VALUES (14, 1, '删除用例分组', '测试用例');
INSERT INTO `lin_auth` VALUES (16, 11, '测试用例', '用例');
INSERT INTO `lin_auth` VALUES (18, 11, '编辑用例', '用例');
INSERT INTO `lin_auth` VALUES (19, 11, '工程列表', '工程');
INSERT INTO `lin_auth` VALUES (20, 11, '工程配置', '工程');
INSERT INTO `lin_auth` VALUES (21, 11, '用例分组', '用例');
INSERT INTO `lin_auth` VALUES (23, 11, '用例日志列表', '测试结果');
INSERT INTO `lin_auth` VALUES (25, 11, '执行记录', '测试结果');
INSERT INTO `lin_auth` VALUES (26, 11, '停止定时任务', '定时任务');
INSERT INTO `lin_auth` VALUES (27, 11, '定时任务列表', '定时任务');
INSERT INTO `lin_auth` VALUES (28, 11, '启动定时任务', '定时任务');
INSERT INTO `lin_auth` VALUES (29, 11, '修改记录', '用例');
INSERT INTO `lin_auth` VALUES (34, 11, '新增定时任务', '定时任务');
INSERT INTO `lin_auth` VALUES (37, 11, '编辑定时任务', '定时任务');
INSERT INTO `lin_auth` VALUES (38, 11, '运行记录', '测试结果');
INSERT INTO `lin_auth` VALUES (39, 11, '运行详情', '测试结果');
INSERT INTO `lin_auth` VALUES (40, 11, 'mock', 'mock管理');
INSERT INTO `lin_auth` VALUES (41, 11, '用例分析', '测试分析');
INSERT INTO `lin_auth` VALUES (42, 11, '删除用例', '用例');
INSERT INTO `lin_auth` VALUES (43, 11, '删除修改记录', '用例');
INSERT INTO `lin_auth` VALUES (44, 11, '新增用例', '用例');

-- ----------------------------
-- Records of lin_file
-- ----------------------------
INSERT INTO `lin_file` VALUES ('2021-08-05 14:28:44', '2021-08-05 14:28:44', NULL, 31, '2021/08/05/6197d98e-f5b6-11eb-8d64-0242c0a86002.jpg', 1, '6197d98e-f5b6-11eb-8d64-0242c0a86002.jpg', '.jpg', 6034, '63b318bfedc9ac5bca9bd33a3d92334e');
INSERT INTO `lin_file` VALUES ('2021-08-05 15:19:39', '2021-08-05 15:19:39', NULL, 32, '2021/08/05/7e81d6ba-f5bd-11eb-9293-0242c0a86002.jpg', 1, '7e81d6ba-f5bd-11eb-9293-0242c0a86002.jpg', '.jpg', 8026, 'a03c8449a8a1a11fb26775d6d09f3b59');

-- ----------------------------
-- Records of lin_group
-- ----------------------------
INSERT INTO `lin_group` VALUES (1, '测试组', '');
INSERT INTO `lin_group` VALUES (2, '0', '测试');
INSERT INTO `lin_group` VALUES (3, '1', '');
INSERT INTO `lin_group` VALUES (4, '2', '');
INSERT INTO `lin_group` VALUES (5, '3', '');
INSERT INTO `lin_group` VALUES (6, '4', '');
INSERT INTO `lin_group` VALUES (7, '5', '');
INSERT INTO `lin_group` VALUES (8, '6', '');
INSERT INTO `lin_group` VALUES (9, '7', '');
INSERT INTO `lin_group` VALUES (10, '8', '');
INSERT INTO `lin_group` VALUES (11, '9', '');
INSERT INTO `lin_group` VALUES (12, '10', '');

-- ----------------------------
-- Records of lin_user
-- ----------------------------
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-03-04 19:50:00', '2021-08-05 15:19:39', NULL, 1, 'super', NULL, '2021/08/05/7e81d6ba-f5bd-11eb-9293-0242c0a86002.jpg', 2, 1, '1234995678@qq.com', NULL, 'pbkdf2:sha256:50000$kNo2Jsin$8137f55f0346103d4357066f782cd2c6a6de0639faec31b36b2273b4dd0c650b', NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-04-06 09:47:23', '2020-04-06 10:05:55', NULL, 2, 'cron', NULL, NULL, 1, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-03-15 10:30:02', '2020-03-15 10:30:02', NULL, 3, 'gjx', NULL, NULL, 1, 1, NULL, 1, 'pbkdf2:sha256:50000$dQj1n9lo$4fe66a271ff262c135a95675722451158883f322efc56f2573c3a292a9d0c4ac', NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-03-15 11:40:56', '2020-03-15 11:40:56', NULL, 4, '小明', NULL, NULL, 1, 1, NULL, 1, 'pbkdf2:sha256:50000$hBH4391V$43df48295077259a44d745f1dca6253576d9ad494ff8a1f2ab7bf11c1c7602db', NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-03-15 16:36:34', '2020-03-15 16:36:34', NULL, 5, '76号', NULL, NULL, 1, 1, 'guojx@citycloud.com.cn', 1, 'pbkdf2:sha256:50000$eUh63qG6$121572fc750a3870d91f2a11cfd05c3ab891e8373f820ad37527f21599564a7b', NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-03-21 14:52:15', '2021-08-05 14:28:44', NULL, 6, '麦克雷', '麦克雷', '2021/08/05/6197d98e-f5b6-11eb-8d64-0242c0a86002.jpg', 1, 1, '302802003@qq.com', 11, 'pbkdf2:sha256:50000$CG4SAUyR$e649bee9885638fa5acac00feee3f8c6c5e7f965579eed331f2dac9ec604921a', NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-03-21 14:52:43', '2020-03-21 14:52:43', NULL, 7, '猎空', NULL, NULL, 1, 1, '15234093915@163.com', 2, 'pbkdf2:sha256:50000$xlW3yKB8$24cfb893c63a286d3fd926dbf784dc72613843a2c70c23144e81af52984d65f8', NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-03-21 14:57:09', '2020-04-21 20:19:54', NULL, 8, '小龙', NULL, NULL, 1, 1, NULL, 11, 'pbkdf2:sha256:50000$Rdrq4kEj$da70521c9b91c6443a71381d4c29474e9d7c9a2802dfbf3f749ced9438099f04', NULL, NULL);
INSERT INTO `easy-test`.`lin_user`(`create_time`, `update_time`, `delete_time`, `id`, `username`, `nickname`, `avatar`, `admin`, `active`, `email`, `group_id`, `password`, `phone`, `openid`) VALUES ('2020-04-06 09:47:23', '2020-04-06 10:05:55', NULL, 9, '小炸', NULL, NULL, 1, 1, NULL, 11, 'pbkdf2:sha256:50000$SCsbf4G9$53a6421800e65918b9c18587db64eb770a7317ced1095aca797f2b20a441e6d7', NULL, NULL);

-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO `project` VALUES ('2020-05-02 14:59:53', '2021-08-02 19:22:57', NULL, 7, 'test_关联', 'www.guojiaxing.red:8085', '{\n  \"token\": \"li\"\n}', NULL, 1, 0, 0, 6, 1, 3, '7,5');
INSERT INTO `project` VALUES ('2020-05-02 19:30:16', '2021-08-02 19:23:48', NULL, 8, 'test_副本', 'http://www.guojiaxing.red:8085', NULL, NULL, 2, 0, 0, 5, 1, 1, '');

-- ----------------------------
-- Records of user_auth
-- ----------------------------
INSERT INTO `user_auth` VALUES ('2020-03-15 17:02:28', '2020-03-15 17:02:28', NULL, 10, 4, 4, 1);
INSERT INTO `user_auth` VALUES ('2020-03-15 17:02:28', '2020-03-15 17:02:28', NULL, 11, 5, 4, 1);
INSERT INTO `user_auth` VALUES ('2020-03-21 17:22:50', '2020-03-21 17:22:50', NULL, 14, 8, 7, 1);
INSERT INTO `user_auth` VALUES ('2020-03-28 14:34:24', '2020-03-28 14:34:24', NULL, 20, 6, 9, 1);
INSERT INTO `user_auth` VALUES ('2020-04-06 08:47:45', '2020-04-06 08:47:45', NULL, 23, 3, 7, 1);
INSERT INTO `user_auth` VALUES ('2020-04-06 10:34:46', '2020-04-06 10:34:46', NULL, 24, 9, 9, 1);
INSERT INTO `user_auth` VALUES ('2020-04-21 20:14:36', '2020-04-21 20:14:36', NULL, 32, 9, 7, 1);
INSERT INTO `user_auth` VALUES ('2020-05-02 14:59:53', '2020-05-02 14:59:53', NULL, 39, 5, 7, 2);
INSERT INTO `user_auth` VALUES ('2020-05-02 19:30:16', '2020-05-02 19:30:16', NULL, 40, 5, 8, 2);
INSERT INTO `user_auth` VALUES ('2020-05-04 15:29:02', '2020-05-04 15:29:02', NULL, 41, 9, 7, 2);
INSERT INTO `user_auth` VALUES ('2020-05-04 15:29:08', '2020-05-04 15:29:08', NULL, 42, 9, 8, 2);
INSERT INTO `user_auth` VALUES ('2020-06-04 08:24:01', '2020-06-04 08:24:01', NULL, 43, 5, 8, 2);
INSERT INTO `user_auth` VALUES ('2020-06-05 12:45:15', '2020-06-05 12:45:15', NULL, 44, 6, 7, 2);
INSERT INTO `user_auth` VALUES ('2020-06-05 12:46:32', '2020-06-05 12:46:32', NULL, 47, 6, 7, 1);
INSERT INTO `user_auth` VALUES ('2020-06-23 22:48:40', '2020-06-23 22:48:40', NULL, 52, 6, 8, 2);

SET FOREIGN_KEY_CHECKS = 1;
