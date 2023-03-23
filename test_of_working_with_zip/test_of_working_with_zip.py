import zipfile
import pytest
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
path_to_files = "./resources"

@pytest.fixture
def file_cleaning():
    try:
        os.mkdir('resources')
    except:
        print('папка resources уже создана')

    for file_name in os.listdir(path_to_files):
        try:
            os.remove(os.path.join(path_to_files, file_name))
        except:
            print(f"Файл {file_name} не найден")

@pytest.fixture
def file_download(file_cleaning):
    print("Setup file downloading")

    response = requests.get(url_of_pdf)
    with open(f'{path_to_files}/{pdf_path}', 'wb') as file_pdf:
        file_pdf.write(response.content)

    response = requests.get(url_of_xlsx)
    with open(f'{path_to_files}/{xlsx_path}', 'wb') as file_xlsx:
        file_xlsx.write(response.content)

    response = requests.get(url_of_csv)
    with open(f'{path_to_files}/{csv_path}', 'wb') as file_csv:
        file_csv.write(response.content)

@pytest.fixture()
def files_archiving(file_download):  # проверяет, существует ли архив с именем "all_files.zip" в директории, заданной переменной
    try:
        os.remove(f'{path_to_files}/all_files.zip')
    except:
        print('архив уже удален')

    with zipfile.ZipFile(f'{path_to_files}/all_files.zip', 'w') as zf:
        zf.write(f'{path_to_files}/{pdf_path}', 'pfg_file.pdf')
        zf.write(f'{path_to_files}/{csv_path}', 'csv_file.csv')
        zf.write(f'{path_to_files}/{xlsx_path}', 'xlsx_file.xlsx')

def test_pdf_read(files_archiving):
    with zipfile.ZipFile(f'{path_to_files}/all_files.zip') as zf:
        with zf.open('pfg_file.pdf', 'r') as open_zf:
            pdf_reader = PyPDF2.PdfReader(open_zf)
            num_pages = pdf_reader.getNumPages()
            assert num_pages == 2
            text = pdf_reader.pages[1].extract_text()
            assert 'Simple PDF File 2' in text, "No this in file"


def test_csv_read(files_archiving):
    with zipfile.ZipFile(f'{path_to_files}/all_files.zip') as zf:
        with zf.open('csv_file.csv') as csv_file:
            csv_reader = csv.reader((line.decode('utf-8') for line in csv_file))
            count_row = 0
            for row in csv_reader:
                count_row += 1
            assert 7 == count_row


def test_xlsx_read(files_archiving):
    with zipfile.ZipFile(f'{path_to_files}/all_files.zip') as zf:
        with zf.open('xlsx_file.xlsx', 'r') as xlsx_file:
            workbook = openpyxl.load_workbook(xlsx_file)
            sheet = workbook.active
            result = sheet.cell(row=7, column=6).value
            assert result == 'ДУШИСТЫЙ ОДЕКОЛОН КЛЕВЕРЕНС БЕЗ ЗАПАХОВ'
