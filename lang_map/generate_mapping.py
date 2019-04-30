import csv

FILE="iso-639-3_20190408.tab"

print("# data taken from")
print("# https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Code_Tables_20190408.zip")
print("LANGUAGE_MAPPING_ISO_639_3_to_1 = {")
with open(FILE) as fp:
    reader = csv.DictReader(fp, delimiter='\t')
    first = True
    for row in reader:
        if row['Part1']:
            if first:
                first = False
            else:
                print(',')
            print('    "{Id}": "{Part1}"'.format(**row), end='')
print("}")
print("")
print("LANGUAGE_MAPPING_ISO_639_1_to_3 = {")
with open(FILE) as fp:
    reader = csv.DictReader(fp, delimiter='\t')
    first = True
    for row in reader:
        if row['Part1']:
            if first:
                first = False
            else:
                print(',')
            print('    "{Part1}": "{Id}"'.format(**row), end='')
print("}")
