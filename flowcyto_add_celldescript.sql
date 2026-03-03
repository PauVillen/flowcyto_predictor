USE flowcyto_db;

SET SQL_SAFE_UPDATES = 0;

UPDATE cell_types ct
JOIN staging_descriptions sd 
  ON TRIM(REPLACE(ct.cell_name, '"', '')) = TRIM(REPLACE(sd.CellType, '"', ''))
SET ct.cell_description = TRIM(REPLACE(sd.Description, '"', ''));

SET SQL_SAFE_UPDATES = 1;

SELECT cell_name, cell_description FROM cell_types LIMIT 5;