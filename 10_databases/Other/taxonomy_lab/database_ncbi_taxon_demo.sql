DROP SCHEMA IF EXISTS ncbi_taxon;

CREATE SCHEMA ncbi_taxon;

USE ncbi_taxon;


DROP TABLE IF EXISTS `ncbi_names`;

CREATE TABLE `ncbi_names` (
  `tax_id` int unsigned NOT NULL,
  `name_txt` varchar(255) NOT NULL,
  `unique_name` varchar(255) NOT NULL DEFAULT '',
  `name_class` varchar(63) NOT NULL
);

LOAD DATA LOCAL INFILE '/Users/squiresrb/Desktop/taxdmp/names.dmp' 
INTO TABLE `ncbi_names` 
FIELDS TERMINATED BY '\t|\t' 
LINES TERMINATED BY '\t|\n' 
(tax_id, name_txt, unique_name, name_class);


DROP TABLE IF EXISTS `ncbi_nodes`;

CREATE TABLE `ncbi_nodes` (
     `tax_id`                        INT UNSIGNED NOT NULL, 
     `parent_tax_id`                 INT UNSIGNED NOT NULL, 
     `rank`                          VARCHAR(32) NOT NULL, 
     `embl_code`                     VARCHAR(16) DEFAULT NULL, 
     `division_id`                   SMALLINT NOT NULL, 
     `inherited_div_flag`            TINYINT NOT NULL, 
     `genetic_code_id`               SMALLINT NOT NULL, 
     `inherited_gc_flag`             TINYINT NOT NULL, 
     `mitochondrial_genetic_code_id` TINYINT NOT NULL, 
     `inherited_mgc_flag`            TINYINT NOT NULL, 
     `genbank_hidden_flag`           TINYINT NOT NULL, 
     `hidden_subtree_root_flag`      TINYINT NOT NULL, 
     `comments`                      VARCHAR(255) DEFAULT NULL 
);

LOAD DATA LOCAL INFILE '/Users/squiresrb/Desktop/taxdmp/nodes.dmp' 
INTO TABLE `ncbi_nodes`
FIELDS TERMINATED BY '\t|\t' 
LINES TERMINATED BY '\t|\n'
(tax_id,parent_tax_id,rank,embl_code,division_id,inherited_div_flag,
genetic_code_id,inherited_GC_flag,mitochondrial_genetic_code_id,
inherited_MGC_flag,GenBank_hidden_flag,hidden_subtree_root_flag,comments);