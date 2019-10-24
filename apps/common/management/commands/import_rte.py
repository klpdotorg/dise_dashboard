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
        # SCHCD,AC_YEAR,WORKDAYS_PR,WORKDAYS_UPR,SCHHRSTCH_PR,SCHHRSCHILD_UPR,
        # SCHHRSTCH_PR1,SCHHRSTCH_UPR,APPROACHBYROAD,CCE_YN,PCR_MAINTAINED,
        # PCR_SHARED,WSEC25P_APPLIED,WSEC25P_ENROLLED,AIDRECD,STUADMITTED,
        # SMC_YN,SMCMEM_M,SMCMEM_F,SMSPARENTS_M,SMSPARENTS_F,SMCNOMLOCAL_M,
        # SMCNOMLOCAL_F,SMCMEETINGS,SMCSDP_YN,SMSCHILDREC_YN,
        # SPLTRG_CY_ENROLLED_B,SPLTRG_CY_ENROLLED_G,SPLTRG_CY_PROVIDED_B,
        # SPLTRG_CY_PROVIDED_G,SPLTRG_PY_ENROLLED_B,SPLTRG_PY_ENROLLED_G,
        # SPLTRG_PY_PROVIDED_B,SPLTRG_PY_PROVIDED_G,SPLTRG_BY,SPLTRG_PLACE,
        # SPLTRG_TYPE,SPLTRG_TOTEV,SPLTRG_MATERIAL_YN,TXTBKRECD_YN,TXTBKMNTH,
        # TXTBKYEAR,ACSTARTMNTH,MEALSINSCH,KITSHED,MDM_MAINTAINER,
        # DAYS_WITHFOOD,MEALSERVED,BENEFITTED_BOYS,BENEFITTED_GIRLS,
        # KITDEVGRANT_YN,COOK_M,COOK_F,INSPECT_SO,INSPECT_CM

        DiseBasicData = basic_data_model

        school = {}

        if not row.get('SCHCD').isdigit():
                return

        if row.get('APPROACHBYROAD'):
            school['approachable_by_road'] = row.get('APPROACHBYROAD')
        if row.get('CCE_YN'):
            school['continuous_comprehensive_evaluation'] = row.get('CCE_YN')
        if row.get('PCR_MAINTAINED'):
            school['pupil_cumulative_record_maitained'] = row.get('PCR_MAINTAINED')
        if row.get('PCR_SHARED'):
            school['pupil_cumulative_record_shared'] = row.get('PCR_SHARED')
        if row.get('SMC_YN'):
            school['school_management_committee'] = row.get('SMC_YN')
        if row.get('KITDEVGRANT_YN'):
            school['kitchen_devices_grant'] = row.get('KITDEVGRANT_YN')

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
