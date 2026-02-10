USE mydb;
-- Run the script selecting part by part, not all at once

-- -----------------------------------------------------
-- PART ZERO --
-- -----------------------------------------------------
-- Only run this part if we want to modify something later --
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE markers;
TRUNCATE TABLE genes;
TRUNCATE TABLE cell_types;
SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------------------
-- PART ONE --
-- -----------------------------------------------------
-- Create staging table to load the CSV
DROP TABLE IF EXISTS staging_import;
CREATE TABLE staging_import (
	cell_name VARCHAR(255),
    `source` VARCHAR(255),
    weight DECIMAL(5,2), 
    gene_symbol VARCHAR(255),
    ensembl_id VARCHAR(255),
    gene_full_name VARCHAR(255),
    cell_id VARCHAR(255)
);

-- Here we have to import manually the csv before proceeding with the next steps
-- In order to do it: manually select staging_import in left panel --> 
-- select: Table Data Import Wizard --> import the csv file

-- -----------------------------------------------------
-- PART TWO --
-- -----------------------------------------------------
-- Fill genes table
INSERT IGNORE INTO genes (gene_ensembl_id, gene_symbol, gene_full_name) 
SELECT DISTINCT ensembl_id, gene_symbol, gene_full_name  -- Distinct to fill only one time each
FROM staging_import
WHERE ensembl_id IS NOT NULL;

-- Fill cells table
INSERT IGNORE INTO cell_types (cell_type_id, cell_name)
SELECT DISTINCT cell_id, cell_name  -- Distinct to fill only one time each
FROM staging_import
WHERE cell_id IS NOT NULL;

-- Fill markers table
INSERT IGNORE INTO markers (gene_ensembl_id, cell_type_id, weight, `source`)
SELECT ensembl_id, cell_id, weight, `source`  -- Now we don't need distinct, we want all the relations
FROM staging_import
WHERE ensembl_id IS NOT NULL AND cell_id IS NOT NULL;

-- Remove staging table
DROP TABLE IF EXISTS staging_import;
