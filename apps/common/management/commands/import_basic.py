import os
import csv
from optparse import make_option

from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from schools.models import get_models
from datetime import datetime


class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports Basic data files'
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest="year",
            help='import for specific academic year'
        ),
    )
    rows_to_create = []

    def process_row(self, row, year=None):
        # DISTNAME,SCHOOL_CODE,SCHOOL_NAME,BLOCK_NAME,CLUSTER_NAME,VILLAGE_NAME,PINCODE
        DiseBasicData = get_models(session='15-16', what='school')

        school = DiseBasicData(
            school_code=row['SCHOOL_CODE'],
            district=row['DISTNAME'],
            school_name=row['SCHOOL_NAME'],
            block_name=row['BLOCK_NAME'],
            cluster_name=row['CLUSTER_NAME'],
            village_name=row['VILLAGE_NAME'],
            pincode=row['PINCODE'],
        )
        self.rows_to_create.append(school)

    def handle(self, *args, **options):
        print "="*80
        print datetime.now()
        print "="*80
        if 'year' in options:
            from_year, to_year = options.get('year').split('-')

            table_name = 'dise_{from_year}{to_year}_basic_data'.format(
                from_year=from_year[-2:],
                to_year=to_year[-2:],
            )

            # create table if it doesn't exist
            try:
                cursor = connection.cursor()
                cursor.execute('DROP TABLE IF EXISTS "%s"' % table_name)
                print 'Table dropped'
                cursor.execute("CREATE TABLE %s as SELECT * FROM dise_1314_basic_data WITH NO DATA" % table_name)
                print 'Table %s created' % table_name
            except Exception, e:
                raise e

        for basic_data in args:
            full_path = os.path.join(settings.PROJECT_ROOT, basic_data)

            with open(full_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0

                print 'processing schools'
                for row in reader:
                    self.process_row(row)
                    count += 1
                    if count % 100 == 0:
                        print count,

                print 'creating schools'
                DiseBasicData = get_models(session='%s-%s' % (from_year[-2:], to_year[-2:]), what='school')
                DiseBasicData.objects.bulk_create(self.rows_to_create)
