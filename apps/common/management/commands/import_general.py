import os
import xlrd
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from common.models import Cluster, Block, EducationDistrict, Village, State
from django.conf import settings

from common.models import Cluster, Block, Village, State, EducationDistrict
from schools.models import School, AcademicYear, InstractionMedium, ResidentialType, YearlyData, SchoolManaagement, SchoolCategory


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
        'Rural_Urban': 1,
        'Medium_of_Instruction': 2,
        'Distance_BRC': 3,
        'Distance_CRC': 4,
        'Yeur_Estd': 5,
        'Pre_Pry_YN': 6,
        'Residential_Sch_YN': 7,
        'Sch_Management': 8,
        'Lowest_Class': 9,
        'Highest_Class': 10,
        'Sch_Category': 11,
        'Pre_Pry_Students': 12,
        'School_Type': 13,
        'Shift_School_YN': 14,
        'No_of_Working_Days': 15,
        'No_of_Acad_Inspection': 16,
        'Residential_Sch_Type': 17,
        'Pre_Pry_Teachers': 18,
        'Visits_by_BRC': 19,
        'Visits_by_CRC': 20,
        'School_Dev_Grant_Recd': 21,
        'School_Dev_Grant_Expnd': 22,
        'TLM_Grant_Recd': 23,
        'TLM_Grant_Expnd': 24,
        'Funds_from_students_Recd': 25,
        'Funds_from_students_Expnd': 26,
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
            academic_year=year
        )
        yearly_data.area_type = row[self.INDEXES['Rural_Urban']]

        try:
            medium = InstractionMedium.objects.get(id=int(row[self.INDEXES['Medium_of_Instruction']]))
            yearly_data.mediums.add(medium)
        except:
            pass

        yearly_data.distance_from_brc = row[self.INDEXES['Distance_BRC']]
        yearly_data.distance_from_crc = row[self.INDEXES['Distance_CRC']]

        school.year_established = row[self.INDEXES['Yeur_Estd']]
        school.save()

        yearly_data.pre_primary_available = row[self.INDEXES['Pre_Pry_YN']]
        yearly_data.pre_primary_student_count = row[self.INDEXES['Pre_Pry_Students']]
        yearly_data.pre_primary_teacher_count = row[self.INDEXES['Pre_Pry_Teachers']]

        yearly_data.residential = row[self.INDEXES['Residential_Sch_YN']]
        try:
            res_type = ResidentialType.objects.get(id=int(row[self.INDEXES['Residential_Sch_Type']]))
        except:
            print 'Unknown ResidentialType found', school.id, row[self.INDEXES['Residential_Sch_Type']]
            res_type = ResidentialType(
                id=int(row[self.INDEXES['Residential_Sch_Type']]),
                name="Unknown"
            )
            res_type.save()
        yearly_data.residential_type = res_type

        try:
            mgmt = SchoolManaagement.objects.get(id=int(row[self.INDEXES['Sch_Management']]))
        except:
            print 'Unknown Management found', school.id, row[self.INDEXES['Sch_Management']]
            mgmt = SchoolManaagement(
                id=int(row[self.INDEXES['Sch_Management']]),
                name="Unknown"
            )
            mgmt.save()

        yearly_data.management = mgmt

        yearly_data.lowest_class = int(row[self.INDEXES['Lowest_Class']])
        yearly_data.highest_class = int(row[self.INDEXES['Highest_Class']])

        try:
            category = SchoolCategory.objects.get(id=int(row[self.INDEXES['Sch_Category']]))
        except:
            print 'Unknown Category found', school.id, row[self.INDEXES['Sch_Category']]
            category = SchoolCategory(
                id=int(row[self.INDEXES['Sch_Category']]),
                name="Unknown"
            )
            category.save()
        yearly_data.category = category

        yearly_data.type = row[self.INDEXES['School_Type']]
        yearly_data.part_of_shift = row[self.INDEXES['Shift_School_YN']]
        yearly_data.working_day_count = row[self.INDEXES['No_of_Working_Days']]

        yearly_data.academic_inspection_count = row[self.INDEXES['No_of_Acad_Inspection']]
        yearly_data.brc_visit_count = row[self.INDEXES['Visits_by_BRC']]
        yearly_data.crc_visit_count = row[self.INDEXES['Visits_by_CRC']]

        yearly_data.development_grant_received = float(row[self.INDEXES['School_Dev_Grant_Recd']])
        yearly_data.development_grant_expenditure = float(row[self.INDEXES['School_Dev_Grant_Expnd']])
        yearly_data.tlm_grant_received = float(row[self.INDEXES['TLM_Grant_Recd']])
        yearly_data.tlm_grant_expenditure = float(row[self.INDEXES['TLM_Grant_Expnd']])
        yearly_data.fund_from_student_received = float(row[self.INDEXES['Funds_from_students_Recd']])
        yearly_data.fund_from_student_expenditure = float(row[self.INDEXES['Funds_from_students_Expnd']])

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
                        if not row[self.INDEXES['School_Code']]:
                            continue
                        self.process_row(row, year)

                        if idx % 100 == 0:
                            print "%s/%s: %s%% done." % (idx, sheet.nrows, (idx/float(sheet.nrows))*100)

            except Exception as e:
                print str(e)
