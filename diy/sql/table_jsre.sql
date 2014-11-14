-- -----------------------------------------
-- db tables setup
-- -----------------------------------------

-- CREATE DATABASE 20140226_coocs;
use 20140226_coocs;

-- GET DATA, unzip
-- wget 'https://drive.switch.ch/public.php?service=files&t=71204d4bbf908f574bcd5712084984d4&download'
-- mysql ... --local-infile

-- -------------------------------------------
-- -- data tables
-- -- name format: date_name_{data|feedback}
-- -------------------------------------------

use 20140226_coocs;
CREATE TABLE `20140226_aba_data` (
  `pubmed_id` int(11) NOT NULL,
  `confidence` float NOT NULL,
  `e1_text` varchar(200) NOT NULL,
  `e1_entity` varchar(200) NOT NULL,
  `e1_begin` int(11) NOT NULL,
  `e1_end` int(11) NOT NULL,
  `e2_text` varchar(200) NOT NULL,
  `e2_entity` varchar(200) NOT NULL,
  `e2_begin` int(11) NOT NULL,
  `e2_end` int(11) NOT NULL,
  `extr_topdown` int(1) NOT NULL,
  `extr_kernel` int(1) NOT NULL,
  `extr_rules` int(1) NOT NULL,
  `sentence_begin` int(11) NOT NULL,
  `sentence_end` int(11) NOT NULL,
  `snippet` text NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `idx_e1_entity` (`e1_entity`),
  KEY `idx_e2_entity` (`e2_entity`)
) ENGINE=InnoDB AUTO_INCREMENT=196606 DEFAULT CHARSET=utf8;

CREATE TABLE 20140226_aba_feedback (
  -- from the data table above
  `data_id` int(11) NOT NULL,
  -- 0 no feedback yet
  -- 1 ok (up)
  -- 2 wrong (down)
  `feedback` tinyint(1) NOT NULL DEFAULT '0',
  `user` varchar(128),
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=196606 DEFAULT CHARSET=utf8;

-- LOAD ABA DATA
LOAD DATA LOCAL INFILE 'aba_abstracts_rels.tsv' INTO TABLE 20140226_aba_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'aba_ftns_rels.tsv'      INTO TABLE 20140226_aba_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

-- LOAD brainer data
CREATE TABLE `20140522_brainer_data`     LIKE `20140226_aba_data`;
CREATE TABLE `20140522_brainer_feedback` LIKE `20140226_aba_feedback`;
LOAD DATA LOCAL INFILE 'brainer_rels_idx_2.tsv' INTO TABLE 20140522_brainer_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

-- some stats
SELECT table_name, TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '20140226_coocs';
