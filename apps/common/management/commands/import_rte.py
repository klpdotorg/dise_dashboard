import os
import xlrd
from optparse import make_option
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from common.models import Cluster, Block, EducationDistrict, Village, State
from django.conf import settings
from django.db import transaction

from schools.models import *


class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports General data files'
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest="year",
            help='import for specific academic year'
        ),
    )

    INDEXES = {
        'schcd': 0,
        'acyear': 1,
        'Working_Days_Primary': 2,
        'Working_Days_UPrimary': 3,
        'Schoool_Hours_Children_Pri': 4,
        'School_Hours_Children_UPri': 5,
        'School_Hours_Tch_P': 6,
        'School_Hours_Tch_UPR': 7,
        'Approachable_by_All_Weather_Road': 8,
        'CCE_implemented': 9,
        'People_Cumilativere_Record_Maintained': 10,
        'PCR_Shared_with_Parents': 11,
        'Children_from_Weaker_Section_Applied': 12,
        'Children_from_Weaker_Section_Enrolled': 13,
        'Aid_Received': 14,
        'Chilren_Admitted_for_Free_Education': 15,
        'SMC_Constituted': 16,
        'SMC_Members_Male': 17,
        'SMC_Members_Female': 18,
        'SMC_Members_Parents_Male': 19,
        'SMC_Members_PArents_Female': 20,
        'SMC_Members_Local_Authority_Male': 21,
        'SMC_Members_Local_Authority_Female': 22,
        'SMC_Meetings_Held': 23,
        'School_Developmentplan_Prepared': 24,
        'SMC_Children_Record_Maintained': 25,
        'Chld_Enrolled_for_Sp_Training_Current_Year_B': 26,
        'Chld_Enrolled_for_Sp_Training_Current_Year_G': 27,
        'Spl_Training_Provided_Current_Year_B': 28,
        'Spl_Training_Provided_Current_Year_G': 29,
        'Spl_Training_Enrolled_Previous_Year_B': 30,
        'Spl_Training_Enrolled_Previous_Year_G': 31,
        'Spl_training_Provided_Previous_Year_B': 32,
        'Spl_Training_Provided_Previous_Year_G': 33,
        'Spl_Training_Conducted_by': 34,
        'Spl_Training_Place': 35,
        'spl_Training_Type': 36,
        'Tch_or_EVS_for_spl_training': 37,
        'Spl_Training_Material': 38,
        'Textbook_Received': 39,
        'Text_Book_Received_Month': 40,
        'Text_Book_Received_Year': 41,
        'Academic_Session_Start_in': 42,
        'MDM_Status': 43,
        'Kitchenshed_Status': 44,
        'MDM_Source': 45,
        'Days_Meals_Served': 46,
        'Meals_Served_Prev_Yr': 47,
        'Students_Opted_MDM_B': 48,
        'Stdents_Opted_MDM_G': 49,
        'Kitchen_Devaices_Grant': 50,
        'Cook_M': 51,
        'Cook_F': 52,
        'Inspections_by_SO': 53,
        'Inspections_by_CM': 54,
    }

    def process_row(self, row, year):
        try:
            school = School.objects.get(code=int(row[self.INDEXES['schcd']]))
        except Exception as e:
            school = School(
                code=int(row[self.INDEXES['schcd']]),
                name="School@%s" % int(row[self.INDEXES['schcd']])
            )
            school.save()
            print "created", str(school)

        yearly_data, created = YearlyData.objects.get_or_create(
            school=school,
            academic_year_id=year
        )

        yearly_data.sdmc_constituted = int(row[self.INDEXES['SMC_Constituted']])
        yearly_data.sdmc_meeting_count = int(row[self.INDEXES['SMC_Meetings_Held']])

        yearly_data.textbook_received = int(row[self.INDEXES['Textbook_Received']])

        try:
            yearly_data.textbook_received_date = datetime(
                int(row[self.INDEXES['Text_Book_Received_Year']]),
                int(row[self.INDEXES['Text_Book_Received_Month']]),
                1
            )
        except:
            print int(row[self.INDEXES['Text_Book_Received_Year']]), int(row[self.INDEXES['Text_Book_Received_Month']])

        yearly_data.weakersec_children_applied = int(row[self.INDEXES['Children_from_Weaker_Section_Applied']])
        yearly_data.weakersec_children_enrolled = int(row[self.INDEXES['Children_from_Weaker_Section_Enrolled']])

        yearly_data.middaymeal_status = int(row[self.INDEXES['MDM_Status']])
        yearly_data.kitchenshed_status = int(row[self.INDEXES['Kitchenshed_Status']])

        yearly_data.save()

    def handle(self, *args, **options):
        year = None

        if 'year' in options:
            from_year, to_year = options.get('year').split('-')
            year = AcademicYear.objects.get(from_year=from_year, to_year=to_year)

        for basic_data in args:
            full_path = os.path.join(settings.DATADUMP_ROOT, basic_data)
            try:
                fp = xlrd.open_workbook(full_path)
                for sheet in fp.sheets():
                    for idx in range(1, sheet.nrows):
                        row = sheet.row_values(idx)
                        if not row[self.INDEXES['schcd']]:
                            continue
                        self.process_row(row, year)
                        # import pdb; pdb.set_trace();

                        if idx % 100 == 0:
                            print "%s/%s: %s%% done." % (idx, sheet.nrows, (idx/float(sheet.nrows))*100)

            except Exception as e:
                print str(e)
