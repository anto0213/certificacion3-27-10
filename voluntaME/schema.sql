-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema voluntame
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema voluntame
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `voluntame` DEFAULT CHARACTER SET utf8 ;
USE `voluntame` ;

-- -----------------------------------------------------
-- Table `voluntame`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `voluntame`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `contraseña` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `voluntame`.`misiones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `voluntame`.`misiones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `fecha` VARCHAR(45) NULL,
  `voluntarios_necesarios` VARCHAR(45) NULL,
  `descripcion` VARCHAR(45) NULL,
  `usuarios_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`, `usuarios_id`),
  INDEX `fk_misiones_usuarios_idx` (`usuarios_id` ASC) VISIBLE,
  CONSTRAINT `fk_misiones_usuarios`
    FOREIGN KEY (`usuarios_id`)
    REFERENCES `voluntame`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `voluntame`.`table1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `voluntame`.`table1` (
  `misiones_id` INT NOT NULL,
  `misiones_usuarios_id` INT NOT NULL,
  `usuarios_id` INT NOT NULL,
  INDEX `fk_table1_misiones1_idx` (`misiones_id` ASC, `misiones_usuarios_id` ASC) VISIBLE,
  INDEX `fk_table1_usuarios1_idx` (`usuarios_id` ASC) VISIBLE,
  CONSTRAINT `fk_table1_misiones1`
    FOREIGN KEY (`misiones_id` , `misiones_usuarios_id`)
    REFERENCES `voluntame`.`misiones` (`id` , `usuarios_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table1_usuarios1`
    FOREIGN KEY (`usuarios_id`)
    REFERENCES `voluntame`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
