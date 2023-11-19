from sudoku import positions, s_utils

# Class PencilMark dung de danh dau nhung gia tri co the dien duoc o tung o trong trong sudoku
class PencilMark(object):
    _sudoku = None # single pre underscore is only meant to use for internal use. (bien co 1 gach duoi phia truoc la co y dinh chi dung cuc bo)
    
    def __init__(self, sudoku): # Constructor
        self._sudoku = sudoku
    
    def run(self): # Danh dau nhung gia tri co the dien duoc vao o trong trong sudoku (o trong duoc dai dien = '0'), ham nay se lap lai den khi khong con co the dien duoc them gia tri nao vao sudoku
        found_new = True
        while found_new:
            pencil_mark = self._run_one_iteration()
            new_values = self.generate_values_from_pencil(pencil_mark)
            found_new = new_values != self._sudoku.get_initial_values()
            self._sudoku.set_initial_values(new_values)

    def _run_one_iteration(self):
        """
        Moi cell trong sudoku se co 1 mang boolean, moi index cua mang se la gia tri co the dien duoc vao cell.
        Khoi tao mang, tat ca se co gia tri True, chay vong lap kiem tra dieu kien rang buoc, neu co gia tri khong the dien
        thi gia tri tai index se tro thanh False.
        Nhung o co gia tri duoc cho truoc thi tat cac index con lai se la False.
        """
        sudoku_size = self._sudoku.size()
        grid_size = self._sudoku.grid_size()
        # Khoi tao dict pencil mark voi tat ca gia tri la True
        pencil_mark = {}
        for i in range(sudoku_size):
            for j in range(sudoku_size):
                pencil_mark[s_utils.build_fixed_val_key(i, j)] = [True] * sudoku_size

        position = 0
        for character in self._sudoku.get_initial_values():
            digit = int(character)
            if digit != 0:
                row_id = positions.retrieve_row_id_from_position_and_size(position, sudoku_size)
                col_id = positions.retrieve_column_id_from_position_and_size(position, sudoku_size)
                grid_id = positions.retrieve_grid_id_from_row_and_col(row_id, col_id, grid_size)

                # Dat dieu kien cho cac o khac trong cung hang row_id, col_id vaf grid_id
                for i in range(sudoku_size):
                    key_row = s_utils.build_fixed_val_key(row_id, i)
                    key_col = s_utils.build_fixed_val_key(i, col_id)
                    pencil_mark[key_row][digit - 1] = False
                    pencil_mark[key_col][digit - 1] = False

                range_rows = positions.retrieve_range_rows_from_grid_id(grid_id, grid_size)
                range_cols = positions.retrieve_range_columns_from_grid_id(grid_id, grid_size)
                for i in range_rows:
                    for j in range_cols:
                        key_grid = s_utils.build_fixed_val_key(i, j)
                        pencil_mark[key_grid][digit - 1] = False
                
                # Tai vi tri o co dinh (da biet gia tri truoc) dat tat ca gia tri kha thi thanh False, va gia tri co dinh thanh True
                key_fixed = s_utils.build_fixed_val_key(row_id, col_id)
                pencil_mark[key_fixed] = [False] * sudoku_size
                pencil_mark[key_fixed][digit - 1] = True

            position += 1
        return pencil_mark
    
    @staticmethod # Su dung nhu 1 ham rieng biet va ko lien quan den class, mac du no duoc dinh nghia trong class
    def generate_values_from_pencil(pencil_mark):
        '''
        Dung de duyet qua dict pencil mark, de coi co gia tri moi nao co the dien vao sudoku duoc khong
        gia tri moi duoc dien vao chi khi mang boolean chi co 1 gia tri True duy nhat
        '''
        new_values = []
        for key, bool_arr in pencil_mark.items():
            indices = [i for i, x in enumerate(bool_arr) if x]
            if len(indices) == 1:
                new_values.append(int(indices[0]) + 1)
            else:
                new_values.append(0)
        return new_values