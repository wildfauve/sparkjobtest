from pyspark.sql.types import StructType, StructField, StringType

at_id = StructField('id', StringType(), True)
at_type = StructField('type', StringType(), True)

type_id_label = StructType([
    at_id,
    at_type,
    StructField('label', StringType(), True)
])

type_id = StructType([
    at_id,
    at_type,
])

"""
sfo_position = pa.struct([at_type,
                          at_id,
                          pa_nav_datatime,
                          pa.field(l_get("Position_hasHeldPosition.fibo-sec-eq-eq:indicatesNumberOfShares"),
                                   pa_dec_20_6,
                                   metadata=term_meta(
                                       "Position_hasHeldPosition.fibo-sec-eq-eq:indicatesNumberOfShares")),
                          pa.field("fibo-fi-ip:hasPriceDeterminationMethod", pa_str),
                          pa.field("fibo-fnd-acc-cur:hasPrice", list_of_type_id_amt_curr)])

"""

position_has_held_position = StructType([
    at_id,
    at_type
])

schema = StructType([
    StructField('Portfolio', type_id_label, True),
    StructField('Position', type_id, True)
    # StructField('Position_hasHeldPosition', position_has_held_position, True)
])
