JOB_URN_BASE = "urn:sparkjob:cborBuilder"

dbfs = "/dbfs"
database_name = "dataProduct_cbor"
batch_table = "batch"
graph_table = "graph"
manifest_table = "jobManifest"
batch_table_fully_qualified = "{}.{}".format(database_name, batch_table)
graph_table_fully_qualified = "{}.{}".format(database_name, graph_table)
manifest_table_fully_qualified = "{}.{}".format(database_name, manifest_table)
