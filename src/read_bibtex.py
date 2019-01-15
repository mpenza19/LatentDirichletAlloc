import os, sys
import bibtexparser

def get_years():
    return [mydir for mydir in sorted(os.listdir('./abstracts')) if os.path.isdir('./abstracts/'+mydir)]

def get_bibtex_entries_by_year(year_dir):
    bibtex_entries = list()
    for page in os.listdir('./abstracts/'+year_dir):
        with open('./abstracts/'+year_dir+'/'+page) as bibtex_file:
            bibtex_entries += bibtexparser.load(bibtex_file).entries
    
    return bibtex_entries

def get_bibtex_entries_all():
    bibtex_entries = list()
    for year_dir in get_years():
        bibtex_entries.extend(get_bibtex_entries_by_year(year_dir))
    
    return bibtex_entries

def get_bibtex_entries_from(year_from):
    bibtex_entries = list()
    for year_dir in get_years():
        if year_from <= int(year_dir):
            bibtex_entries += get_bibtex_entries_by_year(year_dir)
    
    return bibtex_entries

def bibtex_tostring_single(bibtex_entry):
    return ("%s. %s. %s" % (bibtex_entry["title"], '; '.join(bibtex_entry["keywords"].split(';')), bibtex_entry["abstract"])).replace("<<ETX>>", "")

def bibtex_tostring_year(year_dir):
    return [bibtex_tostring_single(entry) for entry in get_bibtex_entries_by_year(year_dir)]
    
def bibtex_tostring_all():
    return [bibtex_tostring_single(entry) for entry in get_bibtex_entries_all()]

def bibtex_tostring_from(year_from):
    return [bibtex_tostring_single(entry) for entry in get_bibtex_entries_from(year_from)]
        
def main():
    if len(sys.argv) > 1:
        bibtex_entries = get_bibtex_entries_by_year(sys.argv[1])
        for entry in bibtex_entries:
            print bibtex_tostring_single(entry), '\n'

    else:
        for line in bibtex_tostring_all():
            print line, '\n'

#print len(get_bibtex_entries_all())