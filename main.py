import zipfile
import os.path
import hashlib
import requests
import re

directory_to_extract = R'C:\Users\EsdeathLover\PycharmProjects\LabaPython1\directory'
zip_file = r'C:\Users\EsdeathLover\PycharmProjects\LabaPython1\tiff-4.2.0_lab1.zip'

zip = zipfile.ZipFile(zip_file)
zip.extractall(directory_to_extract)
zip.close()

all_txt_files = []
for dirpath, dirnames, filenames in os.walk(directory_to_extract):
    for filename in filenames:
        #if filename[-4:0] == '.txt':
        if filename.endswith('.txt') == 1:
            all_txt_files.append(os.path.normpath(os.path.join(dirpath, filename)))
for txt_file in all_txt_files:
    txt_file_data = open(txt_file, 'rb').read()
    MD5_hash = hashlib.md5(txt_file_data).hexdigest()
    print("Name: ",txt_file," MD5 Hash: ",MD5_hash)

hash_target = "4636f9ae9fef12ebd56cd39586d33cfb"

for dirpath, dirnames, filenames in os.walk(directory_to_extract):
    for filename in filenames:
        file = os.path.join(dirpath, filename)
        file_data = open(file, 'rb').read()
        file_hash = hashlib.md5(file_data).hexdigest()
        if hash_target == file_hash:
            file_target_text = open(file, 'r').read()
            print("File: ",file," Link: ",file_target_text)

r = requests.get(file_target_text)
count = 0
result_dct = {}
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    if count == 0:
        headers = re.sub(R'(\<(/?[^\>]+)\>)', ';', line)
        headers = re.findall(r'[А-Яа-яёЁ]+\s?', headers)
        headers[3] = headers[3] + ' ' + headers[4]
        headers.pop(4)
        count += 1
        continue
    temp = re.sub(r'(\<(/?[^\>]+)\>)', ';', line)
    temp = re.sub(r'\([^)]*\)', '', temp)
    temp = re.sub(r'[A-Za-z]', '', temp)
    temp = temp[5:].strip()
    temp = re.sub(r'\;+', ';', temp)
    temp = re.sub(r'^;', '', temp)
    temp = re.sub(r';$', '', temp)
    temp = re.sub(r';В', 'В', temp)
    temp = re.sub(r'\*', '', temp)
    temp = re.sub(r'_', '0', temp)
    temp = re.sub(r'\xa0', '', temp)
    tmp_split = re.split(r';', temp)
    country_name = tmp_split[0]
    col1_val = tmp_split[1]
    col2_val = tmp_split[2]
    col3_val = tmp_split[3]
    col4_val = tmp_split[4]

    result_dct[country_name] = {}
    result_dct[country_name][headers[0]] = col1_val
    result_dct[country_name][headers[1]] = col2_val
    result_dct[country_name][headers[2]] = col3_val
    result_dct[country_name][headers[3]] = col4_val
    count += 1

table = open('data.csv', 'w')
count = 0
for key in result_dct.keys():
    if count == 0:
        table.write('Страна' + ' ; ' + ' ; '.join(headers) + '\n')
        count += 1
    table.write(key + " ; ")
    for i in range(0, 3):
        table.write(result_dct[key][headers[i]] + ' ; ')
    table.write(result_dct[key][headers[3]])
    table.write('\n')
table.close()

try:
    country = input("Enter name of the country: ")
    text = result_dct[country]
    print(text)
except KeyError:
    print("Unknown country")