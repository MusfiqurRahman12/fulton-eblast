import pymupdf

doc = pymupdf.open('4559216753 - Fulton - Youre Invited Step Inside Fulton Eblast_v3.pdf')
page = doc[0]
print(f"Page rect: {page.rect}")

blocks = page.get_text('dict')['blocks']
for b in blocks:
    if 'lines' in b:
        for line in b['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                if text:
                    color_hex = f"#{span['color']:06x}"
                    bbox = [round(x, 1) for x in span['bbox']]
                    print(f"{bbox}: {span['font']} ({span['size']:.1f}pt) {color_hex} -> {text}")
