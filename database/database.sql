SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

drop database if exists hksova;

--
CREATE DATABASE IF NOT EXISTS `hksova` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_czech_ci;
USE `hksova`;

-- --------------------------------------------------------

--
-- Struktura tabulky `forum`
--

CREATE TABLE `forum` (
  `idForum` int(10) UNSIGNED NOT NULL COMMENT 'PK',
  `idForumSection` int(10) UNSIGNED NOT NULL COMMENT 'FK - sekce',
  `name` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'jmeno autora',
  `text` text COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'text prispevku',
  `insertedAt` datetime NOT NULL COMMENT 'kdy vlozeno',
  `ip` varchar(15) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'z IP',
  `dns` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'DNS preklad IP',
  `browser` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'prohlizec'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


-- --------------------------------------------------------

--
-- Struktura tabulky `forum_section`
--

CREATE TABLE `forum_section` (
  `idForumSection` int(10) UNSIGNED NOT NULL COMMENT 'PK',
  `idYear` int(10) UNSIGNED NOT NULL COMMENT 'FK - rok',
  `section` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'nazev sekce',
  `order` tinyint(10) UNSIGNED NOT NULL COMMENT 'razeni',
  `isVisible` tinyint(10) UNSIGNED NOT NULL COMMENT 'povoleni'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci COMMENT='Sekce fora';


-- --------------------------------------------------------

--
-- Struktura tabulky `mascot`
--

CREATE TABLE `mascot` (
  `mascot` varchar(50) COLLATE utf8mb4_czech_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


-- --------------------------------------------------------

--
-- Struktura tabulky `menu`
--

CREATE TABLE `menu` (
  `idMenu` int(10) UNSIGNED NOT NULL COMMENT 'PK',
  `idYear` int(10) UNSIGNED NOT NULL COMMENT 'FK',
  `idPage` int(10) UNSIGNED DEFAULT NULL,
  `menu` varchar(50) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'jmeno polozky',
  `link` varchar(255) COLLATE utf8mb4_czech_ci DEFAULT NULL COMMENT 'nette cil odkazu | abs url',
  `param` varchar(255) COLLATE utf8mb4_czech_ci DEFAULT NULL COMMENT 'parametry odkazu',
  `order` int(10) UNSIGNED NOT NULL COMMENT 'poradi',
  `isNewPart` tinyint(1) UNSIGNED NOT NULL COMMENT 'vetsi mezera nad polozkou',
  `isPublic` tinyint(1) UNSIGNED NOT NULL COMMENT 'pro verejnost',
  `isPrivate` tinyint(1) UNSIGNED NOT NULL COMMENT '1=reg | 2=hrac | 3=zaplaceno',
  `isVisible` tinyint(1) UNSIGNED NOT NULL COMMENT 'viditelna | jen pro org',
  `isSystem` tinyint(1) UNSIGNED NOT NULL COMMENT 'systemova poloza - nelze vymazat',
  `isCurrentYear` tinyint(1) UNSIGNED NOT NULL COMMENT 'zobrazuje se pouze v aktualnim rocniku'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;

-- --------------------------------------------------------

--
-- Struktura tabulky `page`
--

CREATE TABLE `page` (
  `idPage` int(10) UNSIGNED NOT NULL COMMENT 'PK',
  `idYear` int(10) UNSIGNED NOT NULL COMMENT 'FK',
  `title` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'nazev stranky',
  `url` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'url *.html',
  `texy` text COLLATE utf8mb4_czech_ci DEFAULT NULL COMMENT 'texy stranka',
  `html` text COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'html stranka',
  `isPublic` tinyint(1) UNSIGNED NOT NULL COMMENT 'pro verejnost',
  `isPrivate` tinyint(1) UNSIGNED NOT NULL COMMENT '1=reg | 2=hrac | 3=zaplaceno',
  `isVisible` tinyint(1) UNSIGNED NOT NULL COMMENT 'viditelne | pro orgy',
  `idForumSection` int(10) UNSIGNED DEFAULT NULL COMMENT 'FK - sekce'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;


-- --------------------------------------------------------

--
-- Struktura tabulky `place`
--

CREATE TABLE `place` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK',
  `year` int(10) UNSIGNED DEFAULT NULL COMMENT 'FK',
  `name` varchar(255) NOT NULL,
  `longitude` double NOT NULL,
  `latitude` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Struktura tabulky `player`
--

CREATE TABLE `player` (
  `idPlayer` int(10) UNSIGNED NOT NULL,
  `idTeam` int(10) UNSIGNED NOT NULL,
  `order` tinyint(1) UNSIGNED NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `publicName` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL,
  `age` tinyint(3) UNSIGNED DEFAULT NULL,
  `gameIndex` tinyint(5) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;

-- --------------------------------------------------------

--
-- Struktura tabulky `puzzle`
--

CREATE TABLE `puzzle` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK',
  `year` int(10) UNSIGNED DEFAULT NULL COMMENT 'FK',
  `position` int(11) DEFAULT NULL COMMENT 'poradi',
  `name` varchar(255) NOT NULL,
  `final` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'je posledni/cil',
  `code` varchar(255) NOT NULL COMMENT 'QR kod',
  `description` text DEFAULT NULL COMMENT 'zadani (nazev nahraneho souboru)',
  `id_place` int(11) DEFAULT NULL COMMENT 'FK',
  `specification` text DEFAULT NULL COMMENT 'upresnitko',
  `comment` text DEFAULT NULL COMMENT 'libovolny dalsi komentar',
  `url` tinytext DEFAULT NULL COMMENT 'zadani URL',
  `hint` text DEFAULT NULL COMMENT 'napoveda',
  `hint_interval` int(11) DEFAULT 30 COMMENT 'po kolika minutach jde vzit napovedu',
  `mandatory_additional_info` tinyint(1) DEFAULT 0 COMMENT 'potrebuje k reseni dalsi informaci?',
  `solution` text DEFAULT NULL COMMENT 'tajenka',
  `solution_interval` int(11) DEFAULT NULL COMMENT 'po kolika minutach jde vzit reseni',
  `solution_instructions` text DEFAULT NULL COMMENT 'postup reseni (nazev nahraneho souboru)',
  `solution_url` tinytext DEFAULT NULL COMMENT 'reseni URL',
  `id_forum_section` int(11) DEFAULT NULL COMMENT 'FK - forum_section.idForumSection, prirazeno pri zverejneni po hre',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Struktura tabulky `setting`
--

CREATE TABLE `setting` (
  `idSetting` int(10) UNSIGNED NOT NULL,
  `idYear` int(10) UNSIGNED DEFAULT NULL,
  `param` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL,
  `value` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;

--
-- Vypisuji data pro tabulku `setting`
--

INSERT INTO `setting` (`idSetting`, `idYear`, `param`, `value`) VALUES
(1, NULL, 'org-pass', 'hash'),
(1, NULL, 'org-salt', 'salt'),
(2, 2022, 'max-players', '5'),
(3, 2022, 'min-players', '1'),
(4, 2022, 'reg-from', '2022-06-01'),
(5, 2022, 'reg-to', '2022-09-01'),
(6, 2022, 'paid-to', '2022-09-01'),
(6, 2022, 'account', '2600149940/2010'),
(7, 2022, 'price', '250 Kč za tým');

-- --------------------------------------------------------

--
-- Struktura tabulky `team`
--

CREATE TABLE `team` (
  `idTeam` int(10) UNSIGNED NOT NULL COMMENT 'PK',
  `idYear` int(10) UNSIGNED NOT NULL COMMENT 'rocnik',
  `name` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'jmeno teamu',
  `mascot` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL COMMENT 'maskot',
  `login` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'prihlasovaci jmeno teamu',
  `pass` varchar(100) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'heslo teamu SHA1 + salat',
  `salt` varchar(100) COLLATE utf8mb4_czech_ci COMMENT 'sul',
  `email` varchar(255) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'E-mail',
  `mobil` varchar(30) COLLATE utf8mb4_czech_ci NOT NULL COMMENT 'kontaktni mobil',
  `webUrl` varchar(255) COLLATE utf8mb4_czech_ci DEFAULT NULL COMMENT 'web teamu',
  `reportUrl` varchar(255) COLLATE utf8mb4_czech_ci DEFAULT NULL COMMENT 'report teamu',
  `isPaid` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'maji zaplaceno',
  `isBackup` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'nahradnici',
  `isDeleted` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'vyrazeni ze hry',
  `registeredAt` datetime NOT NULL COMMENT 'datum a cas registrace',
  `passResetCode` varchar(100) COLLATE utf8mb4_czech_ci DEFAULT NULL COMMENT 'kod poslany E-mailem',
  `passResetAt` datetime DEFAULT NULL COMMENT 'kdy to bylo odeslano'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;

-- --------------------------------------------------------

--
-- Struktura tabulky `year`
--

CREATE TABLE `year` (
  `idYear` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_czech_ci;

--
-- Vypisuji data pro tabulku `year`
--

INSERT INTO `year` (`idYear`) VALUES
(2022);

--
-- Indexy pro exportované tabulky
--

--
-- Indexy pro tabulku `forum`
--
ALTER TABLE `forum`
  ADD PRIMARY KEY (`idForum`),
  ADD KEY `idForumSection` (`idForumSection`);
  
--
-- Indexy pro tabulku `forum_section`
--
ALTER TABLE `forum_section`
  ADD PRIMARY KEY (`idForumSection`),
  ADD KEY `idYear` (`idYear`);

--
-- Indexy pro tabulku `mascot`
--
ALTER TABLE `mascot`
  ADD UNIQUE KEY `mascot` (`mascot`);

--
-- Indexy pro tabulku `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`idMenu`),
  ADD KEY `idYear` (`idYear`),
  ADD KEY `idPage` (`idPage`);

--
-- Indexy pro tabulku `page`
--
ALTER TABLE `page`
  ADD PRIMARY KEY (`idPage`),
  ADD UNIQUE KEY `url` (`url`,`idYear`),
  ADD KEY `idYear` (`idYear`),
  ADD KEY `idForumSection` (`idForumSection`);

--
-- Indexy pro tabulku `place`
--
ALTER TABLE `place`
  ADD KEY `year` (`year`);

--
-- Indexy pro tabulku `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`idPlayer`),
  ADD UNIQUE KEY `order` (`order`,`idTeam`),
  ADD KEY `idTeam` (`idTeam`);

--
-- Indexy pro tabulku `puzzle`
--
ALTER TABLE `puzzle`
  ADD KEY `id_place` (`id_place`),
  ADD KEY `year` (`year`);

--
-- Indexy pro tabulku `setting`
--
ALTER TABLE `setting`
  ADD PRIMARY KEY (`idSetting`),
  ADD UNIQUE KEY `idYear` (`idYear`,`param`),
  ADD KEY `param` (`param`);

--
-- Indexy pro tabulku `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`idTeam`),
  ADD UNIQUE KEY `idYear` (`idYear`,`name`),
  ADD UNIQUE KEY `login` (`login`,`idYear`),
  ADD UNIQUE KEY `email` (`email`,`idYear`);

--
-- Indexy pro tabulku `year`
--
ALTER TABLE `year`
  ADD PRIMARY KEY (`idYear`);

--
-- AUTO_INCREMENT pro tabulky
--

--
-- AUTO_INCREMENT pro tabulku `forum`
--
ALTER TABLE `forum`
  MODIFY `idForum` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK', AUTO_INCREMENT=955;

--
-- AUTO_INCREMENT pro tabulku `forum_section`
--
ALTER TABLE `forum_section`
  MODIFY `idForumSection` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK', AUTO_INCREMENT=184;

--
-- AUTO_INCREMENT pro tabulku `menu`
--
ALTER TABLE `menu`
  MODIFY `idMenu` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK', AUTO_INCREMENT=328;

--
-- AUTO_INCREMENT pro tabulku `page`
--
ALTER TABLE `page`
  MODIFY `idPage` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK', AUTO_INCREMENT=795;

--
-- AUTO_INCREMENT pro tabulku `player`
--
ALTER TABLE `player`
  MODIFY `idPlayer` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3714;

--
-- AUTO_INCREMENT pro tabulku `setting`
--
ALTER TABLE `setting`
  MODIFY `idSetting` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT pro tabulku `team`
--
ALTER TABLE `team`
  MODIFY `idTeam` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK', AUTO_INCREMENT=955;

--
-- AUTO_INCREMENT pro tabulku `year`
--
ALTER TABLE `year`
  MODIFY `idYear` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2023;

--
-- Omezení pro exportované tabulky
--

--
-- Omezení pro tabulku `forum`
--
ALTER TABLE `forum`
  ADD CONSTRAINT `forum_ibfk_1` FOREIGN KEY (`idForumSection`) REFERENCES `forum_section` (`idForumSection`);

--
-- Omezení pro tabulku `forum_section`
--
ALTER TABLE `forum_section`
  ADD CONSTRAINT `forum_section_ibfk_1` FOREIGN KEY (`idYear`) REFERENCES `year` (`idYear`);

--
-- Omezení pro tabulku `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_3` FOREIGN KEY (`idYear`) REFERENCES `year` (`idYear`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `menu_ibfk_5` FOREIGN KEY (`idPage`) REFERENCES `page` (`idPage`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Omezení pro tabulku `page`
--
ALTER TABLE `page`
  ADD CONSTRAINT `page_ibfk_3` FOREIGN KEY (`idYear`) REFERENCES `year` (`idYear`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Omezení pro tabulku `place`
--
ALTER TABLE `place`
  ADD CONSTRAINT `place_ibfk_1` FOREIGN KEY (`year`) REFERENCES `year` (`idYear`) ON DELETE SET NULL;

--
-- Omezení pro tabulku `player`
--
ALTER TABLE `player`
  ADD CONSTRAINT `player_ibfk_2` FOREIGN KEY (`idTeam`) REFERENCES `team` (`idTeam`) ON DELETE CASCADE;

--
-- Omezení pro tabulku `puzzle`
--
ALTER TABLE `puzzle`
  ADD CONSTRAINT `puzzle_ibfk_1` FOREIGN KEY (`id_place`) REFERENCES `place` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `puzzle_ibfk_2` FOREIGN KEY (`year`) REFERENCES `year` (`idYear`) ON DELETE SET NULL;

--
-- Omezení pro tabulku `setting`
--
ALTER TABLE `setting`
  ADD CONSTRAINT `setting_ibfk_3` FOREIGN KEY (`idYear`) REFERENCES `year` (`idYear`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Omezení pro tabulku `team`
--
ALTER TABLE `team`
  ADD CONSTRAINT `team_ibfk_3` FOREIGN KEY (`idYear`) REFERENCES `year` (`idYear`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;