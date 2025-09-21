-- Adminer 5.4.0 MariaDB 12.0.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `place`;
CREATE TABLE `place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(10) unsigned DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `longitude` double NOT NULL,
  `latitude` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `year` (`year`),
  CONSTRAINT `place_ibfk_1` FOREIGN KEY (`year`) REFERENCES `year` (`idYear`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


DROP TABLE IF EXISTS `puzzle`;
CREATE TABLE `puzzle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(10) unsigned DEFAULT NULL,
  `position` int(11) DEFAULT NULL COMMENT 'poradi',
  `name` varchar(255) NOT NULL,
  `final` bit(1) NOT NULL DEFAULT b'0',
  `code` varchar(255) NOT NULL COMMENT 'QR kod',
  `description` text DEFAULT NULL COMMENT 'text sifry',
  `id_place` int(11) DEFAULT NULL,
  `specification` text DEFAULT NULL COMMENT 'upresnitko',
  `comment` text DEFAULT NULL COMMENT 'libovolny dalsi komentar',
  `url` tinytext DEFAULT NULL,
  `hint` text DEFAULT NULL,
  `hint_interval` int(11) DEFAULT 30 COMMENT 'po kolika minutach jde vzit napovedu',
  `mandatory_additional_info` bit(1) DEFAULT NULL COMMENT 'je resitelna bez dalsich informaci?',
  `solution` text DEFAULT NULL COMMENT 'tajenka',
  `solution_interval` int(11) DEFAULT NULL COMMENT 'po kolika minutach jde vzit reseni',
  `solution_instructions` text DEFAULT NULL COMMENT 'postup reseni',
  `solution_url` tinytext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_place` (`id_place`),
  KEY `year` (`year`),
  CONSTRAINT `puzzle_ibfk_1` FOREIGN KEY (`id_place`) REFERENCES `place` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `puzzle_ibfk_2` FOREIGN KEY (`year`) REFERENCES `year` (`idYear`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- 2025-09-21 19:29:14 UTC
