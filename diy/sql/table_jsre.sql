-------------------------------------------
-- db tables setup
-------------------------------------------

CREATE DATABASE 20140226_coocs;

-------------------------------------------
-- data tables
-- name format: date_name_{data|feedback}
-------------------------------------------
use 20140226_coocs;
CREATE TABLE `20140226_br_br_jsre_data` (
  `pubmed_id` int(11) NOT NULL,
  `confidence` float NOT NULL,
  `e1_entity` varchar(200) NOT NULL,
  `e1_begin` int(11) NOT NULL,
  `e1_end` int(11) NOT NULL,
  `e2_entity` varchar(200) NOT NULL,
  `e2_begin` int(11) NOT NULL,
  `e2_end` int(11) NOT NULL,
  `sentence_begin` int(11) NOT NULL,
  `sentence_end` int(11) NOT NULL,
  `snippet` text NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `idx_e1_entity` (`e1_entity`),
  KEY `idx_e2_entity` (`e2_entity`)
) ENGINE=InnoDB AUTO_INCREMENT=196606 DEFAULT CHARSET=utf8;

--
CREATE TABLE 20140226_br_br_nearestn_data LIKE 20140226_br_br_jsre_data;



CREATE TABLE 20140226_br_br_jsre_feedback (
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


/*
INSTRUCTIONS TO LOAD DATA IN

cd to {outputFileDir}
mysql -uroot --local-infile

use 20140226_coocs
LOAD DATA LOCAL INFILE '20131215_br-aba-syn_cooc_jsre.tsv' INTO TABLE br_br_jsre FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE '20131215_br-aba-syn_cooc_nearestn.tsv' INTO TABLE br_br_nearestn FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

*/


/* now with extractors */
-- cd /Users/richarde/Desktop/BBP_experiments/23_extract_brainregions/ABA_connectivity/data/aba_system/20140226_br_rels_aggregate/
-- mysql -h128.178.187.160 -upubtext -pn7nn5fvm0ohngf --local-infile
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
CREATE TABLE 20140226_aba_feedback LIKE 20140226_br_br_jsre_feedback;

LOAD DATA LOCAL INFILE 'aba_abstracts_rels.tsv' INTO TABLE 20140226_aba_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'aba_ftns_rels.tsv' INTO TABLE 20140226_aba_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';


-- LOAD DATA LOCAL INFILE 'aba_rels.tsv' INTO TABLE 20140226_aba_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

CREATE TABLE 20140226_bams_data LIKE 20140226_aba_data;
CREATE TABLE 20140226_bams_feedback LIKE 20140226_br_br_jsre_feedback;
LOAD DATA LOCAL INFILE 'bams_rels.tsv' INTO TABLE 20140226_bams_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';



-- LOAD brainer data
-- cd /Users/richarde/Desktop/BBP_experiments/23_extract_brainregions/ABA_connectivity/data/brainer_system/20140418_br_rels_abstracts_aggregate
-- mysql -h128.178.187.160 -upubtext -pn7nn5fvm0ohngf --local-infile
use 20140226_coocs;
CREATE TABLE `20140509_brainer_data`     LIKE `20140226_aba_data`;
CREATE TABLE `20140509_brainer_feedback` LIKE `20140226_br_br_jsre_feedback`;
LOAD DATA LOCAL INFILE 'brainer_rels_idx.tsv' INTO TABLE 20140509_brainer_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

CREATE TABLE `20140522_brainer_data`     LIKE `20140226_aba_data`;
CREATE TABLE `20140522_brainer_feedback` LIKE `20140226_br_br_jsre_feedback`;
LOAD DATA LOCAL INFILE 'brainer_rels_idx_2.tsv' INTO TABLE 20140522_brainer_data FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

