## Intro
Extract epub files using beautifulsoup parser and filter content such as quote and some non-witcher related contents.

Create a dictionary structure separating sentences, chapters, and books.

Outputs a txt file with GPT-2 <|endoftext|> token prepended to each chapter/books.

## Steps
Run main.py to create witcher.txt

parse.py is the module for parsing the books, it will read epubs inside books/ folder, the epubs must be uncompressed and original.

Jupyter notebook is available.