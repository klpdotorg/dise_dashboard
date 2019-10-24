import os
import csv
from optparse import make_option
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction

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
        # SCHCD,TCH_MALE,TCH_FEMALE,TCH_NR,HEADTCH,HTCHNAME,GRADABOVE,
        # TCHWITHPROF,DAYSINVLD,TCHINVLD
        DiseBasicData = basic_data_model

        school = {}

        if type(row.get('SCHCD')) is not int:
                return

        if row.get('TCH_MALE'):
            school['male_tch'] = row.get('TCH_MALE')
        if row.get('TCH_FEMALE'):
            school['female_tch'] = row.get('TCH_FEMALE')
        if row.get('TCH_NR'):
            school['noresp_tch'] = row.get('TCH_NR')
        if row.get('HEADTCH'):
            school['head_teacher'] = row.get('HEADTCH')
        if row.get('GRADABOVE'):
            school['graduate_teachers'] = row.get('GRADABOVE')
        if row.get('TCHWITHPROF'):
            school['tch_with_professional_qualification'] = row.get('TCHWITHPROF')
        if row.get('DAYSINVLD'):
            school['days_involved_in_non_tch_assgn'] = row.get('DAYSINVLD')
        if row.get('TCHINVLD'):
            school['teachers_involved_in_non_tch_assgn'] = row.get('TCHINVLD')

        DiseBasicData.objects.filter(school_code=row.get('SCHCD')).update(**school)

    def handle(self, *args, **options):
        if 'year' in options:
            from_year, to_year = options.get('year').split('-')

        for rte_data in args:
            full_path = os.path.join(settings.PROJECT_ROOT, rte_data)

            with open(full_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='|')
                count = 0

                print 'processing schools'
                DiseBasicData = get_models(session='%s-%s' % (from_year[-2:], to_year[-2:]), what='school')

                for row in reader:
                    self.process_row(row, DiseBasicData)
                    count += 1
                    if count % 100 == 0:
                        print count,
