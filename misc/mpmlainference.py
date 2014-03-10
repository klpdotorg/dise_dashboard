import psycopg2
import operator
import csv

connection = psycopg2.connect("dbname=klpdise_olap user=klp")
cursor = connection.cursor()
notfound1011 = csv.writer(open('notfound1011.csv', 'w'))
notfound1112 = csv.writer(open('notfound1112.csv', 'w'))
notfound1213 = csv.writer(open('notfound1213.csv', 'w'))

years = ['1011', '1112', '1213']
query = {'get_schools_1011': "SELECT school_code, pincode, school_name, district, block_name, cluster_name, village_name from dise_1011_basic_data WHERE centroid IS NULL;",
'get_schools_1112': "SELECT school_code, pincode, school_name, district, block_name, cluster_name, village_name from dise_1112_basic_data WHERE centroid IS NULL;",
'get_schools_1213': "SELECT school_code, pincode, school_name, district, block_name, cluster_name, village_name from dise_1213_basic_data WHERE centroid IS NULL;",
'get_pincode_boundary': "SELECT wkb_geometry from postal where pincode=%(code)s;",
'get_ac': "SELECT ac_id, ac_name from assembly where ST_Contains(the_geom, %(pincode)s);",
'get_pc': "SELECT pc_id, const_name from parliament where ST_Contains(the_geom, %(pincode)s);",
'check_ac_intersect': "SELECT ac_id, ac_name, the_geom from assembly WHERE ST_Intersects(%(pincode)s, the_geom);",
'check_pc_intersect': "SELECT pc_id, const_name, the_geom from parliament WHERE ST_Intersects(%(pincode)s, the_geom);",
'get_ac_intersection': "SELECT ST_Intersection(the_geom, %(pincode)s) from assembly;",
'get_pc_intersection': "SELECT ST_Intersection(the_geom, %(pincode)s) from parliament;",
'get_intersection_area': "SELECT CAST(ST_Area(ST_Intersection(%(geom)s, %(pincode)s)) AS NUMERIC(10,4));",
'update_ac_name_1011': "UPDATE dise_1011_basic_data SET infered_assembly=%(assembly)s WHERE school_code=%(code)s",
'update_ac_name_1112': "UPDATE dise_1112_basic_data SET infered_assembly=%(assembly)s WHERE school_code=%(code)s",
'update_ac_name_1213': "UPDATE dise_1213_basic_data SET infered_assembly=%(assembly)s WHERE school_code=%(code)s",
'update_pc_name_1011': "UPDATE dise_1011_basic_data SET infered_parliament=%(parliament)s WHERE school_code=%(code)s",
'update_pc_name_1112': "UPDATE dise_1112_basic_data SET infered_parliament=%(parliament)s WHERE school_code=%(code)s",
'update_pc_name_1213': "UPDATE dise_1213_basic_data SET infered_parliament=%(parliament)s WHERE school_code=%(code)s",
'find_cluster_for_pincode_1011': "SELECT distinct cluster_name from dise_1011_basic_data WHERE pincode=%(pincode)s;",
'find_cluster_for_pincode_1112': "SELECT distinct cluster_name from dise_1112_basic_data WHERE pincode=%(pincode)s;",
'find_cluster_for_pincode_1213': "SELECT distinct cluster_name from dise_1213_basic_data WHERE pincode=%(pincode)s;",
'find_pincode_school_cluster_1011': "SELECT pincode from dise_1011_basic_data WHERE cluster_name=%(cluster)s;",
'find_pincode_school_cluster_1112': "SELECT pincode from dise_1112_basic_data WHERE cluster_name=%(cluster)s;",
'find_pincode_school_cluster_1213': "SELECT pincode from dise_1213_basic_data WHERE cluster_name=%(cluster)s;",
}

