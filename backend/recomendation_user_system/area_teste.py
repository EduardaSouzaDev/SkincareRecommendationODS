import re

string2 = 'Pure One Step Sun Camellia Cleansing Oil'
string1 = 'Oil-Free Sun Guard Sunscreen Water Resistant SPF 45'

str1_splitted = re.split('[-,./ \'%]', string1)
for string in str1_splitted:
    if string in string2:
        print(string)

#print(str1_splitted)