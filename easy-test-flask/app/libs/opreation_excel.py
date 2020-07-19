import xlrd


class OperationExcel:
    def __init__(self, file_path):
        self.workbook = xlrd.open_workbook(file_path)
        self.table = None
        self.rowNum = 0
        self.colNum = 0

    def get_table(self, sheet_name=None, sheet_id=0):
        self.table = self.workbook.sheets()[sheet_id]
        if sheet_name:
            self.table = self.workbook.sheet_by_name(sheet_name)

    def get_rowNum(self):
        self.rowNum = self.table.nrows

    def get_colNum(self):
        self.colNum = self.table.ncols

    def get_cell_value(self, x, y):
        cell_value = self.table.cell_value(x, y)
        return cell_value
