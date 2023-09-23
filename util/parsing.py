#!/usr/bin/env python3
from ply import lex
from ply import yacc
from .dataframes import *
import pandas as pd
import sys
import re
sys.path.append("..")


OPERATIONS = r'(PROJ|SELE|INTE|JOIN)'  # unused


def SELE(df: pd.DataFrame, column: str, value_to_match: any, operation: str) -> pd.DataFrame:
    if isinstance(value_to_match, str):
        try:
            value_to_match = int(value_to_match)
        except ValueError:
            pass

    if isinstance(value_to_match, str) and operation not in ['=', '!=']:
        raise ValueError('Can only use = and != for strings')

    if operation == '<=':
        return df.loc[df[column] <= value_to_match]
    elif operation == '>=':
        return df.loc[df[column] >= value_to_match]
    elif operation == '!=':
        return df.loc[df[column] != value_to_match]
    elif operation == '<':
        return df.loc[df[column] < value_to_match]
    elif operation == '>':
        return df.loc[df[column] > value_to_match]
    elif operation == '=':
        return df.loc[df[column] == value_to_match]
    else:
        raise ValueError('Unknown operation')


def process_cond(condition: str, which_comp: int = 1):
    '''
    Returns: column, comparison used, value to compare to
    '''
    if which_comp:
        condition = condition.split(',')[which_comp-1]
    comparisons = ['<=', '>=', '!=', '<',  '>',  '=']
    comp_used = ''
    for c in comparisons:
        comp_used = c if c in condition else ''
        if comp_used != '':
            break
    if comp_used == '':
        return 0
    column, compare_to = str(condition.split(comp_used)[0]).strip(), str(
        condition.split(comp_used)[1]).strip().replace('\'', '').replace('\"', '')
    return column, comp_used, compare_to


def operation_manager(operation: str, query: str):
    if operation == 'SELE':
        t, c, tbl = process_query(query)
        col_name, comp_used, value_comp = process_cond(c)
        sele_result = SELE(eval(f'{tbl.upper()}_DF'),
                           col_name, value_comp, comp_used)
        return sele_result
    if operation == 'PROJ':
        col_names = process_col_names(query)
        get_sele_q = query[query.index('(')+1:query.index(')')]
        sele_result = operation_manager('SELE', get_sele_q)
        PROJ(sele_result, col_names)
        return


def process_col_names(query: str) -> list[str]:
    strip = False
    try:
        query.index(',')
        columns = query[query.index('{')+1:query.index('}')].split(',')
        strip = True
    except ValueError:
        columns = query[query.index('{')+1:query.index('}')]
    return [entry.strip() for entry in columns] if strip else [str(columns)]


def PROJ(sele_df: pd.DataFrame, cols: list[str] = None):
    if cols == None:
        cols = sele_df.columns
    print(sele_df.loc[:, cols])


def process_query(query: str):
    query_type = re.match(r'\(?(PROJ|SELE|INTE|JOIN)', query[0:4]).string
    condition = query[query.index('{')+1:query.index('}')]
    print(query)
    query = query[query.index('SELE'):] if query_type == 'PROJ' else query
    try:
        find_paren = query.index(')')
    except ValueError:
        find_paren = len(query)
    on_table = query[query.index('(')+1: find_paren]
    print('Query type:', query_type)
    print(f'Query {"condition" if query_type == "SELE" else "columns" if query_type == "PROJ" else "?"}:', condition)
    print('Query on table:', query if query_type == 'PROJ' else on_table)
    return query_type, condition, on_table


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
