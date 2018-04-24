CREATE OR REPLACE FUNCTION aggregate_block() RETURNS void AS
$BODY$
DECLARE
    years integer[] := array[1011, 1112, 1213, 1314, 1415, 1516, 1617];
    year integer;
    table_name varchar(50);
    basic_table_name varchar(50);
BEGIN
    FOREACH year IN ARRAY years
    LOOP
        -- can do some processing here
        table_name := 'dise_' || year || '_block_aggregations';
        basic_table_name := 'dise_' || year || '_basic_data';
        EXECUTE 'DROP TABLE IF EXISTS ' || table_name;

        EXECUTE 'CREATE TABLE ' || table_name || ' AS
        SELECT block_name, district, state_name,
            getslug(concat(district, '' '', block_name)) as slug,

            Count(school_code) AS sum_schools,
            Sum(CASE WHEN rural_urban = 1 THEN 1 ELSE 0 END) AS sum_rural_schools,
            Sum(CASE WHEN sch_management IN (1, 7) THEN 1 ELSE 0 END) AS sum_govt_schools,

            Avg(distance_brc) AS avg_distance_brc,
            Avg(distance_crc) AS avg_distance_crc,

            Sum(CASE WHEN pre_pry_yn = 1 THEN 1 ELSE 0 END) AS sum_pre_primary_schools,
            Sum(CASE WHEN residential_sch_yn = 1 THEN 1 ELSE 0 END) AS sum_residential_schools,

            Sum(pre_pry_students) AS sum_pre_primary_students,
            Avg(pre_pry_students) AS avg_pre_primary_students,

            Sum(CASE WHEN shift_school_yn = 1 THEN 1 ELSE 0 END) AS sum_shift_schools,

            Sum(no_of_working_days) AS sum_no_of_working_days,
            Avg(no_of_working_days) AS avg_no_of_working_days,

            Sum(no_of_acad_inspection) AS sum_no_of_acad_inspection,
            Avg(no_of_acad_inspection) AS avg_no_of_acad_inspection,

            Sum(visits_by_brc) AS sum_visits_by_brc,
            Avg(visits_by_brc) AS avg_visits_by_brc,

            Sum(visits_by_crc) AS sum_visits_by_crc,
            Avg(visits_by_crc) AS avg_visits_by_crc,

            Sum(school_dev_grant_recd) AS sum_school_dev_grant_recd,
            Avg(school_dev_grant_recd) AS avg_school_dev_grant_recd,

            Sum(school_dev_grant_expnd) AS sum_school_dev_grant_expnd,
            Avg(school_dev_grant_expnd) AS avg_school_dev_grant_expnd,

            Sum(tlm_grant_recd) AS sum_tlm_grant_recd,
            Avg(tlm_grant_recd) AS avg_tlm_grant_recd,

            Sum(tlm_grant_expnd) AS sum_tlm_grant_expnd,
            Avg(tlm_grant_expnd) AS avg_tlm_grant_expnd,

            Sum(funds_from_students_recd) AS sum_funds_from_students_recd,
            Avg(funds_from_students_recd) AS avg_funds_from_students_recd,

            Sum(funds_from_students_expnd) AS sum_funds_from_students_expnd,
            Avg(funds_from_students_expnd) AS avg_funds_from_students_expnd,

            Sum(school_maintain_grant_recd) AS sum_school_maintain_grant_recd,
            Avg(school_maintain_grant_recd) AS avg_school_maintain_grant_recd,

            Sum(school_maintain_grant_expnd) AS sum_school_maintain_grant_expnd,
            Avg(school_maintain_grant_expnd) AS avg_school_maintain_grant_expnd,

            Sum(tot_clrooms) AS sum_tot_clrooms,
            Avg(tot_clrooms) AS avg_tot_clrooms,

            Sum(classrooms_in_good_condition) as sum_classrooms_in_good_condition,
            Avg(classrooms_in_good_condition) as avg_classrooms_in_good_condition,
            Sum(CASE WHEN classrooms_in_good_condition > 0 THEN 1 ELSE 0 END) AS sum_has_classrooms_in_good_condition,

            Sum(classrooms_require_major_repair) as sum_classrooms_require_major_repair,
            Avg(classrooms_require_major_repair) as avg_classrooms_require_major_repair,

            Sum(classrooms_require_minor_repair) as sum_classrooms_require_minor_repair,
            Avg(classrooms_require_minor_repair) as avg_classrooms_require_minor_repair,

            Sum(other_rooms_in_good_cond) as sum_other_rooms_in_good_cond,
            Avg(other_rooms_in_good_cond) as avg_other_rooms_in_good_cond,

            Sum(other_rooms_need_major_rep) as sum_other_rooms_need_major_rep,
            Avg(other_rooms_need_major_rep) as avg_other_rooms_need_major_rep,

            Sum(other_rooms_need_minor_rep) as sum_other_rooms_need_minor_rep,
            Avg(other_rooms_need_minor_rep) as avg_other_rooms_need_minor_rep,

            Sum(toilet_common) as sum_toilet_common,
            Avg(toilet_common) as avg_toilet_common,

            Sum(toilet_boys) as sum_toilet_boys,
            Avg(toilet_boys) as avg_toilet_boys,

            Sum(toilet_girls) as sum_toilet_girls,
            Avg(toilet_girls) as avg_toilet_girls,

            Sum(kitchen_devices_grant) as sum_kitchen_devices_grant,
            Avg(kitchen_devices_grant) as avg_kitchen_devices_grant,

            Sum(CASE WHEN status_of_mdm IN (2, 3) THEN 1 ELSE 0 END) as sum_has_mdm,

            Sum(CASE WHEN computer_aided_learnin_lab = 1 THEN 1 ELSE 0 END) as sum_has_cal_lab,

            Sum(CASE WHEN separate_room_for_headmaster = 1 THEN 1 ELSE 0 END) as sum_has_separate_room_for_headmaster,

            Sum(CASE WHEN electricity = 1 THEN 1 ELSE 0 END) AS sum_has_electricity,

            Sum(CASE WHEN boundary_wall = 1 THEN 1 ELSE 0 END) AS sum_has_boundary_wall,

            Sum(CASE WHEN library_yn = 1 THEN 1 ELSE 0 END) AS sum_has_library,

            Sum(books_in_library) as sum_books_in_library,
            Avg(books_in_library) as avg_books_in_library,

            Sum(CASE WHEN playground = 1 THEN 1 ELSE 0 END) AS sum_has_playground,

            Sum(CASE WHEN blackboard = 1 THEN 1 ELSE 0 END) AS sum_has_blackboard,

            Sum(CASE WHEN drinking_water = 1 THEN 1 ELSE 0 END) AS sum_has_drinking_water,

            Sum(CASE WHEN medical_checkup = 1 THEN 1 ELSE 0 END) AS sum_has_medical_checkup,

            Sum(CASE WHEN ramps = 1 THEN 1 ELSE 0 END) AS sum_has_ramps,

            Sum(CASE WHEN no_of_computers > 0 THEN 1 ELSE 0 END) AS sum_has_computer,
            Sum(CASE WHEN (COALESCE(toilet_common, 0) + toilet_boys + toilet_girls) > 0 THEN 1 ELSE 0 END) AS sum_has_toilet,
            Sum(CASE WHEN COALESCE(toilet_girls, 0) > 0 THEN 1 ELSE 0 END) AS sum_has_girls_toilet,

            Sum(no_of_computers) as sum_no_of_computers,
            Avg(no_of_computers) as avg_no_of_computers,

            Sum(male_tch) as sum_male_tch,
            Avg(male_tch) as avg_male_tch,

            Sum(female_tch) as sum_female_tch,
            Avg(female_tch) as avg_female_tch,

            Sum(noresp_tch) as sum_noresp_tch,
            Avg(noresp_tch) as avg_noresp_tch,

            Sum(head_teacher) as sum_head_teacher,
            Avg(head_teacher) as avg_head_teacher,

            Sum(graduate_teachers) as sum_graduate_teachers,
            Avg(graduate_teachers) as avg_graduate_teachers,

            Sum(tch_with_professional_qualification) as sum_tch_with_professional_qualification,
            Avg(tch_with_professional_qualification) as avg_tch_with_professional_qualification,

            Sum(days_involved_in_non_tch_assgn) as sum_days_involved_in_non_tch_assgn,
            Avg(days_involved_in_non_tch_assgn) as avg_days_involved_in_non_tch_assgn,

            Sum(teachers_involved_in_non_tch_assgn) as sum_teachers_involved_in_non_tch_assgn,
            Avg(teachers_involved_in_non_tch_assgn) as avg_teachers_involved_in_non_tch_assgn,

            Sum(total_boys) as sum_boys,
            Avg(total_boys) as avg_boys,
            Sum(total_girls) as sum_girls,
            Avg(total_girls) as avg_girls

        FROM ' || basic_table_name || '
        GROUP BY block_name, district, state_name
        ORDER BY block_name, district, state_name';

        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD PRIMARY KEY (slug)';

        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD COLUMN centroid geometry';

        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD CONSTRAINT enforce_dims_centroid CHECK (st_ndims(centroid) = 2)';
        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD CONSTRAINT enforce_geotype_centroid CHECK (geometrytype(centroid) = ''POINT''::text OR centroid IS NULL)';
        EXECUTE 'ALTER TABLE ' || table_name || '
            ADD CONSTRAINT enforce_srid_centroid CHECK (st_srid(centroid) = 4326)';

        EXECUTE 'UPDATE ' || table_name || '
            SET centroid=block_centroid.centroid
            FROM (SELECT t1.block_name, t1.district, ST_Centroid(ST_Collect(t2.centroid)) as centroid
                    FROM ' || table_name || ' AS t1,
                    ' || basic_table_name || ' AS t2
                WHERE t2.block_name=t1.block_name AND
                    t2.district=t1.district
                GROUP BY t1.block_name, t1.district
                ORDER BY t1.block_name, t1.district) as block_centroid
            WHERE ' || table_name || '.block_name=block_centroid.block_name AND
                ' || table_name || '.district=block_centroid.district';


    END LOOP;
    RETURN;
END
$BODY$
LANGUAGE plpgsql;

SELECT * FROM aggregate_block();
