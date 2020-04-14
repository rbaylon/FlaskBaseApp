import openpyxl

class Reader(object):
    def __init__(self, filename):
        xl = openpyxl.load_workbook(filename)
        self.active_sheet = xl.active
        self.workbook = xl

    def getSheetData(self, sheetname=None):
        if sheetname:
            sheet = self.workbook[sheetname]
            data = sheet.rows
        else:
            data = self.active_sheet.rows

        return data


