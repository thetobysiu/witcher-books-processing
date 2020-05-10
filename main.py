# SIU KING WAI SM4701 Deepstory
from parse import parse_book
import glob

books_list = glob.glob('books/*.epub')
books = [parse_book(book) for book in books_list]
texts = [chap for book in books for chap in book[1].values()]

start_token = "<|startoftext|>"
end_token = "<|endoftext|>"
with open('witcher.txt', 'w', encoding='utf-8') as f:
    for text in texts:
        f.write(start_token + text + end_token + "\n")

print('done')
