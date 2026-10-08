import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update meta tags to light only to disable Gmail's heuristic text inversion
html = re.sub(r'<meta name="color-scheme" content="[^"]*" />',
              '<meta name="color-scheme" content="light only" />', html)
html = re.sub(r'<meta name="supported-color-schemes" content="[^"]*" />',
              '<meta name="supported-color-schemes" content="light only" />', html)

# 2. Update :root in CSS
html = html.replace(':root { color-scheme: light dark; supported-color-schemes: light dark; }',
                    ':root { color-scheme: light only; supported-color-schemes: light only; }')

# 3. Update style block with -webkit-text-fill-color
html = html.replace('.c-white { color: #FFFFFE !important; }',
                    '.c-white { color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; }')
html = html.replace('.c-white-light { color: #e0d8d0 !important; }',
                    '.c-white-light { color: #e0d8d0 !important; -webkit-text-fill-color: #e0d8d0 !important; }')
html = html.replace('.c-mauve { color: #C49494 !important; }',
                    '.c-mauve { color: #C49494 !important; -webkit-text-fill-color: #C49494 !important; }')

html = html.replace('[data-ogsc] .c-white { color: #FFFFFE !important; }',
                    '[data-ogsc] .c-white { color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; }')
html = html.replace('[data-ogsc] .c-white-light { color: #e0d8d0 !important; }',
                    '[data-ogsc] .c-white-light { color: #e0d8d0 !important; -webkit-text-fill-color: #e0d8d0 !important; }')
html = html.replace('[data-ogsc] .c-mauve { color: #C49494 !important; }',
                    '[data-ogsc] .c-mauve { color: #C49494 !important; -webkit-text-fill-color: #C49494 !important; }')

# 4. Apple data detectors reset
old_detectors = 'a[x-apple-data-detectors], #MessageViewBody a { color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }'
new_detectors = 'a[x-apple-data-detectors], #MessageViewBody a { color: inherit !important; -webkit-text-fill-color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }'
html = html.replace(old_detectors, new_detectors)

old_body_a = 'u + #body a { color: inherit; text-decoration: none; font-size: inherit; font-family: inherit; font-weight: inherit; line-height: inherit; }'
new_body_a = 'u + #body a { color: inherit; -webkit-text-fill-color: inherit; text-decoration: none; font-size: inherit; font-family: inherit; font-weight: inherit; line-height: inherit; }'
html = html.replace(old_body_a, new_body_a)

# 5. Inline color: #FFFFFE -> color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;
# Replace every occurrence in style attributes
html = html.replace('color: #FFFFFE;', 'color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;')
html = html.replace('color: #C49494;', 'color: #C49494; -webkit-text-fill-color: #C49494;')

# 6. Add -webkit-text-fill-color to <strong> tags inside body copy
html = html.replace('<strong>The Goat</strong>',
                    '<strong style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">The Goat</strong>')
html = html.replace('<strong>cocktails and light bites</strong>',
                    '<strong style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">cocktails and light bites</strong>')
html = html.replace('<strong>guided hard hat tour</strong>',
                    '<strong style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">guided hard hat tour</strong>')
html = html.replace('<strong>step inside the project you&#8217;ve been hearing about</strong>',
                    '<strong style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">step inside the project you&#8217;ve been hearing about</strong>')

# 7. Protect the address links from Apple Blue Link tinting
old_addr1 = '1220 2nd Avenue North, Nashville, TN 37208'
new_addr1 = '<a href="https://maps.apple.com/?q=1220+2nd+Avenue+North+Nashville+TN+37208" target="_blank" style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; text-decoration: none;">1220 2nd Avenue North, Nashville, TN 37208</a>'
# Replace only the paragraph content one
html = html.replace(f'                {old_addr1}\n', f'                {new_addr1}\n')

old_addr2 = '1221 2ND AVE N, NASHVILLE, TN 37208'
new_addr2 = '<a href="https://maps.apple.com/?q=1221+2nd+Ave+N+Nashville+TN+37208" target="_blank" style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; text-decoration: none;">1221 2ND AVE N, NASHVILLE, TN 37208</a>'
html = html.replace(f'                {old_addr2}\n', f'                {new_addr2}\n')

# 8. Button inner text wrap with <span> for bulletproof text protection
html = html.replace(
    '                      RSVP TO ATTEND\n                    </a>',
    '                      <span style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">RSVP TO ATTEND</span>\n                    </a>'
)

html = html.replace(
    '                      SCHEDULE A PRIVATE PRESENTATION\n                    </a>',
    '                      <span style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">SCHEDULE A PRIVATE PRESENTATION</span>\n                    </a>'
)

# Save back to index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Applied complete dark mode hardening to index.html")
print("- color-scheme: light only (disables forced Gmail iOS inversion)")
print("- -webkit-text-fill-color: #FFFFFE on all text, strong tags, and buttons")
print("- Address link protection against iOS blue link tinting")
