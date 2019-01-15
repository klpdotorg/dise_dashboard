import xlrd
import os
import re
import unicodecsv as csv
from os import sys, listdir
from django.core import management
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Insert DISE data for the specified state and year into the dise database"

    dise_files = {
                "Basic": {"suffix": "basic", "found": 0, "file_name": '',
                          "command": "import_basic"},
                "Facility": {"suffix": "facility", "found": 0, "file_name": '',
                             "command": "import_facilities"},
                "General": {"suffix": "general", "found": 0, "file_name": '',
                            "command": "import_general"},
                "RTE": {"suffix": "rte", "found": 0, "file_name": '',
                        "command": "import_rte"},
                "Teachers": {"suffix": "teachercount", "found": 0,
                             "file_name": '', "command": "import_teachercount"},
                "TotalEnrolment": {"suffix": "totalenrolment", "found": 0,
                                   "file_name": '',
                                   "command": "import_totalenrolment"}
               }

    def add_arguments(self, parser):
        print("in add arguments")
        parser.add_argument('state', nargs='+', help="State name")
        parser.add_argument('year', help="Academic Year, format YYYY")
        parser.add_argument('directory',
                            help="Absolute path of directory where DISE files are stored")

    def convert_xlsx_to_csv(self, file_name, state, suffix, year):
        with xlrd.open_workbook(file_name) as wb:
            sh = wb.sheet_by_index(0)
            file_name = "csvs/"+state+"_"+suffix+"_"+year+".csv"
            if not os.path.exists("csvs"):
                os.makedirs("csvs")
            with open(file_name, 'wb') as f:
                csv_file = csv.writer(f, delimiter="|", lineterminator='\n')
                for r in range(sh.nrows):
                    row = sh.row_values(r)
                    row = [re.sub(r"\.", ' ', value) for value in row]
                    row = [re.sub(r"\,", ' ', value) for value in row]
                    row = [re.sub(r"\s+", ' ', value) for value in row]
                    row = [re.sub(r"\s+-\s+",  '-', value) for value in row]
                    row = [value.strip('  ') for value in row]
                    csv_file.writerow(row)
        return file_name

    def add_state(self, file_name, state):
        with open(file_name, 'r') as csvinput:
            reader = csv.reader(csvinput, delimiter="|")
            print(file_name)
            outputfile = file_name.replace(".csv", "_out.csv")
            print(outputfile)
            with open(outputfile, 'wb') as csvoutput:
                writer = csv.writer(csvoutput, delimiter="|", lineterminator='\n')
                headers = reader.next()
                writer.writerow(["STATE_NAME"]+headers)
                for row in reader:
                    row = [re.sub(r",", ' ', value) for value in row]
                    writer.writerow([state]+row)
            return outputfile

    def create_csv_files(self, directory, state, academic_year):
        for filename in listdir(directory):
            for dise_file_type in self.dise_files:
                if dise_file_type in filename:
                    print(dise_file_type)
                    file_name = self.convert_xlsx_to_csv(directory+"/"+filename,
                                    state, self.dise_files[dise_file_type]["suffix"],
                                    academic_year)
                    outputfile = self.add_state(file_name, state)
                    self.dise_files[dise_file_type]["found"] = 1
                    self.dise_files[dise_file_type]["file_name"] = outputfile

    def call_management_commands(self, academic_year):
        print("Calling managment commands")
        for dise_file_type in sorted(self.dise_files):
            print("Running for: "+dise_file_type)
            if self.dise_files[dise_file_type]["found"]:
                print("Running for: "+dise_file_type)
                management.call_command(
                        self.dise_files[dise_file_type]["command"],
                        self.dise_files[dise_file_type]["file_name"],
                        year=academic_year)

    def run_aggregates(self):
        files = ['misc/cluster_aggregation.sql',
                 'misc/block_aggregation.sql',
                 'misc/district_aggregation.sql',
                 'misc/assembly_aggregation.sql',
                 'misc/parliament_aggregation.sql',
                 'misc/pincode_aggregation.sql']
        for filename in files:
            print("Running "+filename)
            f = open(filename)
            with connection.cursor() as cursor:
                cursor.execute(f.read())
                f.close()

    def handle(self, *args, **options):
        if len(args) != 3:
            print(len(args))
            print(args)
            print("Please give state name, academic year and dise file name along with path as arguments. USAGE: python import_disedata.py Karnataka 16-17 ~/dise/DISE_All_India_Schools_Data_2016-17/Karnataka/DISE_Basic_Data_21-11-2017\ 14-21-59.xlsx")
            sys.exit()

        state = args[0]
        academic_year = args[1]
        directory = args[2]

        print("State: "+state+", Academic Year: "+academic_year+", Directory: "+directory)

        self.create_csv_files(directory, state, academic_year)
        self.call_management_commands(academic_year)
        print("Processing aggregates")
        self.run_aggregates()
        print("Finished")
