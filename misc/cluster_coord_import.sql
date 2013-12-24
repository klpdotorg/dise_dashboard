CREATE OR REPLACE FUNCTION coord_import_cluster() RETURNS void AS
$BODY$
DECLARE
    years integer[] := array[1011, 1112, 1213];
    year integer;
    table_name varchar(50);
    basic_table_name varchar(50);
BEGIN
    FOREACH year IN ARRAY years
    LOOP
        -- can do some processing here
        table_name := 'dise_' || year || '_cluster_aggregations';
        basic_table_name := 'dise_' || year || '_basic_data';

        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD COLUMN coord geometry';

        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD CONSTRAINT enforce_dims_coord CHECK (st_ndims(coord) = 2)';
        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD CONSTRAINT enforce_geotype_coord CHECK (geometrytype(coord) = ''POINT''::text OR coord IS NULL)';
        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD CONSTRAINT enforce_srid_coord CHECK (st_srid(coord) = 4326)';

        EXECUTE 'UPDATE ' || table_name || '
        SET coord=t.coord
        FROM
            dblink(''host=localhost dbname=klpwww_ver4 user=klp password=pg2klp''::text,
                ''select * from vw_boundary_coord_wname''::text)
                    t(id integer, name character varying(50), type character varying(20), coord geometry)
        WHERE t.type=''Cluster'' AND cluster_name ~* t.name';

    END LOOP;
    RETURN;
END
$BODY$
LANGUAGE plpgsql;

SELECT * FROM coord_import_cluster();
