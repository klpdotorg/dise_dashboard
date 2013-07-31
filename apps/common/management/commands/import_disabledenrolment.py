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
        'Disabled_C1_Boys': 2,
        'Disabled_C2_Boys': 3,
        'Disabled_C3_Boys': 4,
        'Disabled_C4_Boys': 5,
        'Disabled_C5_Boys': 6,
        'Disabled_C6_Boys': 7,
        'Disabled_C7_Boys': 8,
        'Disabled_C8_Boys': 9,
        'Disabled_C1_Girls': 10,
        'Disabled_C2_Girls': 11,
        'Disabled_C3_Girls': 12,
        'Disabled_C4_Girls': 13,
        'Disabled_C5_Girls': 14,
        'Disabled_C6_Girls': 15,
        'Disabled_C7_Girls': 16,
        'Disabled_C8_Girls': 17,
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
                    if (int(row[self.INDEXES['Disabled_C%s_Boys' % klass]]) > 0 or
                            int(row[self.INDEXES['Disabled_C%s_Girls' % klass]]) > 0):
                        Enrolment.objects.filter(
                            yearly_data=yearly_data,
                            klass=klass
                        ).update(
                            disabled_boys=int(row[self.INDEXES['Disabled_C%s_Boys' % klass]]),
                            disabled_girls=int(row[self.INDEXES['Disabled_C%s_Girls' % klass]]),
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
