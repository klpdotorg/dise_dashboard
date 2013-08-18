import os
import xlrd
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from common.models import Cluster, Block, EducationDistrict, Village, State
from django.conf import settings

from common.models import Cluster, Block, Village, State, EducationDistrict
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
        'Building_Status': 1,
        'Tot_Clrooms': 2,
        'Classrooms_in_Good_Condition': 3,
        'Classrooms_require_major_repair': 4,
        'Classrooms_require_minor_repair': 5,
        'Other_rooms_in_Good_Cond': 6,
        'Other_rooms_need_major_rep': 7,
        'Other_rooms_need_minor_rep': 8,
        'Toilet_Common': 9,
        'Toilet_Boys': 10,
        'Toilet_Girls': 11,
        'Kitchen_Devices_Grant': 12,
        'Status_of_MDM': 13,
        'Computer_Aided_Learnin_Lab': 14,
        'Separate_Room_for_HeadMaster': 15,
        'Electricity': 16,
        'Boundary_Wall': 17,
        'Library_YN': 18,
        'PlayGround': 19,
        'Blackboard': 20,
        'Books_in_library': 21,
        'Drinking_Water': 22,
        'Medical_Checkup': 23,
        'Ramps': 24,
        'No_of_Computers': 25,
        'Male_Tch': 26,
        'Female_Tch': 27,
        'NoResp_Tch': 28,
        'Head_Teacher': 29,
        'Graduate_Teachers': 30,
        'Tch_with_professional_Qualification': 31,
        'Days_involved_in_non_tch_assgn': 32,
        'Teachers_involved_in_non_tch_assgn': 33
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

        try:
            building_status = SchoolBuildingStatus.objects.get(id=int(row[self.INDEXES['Building_Status']]))
        except:
            print 'Unknown SchoolBuildingStatus found', school.id, row[self.INDEXES['Building_Status']]
            building_status = SchoolBuildingStatus(
                id=int(row[self.INDEXES['Building_Status']]),
                name="Unknown"
            )
            building_status.save()
        yearly_data.building_status = building_status

        try:
            drinking_water_source = DrinkingWaterSource.objects.get(id=int(row[self.INDEXES['Drinking_Water']]))
        except:
            print 'Unknown DrinkingWaterSource found', school.id, row[self.INDEXES['Drinking_Water']]
            drinking_water_source = DrinkingWaterSource.objects.create(
                id=int(row[self.INDEXES['Drinking_Water']]),
                name="Unknown"
            )
        yearly_data.drinking_water_source = drinking_water_source

        try:
            boundary_wall_type = BoundaryWallType.objects.get(id=int(row[self.INDEXES['Boundary_Wall']]))
        except:
            print 'Unknown BoundaryWallType found', school.id, row[self.INDEXES['Boundary_Wall']]
            boundary_wall_type = BoundaryWallType.objects.create(
                id=int(row[self.INDEXES['Boundary_Wall']]),
                name="Unknown"
            )
        yearly_data.boundary_wall_type = boundary_wall_type

        yearly_data.room_count = int(row[self.INDEXES['Tot_Clrooms']])
        yearly_data.room_for_headmaster = int(row[self.INDEXES['Separate_Room_for_HeadMaster']])
        yearly_data.electricity_status = int(row[self.INDEXES['Electricity']])
        yearly_data.library_available = int(row[self.INDEXES['Library_YN']])
        yearly_data.library_book_count = int(row[self.INDEXES['Books_in_library']])
        yearly_data.playground_available = int(row[self.INDEXES['PlayGround']])
        yearly_data.computer_count = int(row[self.INDEXES['No_of_Computers']])
        yearly_data.blackboard_count = int(row[self.INDEXES['Blackboard']])
        yearly_data.cal_lab_available = int(row[self.INDEXES['Computer_Aided_Learnin_Lab']])
        yearly_data.medical_checkup = int(row[self.INDEXES['Medical_Checkup']])
        yearly_data.ramp_available = int(row[self.INDEXES['Ramps']])
        yearly_data.save()

        clroom_good = Room.objects.get_or_create(
            yearly_data=yearly_data,
            type='class',
            condition='good',
        )
        clroom_good.count = int(row[self.INDEXES['Classrooms_in_Good_Condition']])
        clroom_good.save()

        clroom_major = Room.objects.get_or_create(
            yearly_data=yearly_data,
            type='class',
            condition='major',
        )
        clroom_major.count = int(row[self.INDEXES['Classrooms_require_major_repair']])
        clroom_major.save()

        clroom_minor = Room.objects.get_or_create(
            yearly_data=yearly_data,
            type='class',
            condition='minor',
        )
        clroom_minor.count = int(row[self.INDEXES['Classrooms_require_minor_repair']])
        clroom_minor.save()

        other_room_good = Room.objects.get_or_create(
            yearly_data=yearly_data,
            type='other',
            condition='good',
        )
        other_room_good.count = int(row[self.INDEXES['Other_rooms_in_Good_Cond']])
        other_room_good.save()

        other_room_major = Room.objects.get_or_create(
            yearly_data=yearly_data,
            type='other',
            condition='major',
        )
        other_room_major.count = int(row[self.INDEXES['Other_rooms_need_major_rep']])
        other_room_major.save()

        other_room_minor = Room.objects.get_or_create(
            yearly_data=yearly_data,
            type='other',
            condition='minor',
        )
        other_room_minor.count = int(row[self.INDEXES['Other_rooms_need_minor_rep']])
        other_room_minor.save()

        toilet_common = Toilet.objects.get_or_create(
            yearly_data=yearly_data,
            type='common',
        )
        toilet_common.count = int(row[self.INDEXES['Toilet_Common']])
        toilet_common.save()

        toilet_boys = Toilet.objects.get_or_create(
            yearly_data=yearly_data,
            type='boy',
        )
        toilet_boys.count = int(row[self.INDEXES['Toilet_Boys']])
        toilet_boys.save()

        toilet_girls = Toilet.objects.get_or_create(
            yearly_data=yearly_data,
            type='girl',
        )
        toilet_girls.count = int(row[self.INDEXES['Toilet_Girls']])
        toilet_girls.save()

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
