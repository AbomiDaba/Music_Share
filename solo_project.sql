-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema solo_project
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `solo_project` ;

-- -----------------------------------------------------
-- Schema solo_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `solo_project` DEFAULT CHARACTER SET utf8 ;
USE `solo_project` ;

-- -----------------------------------------------------
-- Table `solo_project`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `solo_project`.`users` ;

CREATE TABLE IF NOT EXISTS `solo_project`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `solo_project`.`songs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `solo_project`.`songs` ;

CREATE TABLE IF NOT EXISTS `solo_project`.`songs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `artist` VARCHAR(255) NULL,
  `name` VARCHAR(255) NULL,
  `genre` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_songs_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_songs_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `solo_project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `solo_project`.`likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `solo_project`.`likes` ;

CREATE TABLE IF NOT EXISTS `solo_project`.`likes` (
  `song_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  INDEX `fk_songs_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_songs_has_users_songs_idx` (`song_id` ASC) VISIBLE,
  CONSTRAINT `fk_songs_has_users_songs`
    FOREIGN KEY (`song_id`)
    REFERENCES `solo_project`.`songs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_songs_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `solo_project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
