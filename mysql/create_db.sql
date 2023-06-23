CREATE DATABASE IF NOT EXISTS `warehouse_db`;
CREATE DATABASE IF NOT EXISTS `sales_db`;
CREATE DATABASE IF NOT EXISTS `accounting_db`;

CREATE USER 'brewery'@'localhost' IDENTIFIED BY 'brewery';
GRANT ALL ON *.* TO 'brewery';
