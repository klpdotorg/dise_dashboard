UPDATE :table
SET centroid = st_transform(centroid, 4326);


UPDATE :table
SET centroid=st_setsrid(ssa.centroid, 4326)
FROM dblink('host=localhost dbname=ssa user=klp'::text, 'SELECT code, name, centroid FROM schools') AS ssa(code bigint, name character varying(150), centroid geometry)
WHERE :table.school_code = ssa.code;


UPDATE :table
SET assembly_name = ac.ac_name
FROM assembly AS ac
WHERE centroid IS NOT NULL
    AND st_within(centroid, ac.the_geom);


UPDATE :table
SET parliament_name = pc.const_name
FROM parliament AS pc
WHERE centroid IS NOT NULL
    AND st_within(centroid, pc.the_geom);


UPDATE :table
SET pincode = postal.pincode::integer
FROM postal
WHERE st_within(centroid, st_setsrid(postal.wkb_geometry, 4326))
    AND :table.centroid IS NOT NULL
    AND :table.pincode IS NULL;

