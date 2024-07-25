-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema superstore
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema superstore
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `superstore` DEFAULT CHARACTER SET utf8 ;
USE `superstore` ;

-- -----------------------------------------------------
-- Table `superstore`.`shipping`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`shipping` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `mode_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `superstore`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`customers` (
  `id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `superstore`.`priorities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`priorities` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `superstore`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`orders` (
  `id` VARCHAR(45) NOT NULL,
  `order_date` DATE NOT NULL,
  `ship_date` DATE NULL,
  `shipping_id` INT NOT NULL,
  `customer_id` VARCHAR(45) NOT NULL,
  `priority_id` INT NOT NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_orders_shipping_idx` (`shipping_id` ASC) VISIBLE,
  INDEX `fk_orders_customers1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_orders_priorities1_idx` (`priority_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_shipping`
    FOREIGN KEY (`shipping_id`)
    REFERENCES `superstore`.`shipping` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `superstore`.`customers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_priorities1`
    FOREIGN KEY (`priority_id`)
    REFERENCES `superstore`.`priorities` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `superstore`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `superstore`.`subcategories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`subcategories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `superstore`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`products` (
  `id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `category_id` INT NOT NULL,
  `subcategory_id` INT NOT NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_products_categories1_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_products_subcategories1_idx` (`subcategory_id` ASC) VISIBLE,
  CONSTRAINT `fk_products_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `superstore`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_products_subcategories1`
    FOREIGN KEY (`subcategory_id`)
    REFERENCES `superstore`.`subcategories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `superstore`.`order_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `superstore`.`order_items` (
  `id` INT NOT NULL,
  `product_id` VARCHAR(45) NOT NULL,
  `order_id` VARCHAR(45) NOT NULL,
  `sales` FLOAT NULL,
  `quantity` INT NULL,
  `discount` FLOAT NULL,
  `profit` FLOAT NULL,
  `shipping_cost` FLOAT NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_orders_copy1_products1_idx` (`product_id` ASC) VISIBLE,
  INDEX `fk_order_items_orders1_idx` (`order_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_copy1_products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `superstore`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_items_orders1`
    FOREIGN KEY (`order_id`)
    REFERENCES `superstore`.`orders` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
