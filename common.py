import os.path
import datetime

# Compares current date with file creation date
# If both match, return true, otherwise false
def cmp_dates(file_name: str) -> bool:
    file_creation_time = os.path.getctime(file_name)
    file_creation_time = datetime.datetime.fromtimestamp(file_creation_time)
    file_creation_date = file_creation_time.date()

    current_date = datetime.date.today()
    
    if current_date == file_creation_date:
         return True
    
    return False