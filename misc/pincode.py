import psycopg2

connection = psycopg2.connect("dbname=klpdise_olap user=klp")
cursor = connection.cursor()

years = ['1011', '1112', '1213']
query = {'get_schools_1011': "SELECT school_code, school_name, centroid, pincode from dise_1011_basic_data WHERE centroid!='None';",
'get_schools_1112': "SELECT school_code, school_name, centroid, pincode from dise_1112_basic_data WHERE centroid!='None';",
'get_schools_1213': "SELECT school_code, school_name, centroid, pincode from dise_1213_basic_data WHERE centroid!='None';",
'check_pincode': "SELECT pincode FROM postal WHERE ST_Contains(wkb_geometry, %(school)s)='t';",
'update_pincode_1011': "UPDATE dise_1011_basic_data SET new_pincode=%(pincode)s WHERE school_code=%(school)s;",
'update_pincode_1112': "UPDATE dise_1112_basic_data SET new_pincode=%(pincode)s WHERE school_code=%(school)s;",
'update_pincode_1213': "UPDATE dise_1213_basic_data SET new_pincode=%(pincode)s WHERE school_code=%(school)s;"}


# Get all PIN polygons

# For each year
for year in years:
  print "Year", year
  # Get all schools
  cursor.execute(query['get_schools_'+year])
  schools = cursor.fetchall()
  print "Schools", schools.__len__()
  # For each school
  for school in schools:
    # If school within pincode polygon
    cursor.execute(query['check_pincode'], {'school': school[2]})
    pincode = cursor.fetchall()
    if pincode:
      # Update new PIN code column in schools table
      cursor.execute(query['update_pincode_'+year], {'pincode':pincode[0], 'school': (school[0],)})

  connection.commit()

cursor.close()
connection.close()

