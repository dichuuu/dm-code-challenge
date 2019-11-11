import dosing
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def registry_df():
    """
        Returns an example Registry dataframe
    """
    data = [[1, 1, 'USER1', 'sc', 'Y'],
            [2, 1, 'USER1', 'bl', 'Y'],
            [3, 1, 'USER1', 'w02', '-4'],
            [4, 2, 'USER2', 'sc', 'Y'],
            [5, 2, 'USER2', 'bl', 'Y'],
           ]
    headers = ['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE']

    return pd.DataFrame(data, columns=headers)

@pytest.fixture
def ec_df():
    """
        Returns an example EC dataframe
    """
    data = [[1, 1, 'USER1', 'sc', 140],
            [2, 1, 'USER1', 'bl', 0],
            [3, 1, 'USER1', 'w02', 280],
            [5, 3, 'USER3', 'sc', 140],
            [5, 3, 'USER3', 'bl', 280],
           ]
    headers = ['ID', 'RID', 'USERID', 'VISCODE', 'ECSDSTXT']
    return pd.DataFrame(data, columns=headers)

@pytest.fixture
def merged_df():
    """
        Returns the expected merged dataframe
    """
    data = [[1, 1, 'USER1', 'sc', 'Y', 1, 'USER1', 140],
            [2, 1, 'USER1', 'bl', 'Y', 2, 'USER1', 0],
            [3, 1, 'USER1', 'w02', '-4', 3, 'USER1', 280],
            [4, 2, 'USER2', 'sc', 'Y', np.nan, np.nan, np.nan],
            [5, 2, 'USER2', 'bl', 'Y', np.nan, np.nan, np.nan],
           ]
    headers = ['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE', 'ID_ec', 'USERID_ec', 'ECSDSTXT']
    return pd.DataFrame(data, columns=headers)

def test_merge_dataframes(registry_df, ec_df, merged_df):
    df = dosing.merge_dataframes(registry_df, ec_df)
    assert df.equals(merged_df)

def test_filter_dataframe(merged_df):
    viscode = 'sc'
    svdose = 'Y'
    ecsdstxt = 280
    df = dosing.filter_dataframe(merged_df, viscode, svdose, ecsdstxt)

    errors = []
    if df.shape[0] != 2:
        errors.append("Length incorrect")
    if df.loc[0, 'VISCODE'] != viscode:
        errors.append("VISCODE filter incorrect")
    if df.loc[0, 'SVDOSE'] != svdose:
        errors.append("SVDOSE filter incorrect")
    if df.loc[0, 'ECSDSTXT'] == ecsdstxt:
        errors.append("ECSDSTXT filter incorrect")
    assert not errors
