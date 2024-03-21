from OCR import text,text_2
from Names import fullnames,abbreviatednames
import re

def extract_possible_shortened_names(value):
    possible_shortened_names = re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+[-A-Z][-a-zA-Z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+[A-Z][a-z]+\b', value)
    return possible_shortened_names

def extract_possible_full_names(value):
    possible_full_names = re.findall(r'|\b[A-Z][a-z]+\b\s?[A-Z][a-z]+|[A-Z][a-z]+[A-Z][a-z]+\b\s?[A-Z][a-z]+[A-Z][a-z]+\b', value)
    return possible_full_names

def find_name_matches(value):
    full_names=fullnames()
    shortened_names=extract_possible_shortened_names(value)
    possible_full_names=extract_possible_full_names(value)
    extracted_full_names=list(set(fullnames()).intersection(possible_full_names))
    extracted_non_full_names=list(set(abbreviatednames()).intersection(shortened_names))
    locations=list(map(lambda x: abbreviatednames().index(x),extracted_non_full_names))
    print(str(locations))
    complete_names=[]
    for i in range(len(locations)):
        complete_names.append(full_names[locations[i]])
    all_names=extracted_full_names+complete_names
    return all_names


print("ALL: ",find_name_matches(text_2))


