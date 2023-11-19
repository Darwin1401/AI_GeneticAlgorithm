# goi nay duoc dung de tinh toan vi tri cua nhung phan tu trong mang 2 chieu phu thuoc vao kich co cua sudoku (9x9)
from random import shuffle # thay doi thu tu 1 cach ngau nhien cac phan tu trong trong 1 day lien tiep, vi du nhu list

# position(int): vi tri cua o trong sudoku (0 -> 80)
# size(int): kich co cua sudoku (size x size(9x9, size = 9))
def retrieve_row_id_from_position_and_size(position, size): # tra ve toa do x cua position
    return position // size # floor division, lam tron ket qua xuong

def retrieve_column_id_from_position_and_size(position, size): # tra ve toa do y cua position 
    return position % size

# row_id(int): toa do x cua position
# col_id(int): toa do y cua position
# grid_size(int): kich co 1 luoi cua sudoku (thong thuong la 3x3, grid_size = 3)
def retrieve_grid_id_from_row_and_col(row_id, col_id, grid_size): # tra ve so thu tu cua luoi 3x3 cua position (0 -> 8)
    return int(col_id // grid_size + ((row_id // grid_size) * grid_size))

# grid_id(int): so thu tu ve luoi 3x3 trong sudoku (0 -> 8)
def retrieve_range_rows_from_grid_id(grid_id, grid_size): # tra ve 1 range ((start, end) khong bao gom end) cac hang trong luoi 3x3 trong sudoku (VD: (0 -> 3), (3 -> 6), (6 -> 9))
    start = int(grid_id / grid_size) * grid_size
    return range(start, start + grid_size)

def retrieve_range_columns_from_grid_id(grid_id, grid_size):
    start = int(grid_id % grid_size) * grid_size
    return range(start, start + grid_size)

# grid_position (int): vi tri trong cai grid dang tinh (0 -> 8)
def retrieve_row_id_from_grid_id_and_position(grid_id, grid_position, grid_size): # tra ve toa do x (0 -> 8) cua sudoku khi biet position (0 -> 8) trong grid va size cua grid va grid_id
    row_in_grid = retrieve_row_id_from_position_and_size(grid_position, grid_size) # row_in_grid(int): (0 -> 2)
    delta_row = grid_size * (retrieve_row_id_from_position_and_size(grid_id, grid_size))
    return row_in_grid + delta_row

def retrieve_column_id_from_grid_id_and_position(grid_id, grid_position, grid_size): # tra ve toa do y (0 -> 8) cua sudoku khi biet position (0 -> 8) trong grid va size cua grid va grid_id
    col_in_grid = retrieve_column_id_from_position_and_size(grid_position, grid_size) # row_in_grid(int): (0 -> 2)
    delta_col = grid_size * (retrieve_column_id_from_position_and_size(grid_id, grid_size))
    return col_in_grid + delta_col

# array_to_fill: 1 mang, dai dien cho 1 grid 3x3, 1 hang hoac 1 cot trong sudoku
# length: kich thuoc cua array
def fill_with_some_valid_values(array_to_fill, length): # dien vao array nhung gia tri kha thi
    fixed_values = [value for value in array_to_fill if value > 0] # lay nhung gia tri cho truoc trong array
    fixed_index_values = [(pos, value) for pos, value in enumerate(array_to_fill) if value > 0] # lay vi tri va gia tri cua tung phan tu trong array
    available_values = [x for x in range(1, length+1) if x not in fixed_values] # lay nhung gia tri kha thi, dua tren nhung gia tri da cho truoc
    shuffle(available_values) # thay doi thu tu cua available_values 1 cach ngau nhien
    # Them nhung gia tri da cho truoc vao array da duoc shuffle
    for index, val in fixed_index_values:
        available_values.insert(index, val)
    return available_values # sau khi da them vao nhung gia tri kha thi 1 cach ngau nhien, va giu nguyen nhung gia tri da cho truoc