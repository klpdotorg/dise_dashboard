import os
import xlrd
from optparse import make_option


from django.core.management.base import BaseCommand, CommandError
from common.models import Cluster, Block, EducationDistrict, Village, State
from django.conf import settings

from common.models import Cluster, Block, Village, State, EducationDistrict
from schools.models import School, AcademicYear, YearlyData

class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports Basic data files'
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest="year",
            help='import for specific academic year'),
        )

    INDEXES = {
        'district': 0,
        'school_code': 1,
        'school_name': 2,
        'block': 3,
        'cluster': 4,
        'village': 5,
        'pincode': 6
    }

    def process_row(self, row, year=None):
        district, created = EducationDistrict.objects.get_or_create(
            name=row[self.INDEXES['district']]
        )
        # TODO: Detect urban/rural from village name
        village, created = Village.objects.get_or_create(
            name=row[self.INDEXES['village']]
        )
        block, created = Block.objects.get_or_create(
            name=row[self.INDEXES['block']],
            education_district=district
        )
        cluster, created = Cluster.objects.get_or_create(
            name=row[self.INDEXES['cluster']],
            block=block
        )
        school, created = School.objects.get_or_create(
            name=row[self.INDEXES['school_name']],
            code=str(int(row[self.INDEXES['school_code']])),
            pincode=int(row[self.INDEXES['pincode']]),
        )
        yearly_data, created = YearlyData.objects.get_or_create(
            school=school,
            academic_year=year
        )
        yearly_data.cluster = cluster
        yearly_data.village = village
        yearly_data.save()

    def handle(self, *args, **options):
        year=None

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
                        if not row[self.INDEXES['school_code']]:
                            continue
                        self.process_row(row, year)

                        if idx % 100 == 0:
                            print "%s/%s: %s%% done." % (idx, sheet.nrows, (idx/float(sheet.nrows))*100)

            except Exception as e:
                print str(e)