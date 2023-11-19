# row_id: so thu tu cua hang trong sudoku (bat dau tu 1, duoc dung de in ra man hinh nen bat dau tu 1)
# col_id: so thu tu cua cot trong sudoku (bat dau tu 1, duoc dung de in ra man hinh nen bat dau tu 1)
def build_fixed_val_key(row_id, col_id): # tra ve 1 string duoc dung nhu la 1 key cho "fixed_values" dictionary
    return "[{}|{}]".format(str(row_id), str(col_id))

# grid_size(int): kich co 1 luoi cua sudoku (thong thuong la 3x3, grid_size = 3)
def build_separator_line(grid_size): # dung de xay dung 1 duong phan cach khi in sudoku len man hinh
    seps = '--' * grid_size # ------
    if grid_size > 3:
        seps += '----'
    separator_line = '{}-|'.format(seps) * grid_size # -------|-------|-------|
    return separator_line[:len(separator_line) - 1] # -------|-------|-------