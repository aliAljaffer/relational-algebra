import os
import re
from sys import platform
from . import parsing as pars

import pandas as pd

os_separator = '\\' if platform == 'win32' else '/'


def txtToDataFrame(file_path: str) -> pd.DataFrame:
    with open(os.getcwd()+os_separator+file_path, 'r') as file:
        df = pd.read_csv(file, skipinitialspace=True)
        df.columns = df.columns.str.strip()
        return df


def findAll(df: pd.DataFrame, column: str, value_to_match: any, operation: str):
    return df.loc[df[column] == value_to_match]


def process_query(query: str):
    query_type = query[0:4]
    condition = query[6:query[7:].strip().index('}')+1]
    print('Query type:', query_type)
    print('Query condition:', condition)
    print()


def parse_query(query):
    # Define regular expressions to match various parts of the query
    # \(?(PROJ|SELE|INTE|JOIN)_\{([^}]*)\}\s+?\(\w+\s?[*]?\s?\w+?\)\)?
    # Catch operation, get condition, catch in parenthesis. check if theres operation
    # if there is, recurse. if not then catch table
    ra_operator_pattern = r'(PROJ|SELE|INTE|JOIN)'
    attributes_pattern = r'\{([^}]*)\}'
    table_name_pattern = r'\w+'

    # Extract the RA operator
    ra_operator_match = re.search(ra_operator_pattern, query)
    if ra_operator_match:
        ra_operator = ra_operator_match.group(1)
    else:
        raise ValueError("RA operator not found in the query.")

    # Extract attributes enclosed in curly braces (if any)
    attributes_match = re.search(attributes_pattern, query)
    if attributes_match:
        attributes = attributes_match.group(1).split(',')
    else:
        attributes = []

    # Extract table names
    table_names = re.findall(table_name_pattern, query)

    return ra_operator, attributes, table_names


ACTORS_DF = txtToDataFrame('ACTORS.txt')
MOVIES_DF = txtToDataFrame('MOVIES.txt')
PLAY_DF = txtToDataFrame('Play.txt')
QUERIES = open('RAqueries.txt', 'r')

r, a, t = parse_query(
    '(PROJ_{ANO} (SELE_{Payment > 70} (Play))) - (PROJ_{ANO} (SELE_{Payment < 60} (Play)))')
# print(t)
print(MOVIES_DF)
print(findAll(MOVIES_DF, 'MNO', 'M2', ''))
