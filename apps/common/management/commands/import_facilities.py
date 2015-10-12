import os
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from schools.models import get_models


class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports Facility data files'
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest="year",
            help='import for specific academic year'
        ),
    )

    def process_row(self, row, basic_data_model):
        # SCHCD,BLDSTATUS,CLROOMS,CLGOOD,CLMAJOR,CLMINOR,TOILETB,TOILET_G,
        # MEALSINSCH,CAL_YN,HMROOM_YN,ELECTRIC_YN,BNDRYWALL,LIBRARY_YN,
        # PGROUND_YN,BOOKINLIB,WATER,MEDCHK_YN,RAMPS_YN,COMPUTER

        DiseBasicData = basic_data_model

        school = {}

        if row.get('BLDSTATUS'):
            school['building_status'] = row.get('BLDSTATUS')
        if row.get('CLROOMS'):
            school['tot_clrooms'] = row.get('CLROOMS')
        if row.get('CLGOOD'):
            school['classrooms_in_good_condition'] = row.get('CLGOOD')
        if row.get('CLMAJOR'):
            school['classrooms_require_major_repair'] = row.get('CLMAJOR')
        if row.get('CLMINOR'):
            school['classrooms_require_minor_repair'] = row.get('CLMINOR')
        if row.get('TOILETB'):
            school['toilet_boys'] = row.get('TOILETB')
        if row.get('TOILET_G'):
            school['toilet_girls'] = row.get('TOILET_G')
        if row.get('MEALSINSCH'):
            school['status_of_mdm'] = row.get('MEALSINSCH')
        if row.get('CAL_YN'):
            school['computer_aided_learnin_lab'] = row.get('CAL_YN')
        if row.get('HMROOM_YN'):
            school['separate_room_for_headmaster'] = row.get('HMROOM_YN')
        if row.get('ELECTRIC_YN'):
            school['electricity'] = row.get('ELECTRIC_YN')
        if row.get('BNDRYWALL'):
            school['boundary_wall'] = row.get('BNDRYWALL')
        if row.get('LIBRARY_YN'):
            school['library_yn'] = row.get('LIBRARY_YN')
        if row.get('PGROUND_YN'):
            school['playground'] = row.get('PGROUND_YN')
        if row.get('BOOKINLIB'):
            school['books_in_library'] = row.get('BOOKINLIB')
        if row.get('WATER'):
            school['drinking_water'] = row.get('WATER')
        if row.get('MEDCHK_YN'):
            school['medical_checkup'] = row.get('MEDCHK_YN')
        if row.get('RAMPS_YN'):
            school['ramps'] = row.get('RAMPS_YN')
        if row.get('COMPUTER'):
            school['no_of_computers'] = row.get('COMPUTER')

        DiseBasicData.objects.filter(school_code=row.get('SCHCD')).update(**school)

    def handle(self, *args, **options):
        if 'year' in options:
            from_year, to_year = options.get('year').split('-')

        for facility_data in args:
            full_path = os.path.join(settings.PROJECT_ROOT, facility_data)

            with open(full_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0

                print 'processing schools'
                DiseBasicData = get_models(session='%s-%s' % (from_year[-2:], to_year[-2:]), what='school')

                for row in reader:
                    self.process_row(row, DiseBasicData)
                    count += 1
                    if count % 100 == 0:
                        print count,
