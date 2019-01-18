Steps to run the automation script:-
1. Do a git clone from the https://github.com/klpdotorg/dise_dashboard.git
2. The DISE xls file that needs to be imported should be in a readable folder.
3. run: mkvirtualenv disedashboard
4. run: pip install --upgrade -r requirements.txt
5. run: python manage.py import_dise_data StateName YY-YY folder_path_for_state 1>output 2>error &
   The format in which StateName is given is how it will be stored in db. So keep it Capital case.
   The year format is 16-17, 17-18 etc.
   The absolute folder path should be given.

Note:- It takes time to run the script as aggregation calculation takes time.
