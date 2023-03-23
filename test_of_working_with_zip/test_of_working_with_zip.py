import zipfile
import requests
import PyPDF2
import openpyxl
import csv
import os

url_of_pdf = 'https://www.africau.edu/images/default/sample.pdf'
url_of_xlsx = 'https://www.cleverence.ru/files/36024/PARFUM-demo.xlsx'
url_of_csv = 'https://support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv'

pdf_path = os.path.basename(url_of_pdf)
xlsx_path = os.path.basename(url_of_xlsx)
csv_path = os.path.basename(url_of_csv)

def test_filed_download():
    response = requests.get(url_of_pdf)
    with open(f'resources/{pdf_path}', 'wb') as file_pdf:
        file_pdf.write(response.content)

    response = requests.get(url_of_xlsx)
    with open(f'resources/{xlsx_path}', 'wb') as file_xlsx:
        file_xlsx.write(response.content)

    response = requests.get(url_of_csv)
    with open(f'resources/{csv_path}', 'wb') as file_csv:
        file_csv.write(response.content)

def test_file_archiving():
    try:
        os.mkdir('resources')
    except:
        print('папка resources уже создана')

    path = './resources'
    with zipfile.ZipFile('all_files.zip', 'w') as zf:
        zf.write(f'{path}/{pdf_path}', 'pfg_file.pdf')
        zf.write(f'{path}/{csv_path}', 'csv_file.csv')
        zf.write(f'{path}/{xlsx_path}', 'xlsx_file.xlsx')

def test_pdf_read():
    with zipfile.ZipFile('all_files.zip') as zf:
        with zf.open('pfg_file.pdf', 'r') as open_zf:
            pdf_reader = PyPDF2.PdfReader(open_zf)
            num_pages = pdf_reader.getNumPages()
            assert num_pages == 2
            text = pdf_reader.pages[1].extract_text()
            assert 'Simple PDF File 2' in text, "No text in file"

def test_csv_read():
    with zipfile.ZipFile('all_files.zip') as zf:
        with zf.open('csv_file.csv') as csv_file:
            csv_reader = csv.reader((line.decode('utf-8') for line in csv_file))
            count_row = 0
            for row in csv_reader:
                count_row += 1
            assert 7 == count_row

def test_xlsx_read():
    with zipfile.ZipFile('all_files.zip') as zf:
        with zf.open('xlsx_file.xlsx', 'r') as xlsx_file:
            workbook = openpyxl.load_workbook(xlsx_file)
            sheet = workbook.active
            result = sheet.cell(row=7, column=6).value
            assert result == 'ДУШИСТЫЙ ОДЕКОЛОН КЛЕВЕРЕНС БЕЗ ЗАПАХОВ'