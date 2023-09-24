
import os
import pandas as pd

from sys import platform
os_separator = '\\' if platform == 'win32' else '/'


def txtToDataFrame(file_path: str) -> pd.DataFrame:
    with open(os.getcwd()+os_separator+file_path, 'r') as file:
        df = pd.read_csv(file, skipinitialspace=True)
        df.columns = df.columns.str.strip()
        return df


ACTORS_DF = txtToDataFrame('ACTORS.txt')
MOVIES_DF = txtToDataFrame('MOVIES.txt')
PLAY_DF = txtToDataFrame('Play.txt')


def DataFrame_to_csv(df: pd.DataFrame):
    df.to_csv('..{os_separator}outputs{os_separator}RAoutput.csv')
