import datetime # Xem them o https://docs.python.org/3/library/datetime.html#

def get_human_readable_time(start_time, end_time): # Tra ve khoang thoi gian thuc thi chuong trinh
    return str(datetime.timedelta(seconds=(end_time - start_time)))

def count_duplicates(arr): # Tra ve so lan cac gia tri bi lap lai trong arr
    return len(arr) - len(set(arr)) # Set ko chua cac gia tri lap lai