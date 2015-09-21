import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from schools.models import get_models

class Command(BaseCommand):
    """
    e.g.
    (venv)$ python manage.py import_total_enrolment 11-12 /vagrant_data/project/data/Dise_2011_12/DISE_TotalEnrolment_Data_26-09-2012.csv > misc/import/import_1112_total_enrolment.sql
    """
    args = '<acyear> <filename>'
    help = 'Imports total_enrolment file'

    def handle(self, *args, **options):
        if len(args) >= 2:
            acyear = args[0]
            filename = args[1]
            SchoolModel = get_models(acyear, 'school')

            with open(filename, 'rb') as fp:
                reader = csv.reader(fp, delimiter=',', quotechar='"')
                first_row = reader.next()
                columns = ['school_code', 'acyear', 'class1_total_enr_boys', 'class2_total_enr_boys', 'class3_total_enr_boys', 'class4_total_enr_boys', 'class5_total_enr_boys', 'class6_total_enr_boys', 'class7_total_enr_boys', 'class8_total_enr_boys', 'class1_total_enr_girls', 'class2_total_enr_girls', 'class3_total_enr_girls', 'class4_total_enr_girls', 'class5_total_enr_girls', 'class6_total_enr_girls', 'class7_total_enr_girls', 'class8_total_enr_girls']

                query = "ALTER TABLE {} \n".format(SchoolModel._meta.db_table)
                for c in columns[2:]:
                    q = query + " ADD COLUMN {} integer;".format(c)
                    self.stdout.write(q)
                q = query + " ADD COLUMN total_boys integer;"
                self.stdout.write(q)
                q = query + " ADD COLUMN total_girls integer;"
                self.stdout.write(q)

                for row in reader:
                    school_code = int(row[columns.index('school_code')])

                    query = "UPDATE {} SET \n".format(SchoolModel._meta.db_table)
                    for c in columns[2:]:
                        query += "\t{}='{}',\n".format(c, int(row[columns.index(c)]))
                    query += '\ttotal_boys = ({}),\n'.format('+'.join(columns[2:10]))
                    query += '\ttotal_girls = ({}),\n'.format('+'.join(columns[10:]))
                    query = query.rstrip(',\n')
                    query += "\nWHERE school_code='{}';".format(school_code)
                    self.stdout.write(query)
