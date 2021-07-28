from enum import Enum

TOKEN = '1936004153:AAE8o5qpDufsFqU9Pg94FgJ2w3B9s6J5kUA'
db_file = 'database.vdb'

class States(Enum):
    S_START = '0'
    S_ENTER_NAME_1 = '1'
    S_ENTER_NAME_2 = '2'
    S_ENTER_PEOPLE_1 = '3'
    S_ENTER_PEOPLE_2 = '4'
    S_ENTER_NUMBER_1 = '5'
    S_ENTER_NUMBER_2 = '6'
    S_USER = '7'