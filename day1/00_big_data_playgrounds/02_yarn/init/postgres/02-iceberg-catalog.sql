-- Backing DB for the Iceberg REST catalog service (tabulario/iceberg-rest).
-- The REST catalog uses Iceberg's JdbcCatalog under the hood, which
-- creates its own iceberg_tables / iceberg_namespace_properties tables
-- in this DB on first start.
CREATE DATABASE iceberg_catalog OWNER hive;
