# SIU KING WAI SM4701 Deepstory
from ebooklib import epub
from bs4 import BeautifulSoup, NavigableString


def parse_book(path):
    book = epub.read_epub(path)
    spine_list = [x[0] for x in book.spine]
    chapter_list = []
    for i, x in enumerate(spine_list):
        if 'chapter' in x or 'epilogue' in x:
            if chapter_list:
                if spine_list.index(chapter_list[-1]) + 1 == i:
                    chapter_list.append(x)
            else:
                chapter_list.append(x)
    chapters = [
        BeautifulSoup(book.get_item_with_id(chapter).get_content(), 'lxml')
        for chapter in chapter_list
    ]

    book_dict = {}
    chapter_number = ''
    chapter_title = ''
    alt_mode = False
    for chapter in chapters:
        content = []
        sect = ''
        for tag in chapter.find('section'):
            if type(tag) is not NavigableString:
                if tag.text and tag.text != '\n' and tag.text != '\xa0':
                    tag_classes = tag.get('class', [])
                    if any('part-title' in x for x in tag_classes):
                        alt_mode = True
                        chapter_title = tag.text
                        if chapter_title not in book_dict:
                            book_dict[chapter_title] = []
                    elif any('chapter-number' in x for x in tag_classes):
                        if alt_mode:
                            if chapter_number != tag.text and content:
                                content = []
                            chapter_number = tag.text
                        else:
                            chapter_title = tag.text
                            if chapter_title not in book_dict:
                                book_dict[chapter_title] = []
                    elif any('chapter-title' in x for x in tag_classes):
                        if chapter_title:
                            del book_dict[chapter_title]
                        chapter_title = tag.text
                        if chapter_title not in book_dict:
                            book_dict[chapter_title] = []
                    elif any('sect1' in x for x in tag_classes):
                        if sect != tag.text and content:
                            book_dict[chapter_title].append('\n'.join(content))
                            content = []
                        sect = tag.text
                    elif any(any(y in x for y in ['chap', 'epigraph', 'page-break', 'pb'])
                             for x in tag_classes
                             ) or any([tag.select(f'[class*="{x}"]')
                                       for x in ['attribution', 'decoration-rw10', 'dl']]):
                        pass
                    else:
                        content.append(tag.text)
        if chapter_title:
            book_dict[chapter_title].append('\n'.join(content))
            if not alt_mode:
                chapter_title = ''

    book_title = book.get_metadata('DC', 'title')[0][0]
    book_dict = {key: '\n'.join(value) for key, value in book_dict.items()}
    return book_title, book_dict
