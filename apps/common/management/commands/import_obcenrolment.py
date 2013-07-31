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
        'acyear': 1,
        'Class1_OBC_Enr_Boys': 2,
        'Class2_OBC_Enr_Boys': 3,
        'Class3_OBC_Enr_Boys': 4,
        'Class4_OBC_Enr_Boys': 5,
        'Class5_OBC_Enr_Boys': 6,
        'Class6_OBC_Enr_Boys': 7,
        'Class7_OBC_Enr_Boys': 8,
        'Class8_OBC_Enr_Boys': 9,
        'Class1_OBC_Enr_Girls': 10,
        'Class2_OBC_Enr_Girls': 11,
        'Class3_OBC_Enr_Girls': 12,
        'Class4_OBC_Enr_Girls': 13,
        'Class5_OBC_Enr_Girls': 14,
        'Class6_OBC_Enr_Girls': 15,
        'Class7_OBC_Enr_Girls': 16,
        'Class8_OBC_Enr_Girls': 17,
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

        with transaction.commit_on_success():
            for klass in range(1, 9):
                try:
                    if (int(row[self.INDEXES['Class%s_OBC_Enr_Boys' % klass]]) > 0 or
                            int(row[self.INDEXES['Class%s_OBC_Enr_Girls' % klass]]) > 0):
                        Enrolment.objects.filter(
                            yearly_data=yearly_data,
                            klass=klass
                        ).update(
                            obc_boys=int(row[self.INDEXES['Class%s_OBC_Enr_Boys' % klass]]),
                            obc_girls=int(row[self.INDEXES['Class%s_OBC_Enr_Girls' % klass]]),
                        )
                except Exception as e:
                    print str(e)

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
