CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `email` varchar(255),
  `password` varchar(255),
  `role` enum(admin,faculty,student) NOT NULL DEFAULT 'student',
  `phone` varchar(100),
  `address` varchar(255),
  `designation` varchar(255),
  `avatar` varchar(255),
  `about` text,
  `website` varchar(255),
  `github` varchar(255),
  `twitter` varchar(255),
  `facebook` varchar(255),
  `vk` varchar(255),
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `posts` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `type` varchar(255) NOT NULL,
  `user_id` int,
  `image` varchar(255),
  `title` varchar(255) NOT NULL,
  `tags` varchar(255),
  `content` longtext,
  `is_announcement` bool NOT NULL DEFAULT false,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `likes` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `model_type` varchar(255) NOT NULL,
  `model_id` int NOT NULL,
  `user_id` int,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `comments` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `model_type` varchar(255) NOT NULL,
  `model_id` int NOT NULL,
  `user_id` int,
  `content` text NOT NULL,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `attachments` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `model_type` varchar(255) NOT NULL,
  `model_id` int NOT NULL,
  `user_id` int,
  `attachment` varchar(255) NOT NULL,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `classes` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `token` varchar(255) UNIQUE NOT NULL,
  `name` varchar(255) NOT NULL,
  `logo` varchar(255),
  `description` mediumtext,
  `capacity` int NOT NULL DEFAULT 1,
  `tags` varchar(255),
  `gc_attendance` float NOT NULL DEFAULT 5,
  `gc_assignment` float NOT NULL DEFAULT 10,
  `gc_quiz` float NOT NULL DEFAULT 20,
  `gc_midterm` float NOT NULL DEFAULT 25,
  `gc_final` float NOT NULL DEFAULT 40,
  `status` bool NOT NULL DEFAULT true,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `enrollments` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `class_id` int,
  `user_id` int,
  `status` bool NOT NULL DEFAULT true,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `grades` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `enrollment_id` int,
  `gc_type` enum(attendance,assignment,quiz,midterm,final) NOT NULL,
  `total_marks` float NOT NULL,
  `obtained_marks` float NOT NULL,
  `obtained_percentage` float NOT NULL,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE INDEX `posts_index_0` ON `posts` (`type`);

CREATE INDEX `posts_index_1` ON `posts` (`type`, `user_id`);

CREATE INDEX `likes_index_2` ON `likes` (`model_type`);

CREATE INDEX `likes_index_3` ON `likes` (`model_type`, `model_id`);

CREATE INDEX `likes_index_4` ON `likes` (`model_type`, `model_id`, `user_id`);

CREATE INDEX `comments_index_5` ON `comments` (`model_type`);

CREATE INDEX `comments_index_6` ON `comments` (`model_type`, `model_id`);

CREATE INDEX `comments_index_7` ON `comments` (`model_type`, `model_id`, `user_id`);

CREATE INDEX `attachments_index_8` ON `attachments` (`model_type`);

CREATE INDEX `attachments_index_9` ON `attachments` (`model_type`, `model_id`);

CREATE INDEX `attachments_index_10` ON `attachments` (`model_type`, `model_id`, `user_id`);

CREATE INDEX `classes_index_11` ON `classes` (`user_id`);

CREATE INDEX `enrollments_index_12` ON `enrollments` (`class_id`);

CREATE INDEX `enrollments_index_13` ON `enrollments` (`user_id`);

CREATE UNIQUE INDEX `enrollments_index_14` ON `enrollments` (`class_id`, `user_id`);

CREATE INDEX `grades_index_15` ON `grades` (`enrollment_id`);

CREATE INDEX `grades_index_16` ON `grades` (`enrollment_id`, `gc_type`);

ALTER TABLE `posts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `likes` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `comments` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `attachments` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `classes` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `enrollments` ADD FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

ALTER TABLE `enrollments` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `grades` ADD FOREIGN KEY (`enrollment_id`) REFERENCES `enrollments` (`id`);
