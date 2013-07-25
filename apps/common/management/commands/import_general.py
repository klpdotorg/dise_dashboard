import os
import xlrd
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from common.models import Cluster, Block, EducationDistrict, Village, State
from django.conf import settings

from common.models import Cluster, Block, Village, State, EducationDistrict
from schools.models import School

class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports General data files'
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest="year",
            help='import for specific academic year'),
        )

    INDEXES = {
    }

    def process_row(self, row):
        pass

    def handle(self, *args, **options):
        print options