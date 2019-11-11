update dise_1718_basic_data set centroid=data.centroid from (select centroid, school_code as disecode from dise_1617_basic_data) as data where data.disecode =school_code;
update dise_1718_assembly_aggregations set centroid=data.centroid from (select centroid, slug as dataslug from dise_1617_assembly_aggregations) as data where data.dataslug=slug;
update dise_1718_block_aggregations set centroid=data.centroid from (select centroid, slug as dataslug from dise_1617_block_aggregations) as data where data.dataslug=slug;
update dise_1718_cluster_aggregations set centroid=data.centroid from (select centroid, slug as dataslug from dise_1617_cluster_aggregations) as data where data.dataslug=slug;
update dise_1718_district_aggregations set centroid=data.centroid from (select centroid, slug as dataslug from dise_1617_district_aggregations) as data where data.dataslug=slug;
update dise_1718_parliament_aggregations set centroid=data.centroid from (select centroid, slug as dataslug from dise_1617_parliament_aggregations) as data where data.dataslug=slug;
update dise_1718_pincode_aggregations set centroid=data.centroid from (select centroid, slug as dataslug from dise_1617_pincode_aggregations) as data where data.dataslug=slug;
