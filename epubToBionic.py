from ebooklib import epub
from bs4 import BeautifulSoup, NavigableString
import re
import warnings
import os
import zipfile
import shutil

# Ignorer les avertissements pour une exécution propre
warnings.filterwarnings('ignore', category=UserWarning, module='ebooklib')
warnings.filterwarnings('ignore', category=FutureWarning, module='ebooklib')

def bionic_reading(text):
    def transform_word(word):
        word_length = len(word)
        
        if word_length <= 2 :
            # Toutes les lettres en gras pour les mots de 2  lettres
            return f'<b>{word}</b>'
        elif word_length >= 3 and word_length <= 5:
            # Les 2 premières lettres en gras pour les mots de 3 à 5 lettres
            return f'<b>{word[:2]}</b>{word[2:]}'
        elif word_length == 6:
            # Les 3 premières lettres en gras pour les mots de 6 lettres
            return f'<b>{word[:3]}</b>{word[3:]}'
        elif word_length == 7:
            # Les 4 premières lettres en gras pour les mots de 7 lettres
            return f'<b>{word[:4]}</b>{word[4:]}'
        elif word_length == 8:
            # Les 4 premières lettres en gras pour les mots de 8 lettres
            return f'<b>{word[:4]}</b>{word[4:]}'
        elif word_length == 9:
            # Les 5 premières lettres en gras pour les mots de 9 lettres
            return f'<b>{word[:5]}</b>{word[5:]}'
        elif word_length >= 10:
            # Les 5 premières lettres en gras pour les mots de 10 et + lettres
            return f'<b>{word[:5]}</b>{word[5:]}'
        else:
            # Par défaut, toutes les lettres sont normales
            return f'word'

    return re.sub(r'\b\w+\b', lambda m: transform_word(m.group()), text)

def process_soup(soup):
    for elem in soup.find_all(string=True):
        if isinstance(elem, NavigableString):
            bionic_text = bionic_reading(elem)
            elem.replace_with(BeautifulSoup(bionic_text, 'html.parser'))

def clean_generated_html(html_content):
    # Supprimer spécifiquement la séquence indiquée
    cleaned_content = re.sub(r'<b>xm</b>l <b>vers</b>ion=\'<b>1</b>.<b>0</b>\' <b>enco</b>ding=\'<b>ut</b>f-<b>8</b>\'\?', '', html_content)
    return cleaned_content


def create_bionic_epub(input_path, output_path):
    book = epub.read_epub(input_path)
        
    # Vérifier et définir l'UID s'il est manquant
    if not book.uid:
        book.set_identifier('urn:uuid:12345678-1234-5678-1234-567812345678')
        
    # Parcourir tous les éléments du livre EPUB
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            print(f"Modifying file {item.file_name}")
            
            # Extraire le contenu HTML original avec BeautifulSoup
            soup = BeautifulSoup(item.content, 'html.parser')
            
            # Extraire les métadonnées du document original
            head = soup.find('head')
            if head:
                head_content = str(head)
            else:
                head_content = '<head></head>'
            
            # Traiter le contenu textuel pour la lecture bionique
            process_soup(soup)
            cleaned_content = clean_generated_html(str(soup))
            
            # Réassembler le HTML avec les métadonnées et le contenu modifié
            new_content = f'<!DOCTYPE html><html><meta charset="utf-8">{head_content}<body>{cleaned_content}</body></html>'
            
            # Mettre à jour le contenu de l'élément EpubHtml avec le nouveau contenu
            item.content = new_content
    
    # Écrire le nouvel EPUB en conservant la structure originale
    epub.write_epub(output_path, book, {})
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python epubToBionic.py <input_epub> <output_epub>")
        sys.exit(1)
    
    input_epub = sys.argv[1]
    output_epub = sys.argv[2]
    
    create_bionic_epub(input_epub, output_epub)
    print(f"Bionic reading EPUB saved to {output_epub}")
