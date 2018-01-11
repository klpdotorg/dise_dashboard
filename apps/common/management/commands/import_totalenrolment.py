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
        # SCHCD,AC_YEAR,C1_TOTB,C2_TOTB,C3_TOTB,C4_TOTB,C5_TOTB,C6_TOTB,C7_TOTB,
        # C8_TOTB,C1_TOTG,C2_TOTG,C3_TOTG,C4_TOTG,C5_TOTG,C6_TOTG,C7_TOTG,
        # C8_TOTG,C1_CB,C2_CB,C3_CB,C4_CB,C5_CB,C6_CB,C7_CB,C8_CB,C1_CG,C2_CG,
        # C3_CG,C4_CG,C5_CG,C6_CG,C7_CG,C8_CG,C1_TB,C2_TB,C3_TB,C4_TB,C5_TB,
        # C6_TB,C7_TB,C8_TB,C1_TG,C2_TG,C3_TG,C4_TG,C5_TG,C6_TG,C7_TG,C8_TG,
        # C1_OB,C2_OB,C3_OB,C4_OB,C5_OB,C6_OB,C7_OB,C8_OB,C1_OG,C2_OG,C3_OG,
        # C4_OG,C5_OG,C6_OG,C7_OG,C8_OG,C1_DIS_B,C2_DIS_B,C3_DIS_B,C4_DIS_B,
        # C5_DIS_B,C6_DIS_B,C7_DIS_B,C8_DIS_B,C1_DIS_G,C2_DIS_G,C3_DIS_G,
        # C4_DIS_G,C5_DIS_G,C6_DIS_G,C7_DIS_G,C8_DIS_G,FAIL1B,FAIL2B,FAIL3B,
        # FAIL4B,FAIL5B,FAIL6B,FAIL7B,FAIL8B,FAIL1G,FAIL2G,FAIL3G,FAIL4G,FAIL5G,
        # FAIL6G,FAIL7G,FAIL8G,C5_APPEARB,C5_APPEARG,C5_PASSB,C5_PASSG,C5_M60B,
        # C5_M60G,C7_APPEARB,C7_APPEARG,C7_PASSB,C7_PASSG,C7_M60B,C7_M60G
        DiseBasicData = basic_data_model

        school = {
            'total_boys': 0,
            'total_girls': 0
        }

        if row.get('C1_TOTB'):
            school['class1_total_enr_boys'] = row.get('C1_TOTB')
            school['total_boys'] += int(school['class1_total_enr_boys'])
        if row.get('C2_TOTB'):
            school['class2_total_enr_boys'] = row.get('C2_TOTB')
            school['total_boys'] += int(school['class2_total_enr_boys'])
        if row.get('C3_TOTB'):
            school['class3_total_enr_boys'] = row.get('C3_TOTB')
            school['total_boys'] += int(school['class3_total_enr_boys'])
        if row.get('C4_TOTB'):
            school['class4_total_enr_boys'] = row.get('C4_TOTB')
            school['total_boys'] += int(school['class4_total_enr_boys'])
        if row.get('C5_TOTB'):
            school['class5_total_enr_boys'] = row.get('C5_TOTB')
            school['total_boys'] += int(school['class5_total_enr_boys'])
        if row.get('C6_TOTB'):
            school['class6_total_enr_boys'] = row.get('C6_TOTB')
            school['total_boys'] += int(school['class6_total_enr_boys'])
        if row.get('C7_TOTB'):
            school['class7_total_enr_boys'] = row.get('C7_TOTB')
            school['total_boys'] += int(school['class7_total_enr_boys'])
        if row.get('C8_TOTB'):
            school['class8_total_enr_boys'] = row.get('C8_TOTB')
            school['total_boys'] += int(school['class8_total_enr_boys'])
        if row.get('C9_B'):
            school['class9_total_enr_boys'] = row.get('C9_B')
            school['total_boys'] += int(school['class9_total_enr_boys'])
        if row.get('C10_B'):
            school['class10_total_enr_boys'] = row.get('C10_B')
            school['total_boys'] += int(school['class10_total_enr_boys'])
        if row.get('C11_B'):
            school['class11_total_enr_boys'] = row.get('C11_B')
            school['total_boys'] += int(school['class11_total_enr_boys'])
        if row.get('C12_B'):
            school['class12_total_enr_boys'] = row.get('C12_B')
            school['total_boys'] += int(school['class12_total_enr_boys'])
        if row.get('C1_TOTG'):
            school['class1_total_enr_girls'] = row.get('C1_TOTG')
            school['total_girls'] += int(school['class1_total_enr_girls'])
        if row.get('C2_TOTG'):
            school['class2_total_enr_girls'] = row.get('C2_TOTG')
            school['total_girls'] += int(school['class2_total_enr_girls'])
        if row.get('C3_TOTG'):
            school['class3_total_enr_girls'] = row.get('C3_TOTG')
            school['total_girls'] += int(school['class3_total_enr_girls'])
        if row.get('C4_TOTG'):
            school['class4_total_enr_girls'] = row.get('C4_TOTG')
            school['total_girls'] += int(school['class4_total_enr_girls'])
        if row.get('C5_TOTG'):
            school['class5_total_enr_girls'] = row.get('C5_TOTG')
            school['total_girls'] += int(school['class5_total_enr_girls'])
        if row.get('C6_TOTG'):
            school['class6_total_enr_girls'] = row.get('C6_TOTG')
            school['total_girls'] += int(school['class6_total_enr_girls'])
        if row.get('C7_TOTG'):
            school['class7_total_enr_girls'] = row.get('C7_TOTG')
            school['total_girls'] += int(school['class7_total_enr_girls'])
        if row.get('C8_TOTG'):
            school['class8_total_enr_girls'] = row.get('C8_TOTG')
            school['total_girls'] += int(school['class8_total_enr_girls'])
        if row.get('C9_G'):
            school['class9_total_enr_girls'] = row.get('C9_G')
            school['total_girls'] += int(school['class9_total_enr_girls'])
        if row.get('C10_G'):
            school['class10_total_enr_girls'] = row.get('C10_G')
            school['total_girls'] += int(school['class10_total_enr_girls'])
        if row.get('C11_G'):
            school['class11_total_enr_girls'] = row.get('C11_G')
            school['total_girls'] += int(school['class11_total_enr_girls'])
        if row.get('C12_G'):
            school['class12_total_enr_girls'] = row.get('C12_G')
            school['total_girls'] += int(school['class12_total_enr_girls'])

        if row.get('APPRB5'):
            school['boys_appeared_primary_exam'] = row.get('APPRB5')
        if row.get('APPRG5'):
            school['girls_appeared_primary_exam'] = row.get('APPRG5')
        if row.get('APPRB8'):
            school['boys_appeared_upper_primary_exam'] = row.get('APPRB8')
        if row.get('APPRG8'):
            school['girls_appeared_upper_primary_exam'] = row.get('APPRG8')
        if row.get('PASSB5'):
            school['boys_passed_primary_exam'] = row.get('PASSB5')
        if row.get('PASSG5'):
            school['girls_passed_primary_exam'] = row.get('PASSG5')
        if row.get('PASSB8'):
            school['boys_passed_upper_primary_exam'] = row.get('PASSB8')
        if row.get('PASSG8'):
            school['girls_passed_upper_primary_exam'] = row.get('PASSG8')
        if row.get('P60B5'):
            school['boys_more_sixty_percent_primary_exam'] = row.get('P60B5')
        if row.get('P60G5'):
            school['girls_more_sixty_percent_primary_exam'] = row.get('P60G5')
        if row.get('P60B8'):
            school['boys_more_sixty_percent_upper_primary_exam'] = row.get('P60B8')
        if row.get('P60G8'):
            school['girls_more_sixty_percent_upper_primary_exam'] = row.get('P60G8')
            

        DiseBasicData.objects.filter(school_code=row.get('SCHCD')).update(**school)

    def handle(self, *args, **options):
        if 'year' in options:
            from_year, to_year = options.get('year').split('-')

        for rte_data in args:
            full_path = os.path.join(settings.PROJECT_ROOT, rte_data)

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
