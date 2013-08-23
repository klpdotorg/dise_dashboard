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
        'School_Code': 0,
        'Male_Tch': 1,
        'Female_Tch': 2,
        'NoResp_Tch': 3,
        'Head_Teacher': 4,
        'Graduate_Teachers': 5,
        'Tch_with_professional_Qualification': 6,
        'Days_involved_in_non_tch_assgn': 7,
        'Teachers_involved_in_non_tch_assgn': 8,
    }

    def process_row(self, row, year):
        try:
            school = School.objects.get(code=int(row[self.INDEXES['School_Code']]))
        except Exception as e:
            school = School(
                code=int(row[self.INDEXES['School_Code']]),
                name="School@%s" % int(row[self.INDEXES['School_Code']])
            )
            school.save()
            print "created", str(school)

        yearly_data, created = YearlyData.objects.get_or_create(
            school=school,
            academic_year_id=year
        )

        teacher_count, created = TeacherCount.objects.get_or_create(
            yearly_data=yearly_data
        )
        teacher_count.male = int(row[self.INDEXES['Male_Tch']])
        teacher_count.female = int(row[self.INDEXES['Female_Tch']])
        teacher_count.total = int(row[self.INDEXES['Male_Tch']]) + int(row[self.INDEXES['Female_Tch']])
        teacher_count.noresp = int(row[self.INDEXES['NoResp_Tch']])
        teacher_count.headteacher = int(row[self.INDEXES['Head_Teacher']])
        teacher_count.graduate = int(row[self.INDEXES['Graduate_Teachers']])
        teacher_count.with_prof_qual = int(row[self.INDEXES['Tch_with_professional_Qualification']])
        teacher_count.days_in_non_tch = int(row[self.INDEXES['Days_involved_in_non_tch_assgn']])
        teacher_count.involved_in_non_tch = int(row[self.INDEXES['Teachers_involved_in_non_tch_assgn']])
        teacher_count.save()

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
                        if not row[self.INDEXES['School_Code']]:
                            continue
                        self.process_row(row, year)
                        # import pdb; pdb.set_trace();

                        if idx % 100 == 0:
                            print "%s/%s: %s%% done." % (idx, sheet.nrows, (idx/float(sheet.nrows))*100)

            except Exception as e:
                print str(e)
