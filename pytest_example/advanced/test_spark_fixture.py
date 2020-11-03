"""Test function in spark_fixture.py"""

import pytest

import spark_fixture

# Fixture comes from the conftest.py
def test_assert_rows_same(get_session):
    """Tests for assert_rows_same(a_sdf: SparkDF, b_sdf: SparkDF) -> None"""

    columns = ['letter', 'number']
    sdf = get_session.createDataFrame([('a', 1), ('b', 2)], columns)

    # Success, rows in different order
    sdf_rows_flipped = get_session.createDataFrame([('b', 2), ('a', 1)], columns)
    spark_fixture.assert_rows_same(sdf, sdf_rows_flipped)

    # Success, columns in different order
    sdf_backwards_columns = get_session.createDataFrame([('a', 1), ('b', 2)], columns[::-1])
    spark_fixture.assert_rows_same(sdf, sdf_backwards_columns)
    
    # Failure, rows are the same, but one sdf has an extra row of null
    sdf_extra_row = get_session.createDataFrame([('a', 1), ('b', 2), (None, None)], columns)
    with pytest.raises(AssertionError):
        spark_fixture.assert_rows_same(sdf, sdf_extra_row)
    
    # Failure, dataframe has value set to None when other DF is not None
    sdf_none = get_session.createDataFrame([('a', 1), ('b', None)], columns)
    with pytest.raises(AssertionError):
        spark_fixture.assert_rows_same(sdf, sdf_none)
    
    # Success, some rows contain None, but they are None in the same place
    sdf_another_none = get_session.createDataFrame([('a', 1), ('b', None)], columns)
    spark_fixture.assert_rows_same(sdf_none, sdf_another_none)