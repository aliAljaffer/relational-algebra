import re
from util.parsing import *
import pandas as pd


file = open('RAqueries.txt', 'r')
QUERIES = [line.strip() for line in file.readlines() if line.strip()]
file.close()

# process_query('SELE_{FUN > 50}(EMPLOYEE)')
# r, a, t = parse_query(
# '(PROJ_{ANO} (SELE_{Payment > 70} (Play))) - (PROJ_{ANO} (SELE_{Payment < 60} (Play)))')
# print(QUERIES[1])
t, c, tbl = process_query(QUERIES[1])

df = operation_manager(t, QUERIES[1])
print(df)
# col_name, comp_used, value_comp = process_cond(c)
# sele_res = SELE(eval(f'{tbl.upper()}_DF'), col_name, value_comp, comp_used)
# print(sele_res)

# PROJ(sele_res, col_name)
# print(t)
# print(MOVIES_DF)
# print(MOVIES_DF['MNAME'].values)
# dd = findAll(
# MOVIES_DF, 'MNO', 'M2', '=')
# print(dd)
# # print(findAll(PLAY_DF, 'Payment', 80, '<'))
# all_m2_with_payment_lessthan_80 = SELE(
#     SELE(PLAY_DF, 'Payment', 80, '<'), 'MNO', 'M2', '=')
# print(all_m2_with_payment_lessthan_80)
