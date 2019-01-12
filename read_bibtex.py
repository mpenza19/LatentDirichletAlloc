import bibtexparser
from os import listdir, path
import sys

def get_bibtex_entries_by_year(year_dir):
    bibtex_entries = list()
    for page in listdir('./abstracts/'+year_dir):
        with open('./abstracts/'+year_dir+'/'+page) as bibtex_file:
            bibtex_entries += bibtexparser.load(bibtex_file).entries
    
    return bibtex_entries

def get_bibtex_entries_all():
    bibtex_entries = list()
    for year_dir in [mydir for mydir in sorted(listdir('./abstracts')) if path.isdir('./abstracts/'+mydir)]:
        bibtex_entries += get_bibtex_entries_by_year(year_dir)
    
    return bibtex_entries

def print_bibtex(bibtex_entries):
    for entry in bibtex_entries:
        print "%s. %s\n" % (entry["title"], entry["abstract"])
        

def main():
    bibtex_entries = get_bibtex_entries_by_year(sys.argv[1]) if len(sys.argv) > 1 else get_bibtex_entries_all()
    print_bibtex(bibtex_entries)

main()


    




    