def infer_assembly(school, boundary):
  # If the boundary exists, try to find the assembly which contains it.
  cursor.execute(query['get_ac'], {'pincode': boundary[0]})
  ac = cursor.fetchall()
  if ac:
    assembly = ac[0][1]
    return assembly
  else:
    # If no assembly is contains the pin, check for intersection.
    cursor.execute(query['check_ac_intersect'], {'pincode': boundary[0]})
    intersects = cursor.fetchall()
    if intersects:
      # If intersects, calculate the area of blob for each intersection and pick the largest.
      areas = {}
      for intersection in intersects:
        cursor.execute(query['get_intersection_area'], {'geom':intersection[2], 'pincode': boundary[0]})
        blob = cursor.fetchall()
        areas[intersection[1]]=float(blob[0][0])
      assembly = max(areas.iteritems(), key=operator.itemgetter(1))[0]
      return assembly

def infer_parliament(school, boundary):
  # If the boundary exists, try to find the parliament which contains it.
  cursor.execute(query['get_pc'], {'pincode': boundary[0]})
  pc = cursor.fetchall()
  if pc:
    parliament = pc[0][1]
    return parliament
  else:
    # If no parliament is contains the pin, check for intersection.
    cursor.execute(query['check_pc_intersect'], {'pincode': boundary[0]})
    intersects = cursor.fetchall()
    if intersects:
      # If intersects, calculate the area of blob for each intersection and pick the largest.
      areas = {}
      for intersection in intersects:
        cursor.execute(query['get_intersection_area'], {'geom':intersection[2], 'pincode': boundary[0]})
        blob = cursor.fetchall()
        areas[intersection[1]]=float(blob[0][0])
      parliament = max(areas.iteritems(), key=operator.itemgetter(1))[0]
      return parliament

def enter_missing(school, year):
  # cursor.execute(query['get_schools_with_no_pin_'+year], {'pincode': pincode})
  # missing = cursor.fetchall()
  print school
  if year == '1011':
    notfound1011.writerow(school)
  elif year == '1112':
    notfound1112.writerow(school)
  else:
    notfound1213.writerow(school)
  
for year in years:
  print "Year", year
  # Get all schools without coordinates
  cursor.execute(query['get_schools_'+year])
  schools = cursor.fetchall()
  for school in schools:
    school_code = school[0]
    pincode = school[1]
    assembly = None
    print "Pincode", pincode
    # Get pincode boundary
    cursor.execute(query['get_pincode_boundary'], {'code': str(pincode)})
    pboundary = cursor.fetchall()
    if pboundary:
      assembly = infer_assembly(school, pboundary)
      print assembly
      cursor.execute(query['update_ac_name_'+year], {'assembly':assembly, 'code': school_code})
      parl = infer_parliament(school, pboundary)
      cursor.execute(query['update_pc_name_'+year], {'parliament':parl, 'code': school_code})
      print parl
    else:
      # Okay, no pincode boundary. It could just be a data entry issue.
      # Find clusters with the same pincode and if there's only one, pick a school and find it's pincode.
      # print "missing"
      cursor.execute(query['find_cluster_for_pincode_'+year], {'pincode':pincode})
      clusters = cursor.fetchall()
      if clusters.__len__() == 1:
        # If there's only one cluster, it is safe to pick a school and find the pincode.
        cursor.execute(query['find_pincode_school_cluster_'+year], {'cluster': clusters[0][0]})
        school_pincode = cursor.fetchall()
        cursor.execute(query['get_pincode_boundary'], {'code': str(pincode)})
        pboundary = cursor.fetchall()
        if pboundary:
          assembly = infer_assembly(school, pboundary)
          print assembly
          cursor.execute(query['update_ac_name_'+year], {'assembly':assembly, 'code': school_code})
          parl = infer_parliament(school, pboundary)
          cursor.execute(query['update_pc_name_'+year], {'parliament':parl, 'code': school_code})
          print parl
        else: 
          enter_missing(school, year) 
      else:
        enter_missing(school, year)

connection.commit()
cursor.close()
connection.close()