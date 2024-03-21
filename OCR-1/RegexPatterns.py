from OCR import text,text_2
from Database import fullnames,abbreviatednames
import re
"""
initial_and_last_names=re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+\b', text)
print(initial_and_last_names)
non_mixed_case=re.findall(r'\b[A-Z][a-z]+\b\s?[A-Z][a-z]+', text)
#print(non_mixed_case)
mixed_case=re.findall(r'\b[A-Z][a-z]+[A-Z][a-z]+\b\s?[A-Z][a-z]+[A-Z][a-z]+\b',text)
#print(mixed_case)
all_case=non_mixed_case+mixed_case
print(all_case)

print("\n\n\n")
initial_and_last_names=re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+\b', text_2)
print(initial_and_last_names)
non_mixed_case=re.findall(r'\b[A-Z][a-z]+\b\s?[A-Z][a-z]+', text_2)
#print(non_mixed_case)
mixed_case=re.findall(r'\b[A-Z][a-z]+[A-Z][a-z]+\b\s?[A-Z][a-z]+[A-Z][a-z]+\b',text_2)
#print(mixed_case)
all_case=non_mixed_case+mixed_case
print(all_case)
"""

def extract_shortened_names(value1):
    possible_names = re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+\b', value1)
    return possible_names

def extract_full_names(value2):
    possible_names = re.findall(r'\b[A-Z][a-z]+[A-Z][a-z]+\b\s?[A-Z][a-z]+[A-Z][a-z]+\b', value2)
    possible_names=possible_names+re.findall(r'\b[A-Z][a-z]+[A-Z][a-z]+\b\s?[A-Z][a-z]+[A-Z][a-z]+\b',value2)
    return possible_names


def find_name_matches(value1, value2):
    search=value1, value2
    return search


test_list1 = [5, 7, 8, 9, 10, 11]
test_list2 = [8, 10, 11]

res = list(map(lambda x: test_list1.index(x), test_list2))
print("The matching element Indices list : " , res)
newarr=[]

i=len(res)
for i in res:
    newarr=res[i]
print(newarr)
print(test_list1[res[0]])