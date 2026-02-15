-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema flowcyto_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `flowcyto_db` ;

-- -----------------------------------------------------
-- Schema flowcyto_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `flowcyto_db` DEFAULT CHARACTER SET utf8 ;
USE `flowcyto_db` ;

-- -----------------------------------------------------
-- Table `flowcyto_db`.`genes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flowcyto_db`.`genes` ;

CREATE TABLE IF NOT EXISTS `flowcyto_db`.`genes` (
  `gene_ensembl_id` VARCHAR(45) NOT NULL,
  `gene_symbol` VARCHAR(20) NULL,
  `gene_full_name` VARCHAR(150) NULL,
  PRIMARY KEY (`gene_ensembl_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flowcyto_db`.`cell_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flowcyto_db`.`cell_types` ;

CREATE TABLE IF NOT EXISTS `flowcyto_db`.`cell_types` (
  `cell_type_id` VARCHAR(45) NOT NULL,
  `cell_name` VARCHAR(100) NULL,
  `cell_description` TEXT NULL,
  PRIMARY KEY (`cell_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flowcyto_db`.`markers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flowcyto_db`.`markers` ;

CREATE TABLE IF NOT EXISTS `flowcyto_db`.`markers` (
  `gene_ensembl_id` VARCHAR(45) NOT NULL,
  `cell_type_id` VARCHAR(45) NOT NULL,
  `weight` DECIMAL(5,2) NULL,
  `source` VARCHAR(100) NULL,
  PRIMARY KEY (`gene_ensembl_id`, `cell_type_id`),
  INDEX `fk_markers_users_idx` (`gene_ensembl_id` ASC) VISIBLE,
  INDEX `fk_markers_cell_types1_idx` (`cell_type_id` ASC) VISIBLE,
  CONSTRAINT `fk_markers_users`
    FOREIGN KEY (`gene_ensembl_id`)
    REFERENCES `flowcyto_db`.`genes` (`gene_ensembl_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_markers_cell_types1`
    FOREIGN KEY (`cell_type_id`)
    REFERENCES `flowcyto_db`.`cell_types` (`cell_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flowcyto_db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flowcyto_db`.`users` ;

CREATE TABLE IF NOT EXISTS `flowcyto_db`.`users` (
  `user_email` VARCHAR(95) NOT NULL,
  `user_password` VARCHAR(255) NULL,
  PRIMARY KEY (`user_email`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`predictions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flowcyto_db`.`predictions` ;

CREATE TABLE IF NOT EXISTS `flowcyto_db`.`predictions` (
  `prediction_id` INT NOT NULL AUTO_INCREMENT,
  `input_genes` TEXT NULL,
  `request_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `user_email` VARCHAR(95) NOT NULL,
  PRIMARY KEY (`prediction_id`),
  INDEX `fk_predictions_users1_idx` (`user_email` ASC) VISIBLE,
  CONSTRAINT `fk_predictions_users1`
    FOREIGN KEY (`user_email`)
    REFERENCES `flowcyto_db`.`users` (`user_email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `flowcyto_db`.`results`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flowcyto_db`.`results` ;

CREATE TABLE IF NOT EXISTS `flowcyto_db`.`results` (
  `prediction_id` INT NOT NULL,
  `cell_type_id` VARCHAR(45) NOT NULL,
  `score` DECIMAL(5,2) NULL,
  `probability_pct` DECIMAL(5,2) NULL,
  INDEX `fk_results_predictions1_idx` (`prediction_id` ASC) VISIBLE,
  INDEX `fk_results_cell_types1_idx` (`cell_type_id` ASC) VISIBLE,
  PRIMARY KEY (`prediction_id`, `cell_type_id`),
  CONSTRAINT `fk_results_predictions1`
    FOREIGN KEY (`prediction_id`)
    REFERENCES `flowcyto_db`.`predictions` (`prediction_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_results_cell_types1`
    FOREIGN KEY (`cell_type_id`)
    REFERENCES `flowcyto_db`.`cell_types` (`cell_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
