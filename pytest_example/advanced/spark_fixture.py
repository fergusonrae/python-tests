"""Functions for testing if two spark DataFrames are the same."""

from pyspark.sql import DataFrame as SparkDF

def assert_rows_same(a_sdf: SparkDF, b_sdf: SparkDF) -> None:
    """Asserts that both sdfs contain the same rows.
    Does not care about column order or row order"""
    # Sort the columns first as subtract is sensitive to that
    for sdf in [a_sdf, b_sdf]:
        sdf = sdf.select(sorted(sdf.columns))

    # Subtract the sdfs
    not_in_a = b_sdf.subtract(a_sdf).count()
    not_in_b = a_sdf.subtract(b_sdf).count()
    if (not_in_a != 0) or (not_in_b != 0):
        raise AssertionError("""
    One or both of the sdfs have rows that the other does not.
    Ther are not identical.
    Count of rows in a_sdf but not b_sdf: {not_b}
    Count of rows in b_sdf but not a_sdf: {not_a}
    """.format(not_a=not_in_a, not_b=not_in_b))