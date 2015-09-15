import os
import csv
import xlrd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from schools.models import get_models

class Command(BaseCommand):
    """
    e.g.
    (venv)$ python manage.py import_total_enrolment_1213 "/project/data/DISE%202012-2013 v2/Enrolment/file.csv" > misc/import/import_1213_total_enrolment.sql
    """
    args = '<filename>'
    help = 'Imports 2012-13 total_enrolment file'

    def handle(self, *args, **options):
        if len(args) >= 1:
            filename = args[0]
            SchoolModel = get_models('12-13', 'school')

            with open(filename, 'rb') as fp:
                reader = csv.reader(fp, delimiter=',', quotechar='"')
                first_row = reader.next()
                columns = ['school_code', 'acyear', 'class1_total_enr_boys', 'class2_total_enr_boys', 'class3_total_enr_boys', 'class4_total_enr_boys', 'class5_total_enr_boys', 'class6_total_enr_boys', 'class7_total_enr_boys', 'class8_total_enr_boys', 'class1_total_enr_girls', 'class2_total_enr_girls', 'class3_total_enr_girls', 'class4_total_enr_girls', 'class5_total_enr_girls', 'class6_total_enr_girls', 'class7_total_enr_girls', 'class8_total_enr_girls', 'class1_sc_enr_boys', 'class2_sc_enr_boys', 'class3_sc_enr_boys', 'class4_sc_enr_boys', 'class5_sc_enr_boys', 'class6_sc_enr_boys', 'class7_sc_enr_boys', 'class8_sc_enr_boys', 'class1_sc_enr_girls', 'class2_sc_enr_girls', 'class3_sc_enr_girls', 'class4_sc_enr_girls', 'class5_sc_enr_girls', 'class6_sc_enr_girls', 'class7_sc_enr_girls', 'class8_sc_enr_girls', 'class1_st_enr_boys', 'class2_st_enr_boys', 'class3_st_enr_boys', 'class4_st_enr_boys', 'class5_st_enr_boys', 'class6_st_enr_boys', 'class7_st_enr_boys', 'class8_st_enr_boys', 'class1_st_enr_girls', 'class2_st_enr_girls', 'class3_st_enr_girls', 'class4_st_enr_girls', 'class5_st_enr_girls', 'class6_st_enr_girls', 'class7_st_enr_girls', 'class8_st_enr_girls', 'class1_obc_enr_boys', 'class2_obc_enr_boys', 'class3_obc_enr_boys', 'class4_obc_enr_boys', 'class5_obc_enr_boys', 'class6_obc_enr_boys', 'class7_obc_enr_boys', 'class8_obc_enr_boys', 'class1_obc_enr_girls', 'class2_obc_enr_girls', 'class3_obc_enr_girls', 'class4_obc_enr_girls', 'class5_obc_enr_girls', 'class6_obc_enr_girls', 'class7_obc_enr_girls', 'class8_obc_enr_girls', 'disabled_c1_boys', 'disabled_c2_boys', 'disabled_c3_boys', 'disabled_c4_boys', 'disabled_c5_boys', 'disabled_c6_boys', 'disabled_c7_boys', 'disabled_c8_boys', 'disabled_c1_girls', 'disabled_c2_girls', 'disabled_c3_girls', 'disabled_c4_girls', 'disabled_c5_girls', 'disabled_c6_girls', 'disabled_c7_girls', 'disabled_c8_girls', 'repeaters_c1_boys', 'repeaters_c2_boys', 'repeaters_c3_boys', 'repeaters_c4_boys', 'repeaters_c5_boys', 'repeaters_c6_boys', 'repeaters_c7_boys', 'repeaters_c8_boys', 'repeaters_c1_girls', 'repeaters_c2_girls', 'repeaters_c3_girls', 'repeaters_c4_girls', 'repeaters_c5_girls', 'repeaters_c6_girls', 'repeaters_c7_girls', 'repeaters_c8_girls', 'c5_appeared_boys', 'c5_appeared_girls', 'c5_passed_boys', 'c5_passed_girls', 'c5_passed_with_more_than_60_boys', 'c5_passed_with_more_than_60_girls', 'c7_appeared_boys', 'c7_appeared_girls', 'c7_passed_boys', 'c7_passed_girls', 'c7_passed_with_more_than_60_boys', 'c7_passed_with_more_than_60_girls']

                query = "ALTER TABLE {} \n".format(SchoolModel._meta.db_table)
                for c in columns[2:18]:
                    q = query + " ADD COLUMN {} integer;".format(c)
                    self.stdout.write(q)
                q = query + " ADD COLUMN total_boys integer;"
                self.stdout.write(q)
                q = query + " ADD COLUMN total_girls integer;"
                self.stdout.write(q)

                for row in reader:
                    school_code = int(row[columns.index('school_code')])

                    query = "UPDATE {} SET \n".format(SchoolModel._meta.db_table)
                    for c in columns[2:18]:
                        query += "\t{}='{}',\n".format(c, int(row[columns.index(c)]))
                    query += '\ttotal_boys = ({}),\n'.format('+'.join(columns[2:10]))
                    query += '\ttotal_girls = ({}),\n'.format('+'.join(columns[10:18]))
                    query = query.rstrip(',\n')
                    query += "\nWHERE school_code='{}';".format(school_code)
                    self.stdout.write(query)
