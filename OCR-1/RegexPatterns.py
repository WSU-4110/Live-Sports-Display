from OCR import text,text_2
import re
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

