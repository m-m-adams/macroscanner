#! python3
# look through all pdfs in current directory for specific keywords

# Imports
import os, shutil


keywords = []
with open('./keywords.txt', 'r') as words:
    for word in words.readlines():
        keywords.append(word.strip('\n'))

def pdf_cond(file):
    if file.endswith(".pdf"):
        return True
    return False

# Loop over the files in the working directory, looking only for pdfs
def triagePDF(file):
    with open(file, 'rb') as pdf:
        hits = [keyword.encode('utf-8') in pdf.read() for keyword in keywords]
        if any(hits):
            matches = [keyword for keyword, hit in zip(keywords, hits) if hit]
            print(file, matches)

