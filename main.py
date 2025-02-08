import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import argparse


def scrape_epub(epub_path):
    book = epub.read_epub(epub_path)
    title = book.get_metadata("DC", "title")[0][0]
    sections = []
    plain_text = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            section_title = soup.find("h1") or soup.find("h2")
            section_title = (
                section_title.text.strip() if section_title else "Untitled Section"
            )
            section_text = soup.get_text(strip=True)

            # Remove the title from the beginning of the text using regex
            section_text = re.sub(
                f"^{re.escape(section_title)}", "", section_text, flags=re.IGNORECASE
            ).strip()

            sections.append({"title": section_title, "text": section_text})
            plain_text.append({"title": section_title, "text": section_text})

    return title, sections, plain_text


def main():
    parser = argparse.ArgumentParser(description="Scrape an EPUB file.")
    parser.add_argument("--epub-path", type=str, help="Path to the EPUB file.")
    parser.add_argument("--output-file", type=str, help="Path to the output file.")
    args = parser.parse_args()
    title, sections, plain_text = scrape_epub(args.epub_path)
    print(f"Book Title: {title}")
    print(f"Number of sections: {len(sections)}")
    print(f"Number of plain text entries: {len(plain_text)}")
    output_file = args.output_file
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in plain_text:
            f.write(f"= {entry['title']}\n{entry['text']}\n\n")


if __name__ == "__main__":
    main()
