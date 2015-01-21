psql -U klp -h localhost -d klpdise_olap -f cluster_aggregation.sql
psql -U klp -h localhost -d klpdise_olap -f block_aggregation.sql
psql -U klp -h localhost -d klpdise_olap -f district_aggregation.sql
psql -U klp -h localhost -d klpdise_olap -f assembly_aggregation.sql
psql -U klp -h localhost -d klpdise_olap -f parliament_aggregation.sql
psql -U klp -h localhost -d klpdise_olap -f pincode_aggregation.sql
