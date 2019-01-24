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
        DiseBasicData = get_models(session='16-17', what='school')

        school = {}

        if row.get('AC_YEAR'):
            school['academic_year'] = row.get('AC_YEAR')
        if row.get('SCHOOL_CODE'):
        	school['school_code'] = row.get('SCHOOL_CODE')
       	if row.get('SCHOOL_NAME'):
            school['school_name'] = row.get('SCHOOL_NAME')
        if row.get('HABNAME'):
        	school['habitat_name'] = row.get('HABNAME')
        if row.get('VILLAGE_NAME'):
            school['village_name'] = row.get('VILLAGE_NAME')
        if row.get('PANCHAYAT_CODE'):
        	school['panchayat_code'] = row.get('PANCHAYAT_CODE')
       	if row.get('PANCHAYAT'):
            school['panchayat_name'] = row.get('PANCHAYAT')
       	if row.get('MUNNAME'):
            school['muncipality_name'] = row.get('MUNNAME')
        if row.get('CITYNAME'):
        	school['city_name'] = row.get('CITYNAME')
       	if row.get('CLUSTER_NAME'):
            school['cluster_name'] = row.get('CLUSTER_NAME').upper()
        if row.get('BLOCK_NAME'):
        	school['block_name'] = row.get('BLOCK_NAME').upper()
        if row.get('DISTNAME'):
            school['district'] = row.get('DISTNAME').upper()
        if row.get('STATE_NAME'):
        	school['state_name'] = row.get('STATE_NAME')
       	if row.get('PINCODE'):
            school['pincode'] = row.get('PINCODE')
        if row.get('LatitudeDeg'):
        	school['latitude_degrees'] = row.get('LatitudeDeg')
        if row.get('LatitudeMin'):
        	school['latitude_minutes'] = row.get('LatitudeMin')
        if row.get('LatitudeSec'):
        	school['latitude_seconds'] = row.get('LatitudeSec')
        if row.get('LongitudeDeg'):
        	school['longitude_degrees'] = row.get('LongitudeDeg')
        if row.get('LongitudeMin'):
        	school['longitude_minutes'] = row.get('LongitudeMin')
        if row.get('LongitudeSec'):
        	school['longitude_seconds'] = row.get('LongitudeSec')

        self.rows_to_create.append(DiseBasicData(**school))

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
                #cursor.execute('DROP TABLE IF EXISTS "%s"' % table_name)
                #print 'Table dropped'
                #print cursor.description
                cursor.execute("CREATE TABLE IF NOT EXISTS %s as SELECT * FROM dise_1314_basic_data WITH NO DATA" % table_name)

                #print 'Table %s created' % table_name
            except Exception, e:
                raise e

        for basic_data in args:
            full_path = os.path.join(settings.PROJECT_ROOT, basic_data)

            with open(full_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='|')
                count = 0
                totalcount = 0

                print 'processing schools'
                for row in reader:
                    self.process_row(row)
                    count += 1
                    totalcount += 1
                    if count % 1000 == 0:
                        print count,
                        print "creating 1000 schools at a time"
                        DiseBasicData = get_models(session='%s-%s' % (from_year[-2:], to_year[-2:]), what='school')
                        DiseBasicData.objects.bulk_create(self.rows_to_create)
                        self.rows_to_create = []
                        count = 0

                print 'creating remaining schools :'+str(count)
                DiseBasicData = get_models(session='%s-%s' % (from_year[-2:], to_year[-2:]), what='school')
                DiseBasicData.objects.bulk_create(self.rows_to_create)
                print str(totalcount)+" schools created"
