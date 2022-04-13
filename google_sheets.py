import gspread

from settings import CREDENTIALS, SHEET_ID

SERVICE = gspread.service_account_from_dict(CREDENTIALS)
SHEET = SERVICE.open_by_key(SHEET_ID)
WORKSHEET = SHEET.get_worksheet(0)


def get_numeric_list(input_list):
    output_list = []
    for i in input_list:
        try:
            output_list.append(float(i))
        except:
            pass
    return output_list


def get_total_revenue():
    values_list = WORKSHEET.col_values(3, 'UNFORMATTED_VALUE')
    return sum(get_numeric_list(values_list))


def add_row(values_list):
    WORKSHEET.insert_row(values_list, 2)
