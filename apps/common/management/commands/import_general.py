import os
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from schools.models import get_models


class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports General data files'
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest="year",
            help='import for specific academic year'
        ),
    )

    def process_row(self, row, basic_data_model):
        DiseBasicData = basic_data_model

        # SCHCD,RURURB,MEDINSTR1,DISTHQ,DISTCRC,ESTDYEAR,PPSEC_YN,SCHRES_YN,SCHMGT,LOWCLASS,HIGHCLASS,SCHCAT,
        # PPSTUDENT,SCHTYPE,SCHSHI_YN,WORKDAYS,NOINSPECT,RESITYPE,PPTEACHER,VISITSBRC,VISITSCRC,
        # CONTI_R,CONTI_E,TLM_R,TLM_E,FUNDS_R,FUNDS_E

        school = {}

        if row.get('RURURB'):
            school['rural_urban'] = row.get('RURURB')
        if row.get('MEDINSTR1'):
            school['medium_of_instruction'] = row.get('MEDINSTR1')

        if row.get('DISTHQ'):
            school['distance_brc'] = row.get('DISTHQ')
        if row.get('DISTCRC'):
            school['distance_crc'] = row.get('DISTCRC')

        if row.get('ESTDYEAR'):
            school['yeur_estd'] = row.get('ESTDYEAR')
        if row.get('PPSEC_YN'):
            school['pre_pry_yn'] = row.get('PPSEC_YN')
        if row.get('SCHRES_YN'):
            school['residential_sch_yn'] = row.get('SCHRES_YN')
        if row.get('SCHMGT'):
            school['sch_management'] = row.get('SCHMGT')
        if row.get('LOWCLASS'):
            school['lowest_class'] = row.get('LOWCLASS')
        if row.get('HIGHCLASS'):
            school['highest_class'] = row.get('HIGHCLASS')
        if row.get('SCHCAT'):
            school['sch_category'] = row.get('SCHCAT')
        if row.get('PPSTUDENT'):
            school['pre_pry_students'] = row.get('PPSTUDENT')
        if row.get('SCHTYPE'):
            school['school_type'] = row.get('SCHTYPE')
        if row.get('SCHSHI_YN'):
            school['shift_school_yn'] = row.get('SCHSHI_YN')
        if row.get('WORKDAYS'):
            school['no_of_working_days'] = row.get('WORKDAYS')
        if row.get('NOINSPECT'):
            school['no_of_acad_inspection'] = row.get('NOINSPECT')
        if row.get('RESITYPE'):
            school['residential_sch_type'] = row.get('RESITYPE')
        if row.get('PPTEACHER'):
            school['pre_pry_teachers'] = row.get('PPTEACHER')
        if row.get('VISITSBRC'):
            school['visits_by_brc'] = row.get('VISITSBRC')
        if row.get('VISITSCRC'):
            school['visits_by_crc'] = row.get('VISITSCRC')

        if row.get('CONTI_R'):
            school['school_dev_grant_recd'] = row.get('CONTI_R')
        if row.get('CONTI_E'):
            school['school_dev_grant_expnd'] = row.get('CONTI_E')
        if row.get('TLM_R'):
            school['tlm_grant_recd'] = row.get('TLM_R')
        if row.get('TLM_E'):
            school['tlm_grant_expnd'] = row.get('TLM_E')
        if row.get('FUNDS_R'):
            school['funds_from_students_recd'] = row.get('FUNDS_R')
        if row.get('FUNDS_E'):
            school['funds_from_students_expnd'] = row.get('FUNDS_E')

        DiseBasicData.objects.filter(school_code=row.get('SCHCD')).update(**school)

    def handle(self, *args, **options):
        if 'year' in options:
            from_year, to_year = options.get('year').split('-')

        for general_data in args:
            full_path = os.path.join(settings.PROJECT_ROOT, general_data)

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
