JOB_URN_BASE = "urn:sparkjob:cborBuilder"


#
# DB and Tables
#
database_name = "dataProduct_cbor"
cbor_table = "cbor"
manifest_table = "jobManifest"
cbor_table_fully_qualified = "{}.{}".format(database_name, cbor_table)
manifest_table_fully_qualified = "{}.{}".format(database_name, manifest_table)


#
# Batch Config
#
dbfs = "/dbfs"
batch_source_folder = "{}/FileStore/cbor/batch".format(dbfs)


