# import pandas as pd

# df = pd.read_excel (r'C:\Users\MSI-PC\Desktop\Book1.xlsx')

# df = pd.read_excel (r'C:\Users\MSI-PC\Desktop\Book1.xlsx', index_col=0, dtype={'Name': str, 'Value': float}) 
# print (df)

# import tkinter as tk
# from tkinter import filedialog
# import pandas as pd

# root= tk.Tk()

# canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue')
# canvas1.pack()

# def getExcel ():
#     global df
    
#     import_file_path = filedialog.askopenfilename()
#     df = pd.read_excel (import_file_path)
#     print (df)

    
# browseButton_Excel = tk.Button(text='Import Excel File', command=getExcel, bg='green', fg='white', font=('helvetica', 12, 'bold'))
# canvas1.create_window(150, 150, window=browseButton_Excel)


# root.mainloop()


# Reading an excel file using Python 
import xlrd 
import openpyxl 

# Give the location of the file 
loc = ("Book1.xlsx") 

# To open Workbook 
# wb = xlrd.open_workbook(loc) 
# sheet = wb.sheet_by_index(0) 

wb = openpyxl.load_workbook(excel_file)
sheet = wb.sheetnames

# For row 0 and column 0 

for i in range(0,100):
    a=int(sheet.cell_value(i,0))
    b=int(sheet.cell_value(i,1))
    c=str(sheet.cell_value(i,5))
    d=str(sheet.cell_value(i,6))
    a=str(a)
    b=str(b)
    try:
        User.objects.create(username=b,password=b,first_name=c,last_name=d,is_student=True)
    except:
        pass


