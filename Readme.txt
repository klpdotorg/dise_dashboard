Steps to run the automation script:-
1. Do a git clone from the https://github.com/klpdotorg/dise_dashboard.git
2. The DISE xls file that needs to be imported should be in a readable folder.
3. run: mkvirtualenv disedashboard
4. run: pip install --upgrade -r requirements.txt
5. If you are creating data for a new academic year add the model in apps/schools/models.py file:
e.g.
class Dise1718BasicData(BasicData):
    class Meta:
        db_table = 'dise_1718_basic_data'

class Dise1718AssemblyAggregations(AssemblyAggregations):
    class Meta:
        db_table = 'dise_1718_assembly_aggregations'

class Dise1718BlockAggregations(BlockAggregations):
    class Meta:
        db_table = 'dise_1718_block_aggregations'

class Dise1718ClusterAggregations(ClusterAggregations):
    class Meta:
        db_table = 'dise_1718_cluster_aggregations'

class Dise1718ParliamentAggregations(ParliamentAggregations):
    class Meta:
        db_table = 'dise_1718_parliament_aggregations'

class Dise1718DistrictAggregations(DistrictAggregations):
    class Meta:
        db_table = 'dise_1718_district_aggregations'

class Dise1718PincodeAggregations(PincodeAggregations):
    class Meta:
        db_table = 'dise_1718_pincode_aggregations'

6. Run:- python manage.py makemigrations
7. Run:- python manage.py migrate
8. run: python manage.py import_dise_data StateName YY-YY folder_path_for_state 1>output 2>error &
   The format in which StateName is given is how it will be stored in db. So keep it Capital case.
   The year format is 16-17, 17-18 etc.
   The absolute folder path should be given.

Note:- It takes time to run the script as aggregation calculation takes time.
