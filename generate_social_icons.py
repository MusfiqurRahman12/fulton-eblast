"""
Extract exact vector icons from PDF for Facebook and Instagram.
Renders transparent PNGs at 4x retina (104x104px for 26x26px display)
using the exact vector path instructions from the PDF.
"""
import pymupdf
from PIL import Image
import os

PDF_PATH = "4559216753 - Fulton - Youre Invited Step Inside Fulton Eblast_v3.pdf"
ASSETS_DIR = "assets"

doc = pymupdf.open(PDF_PATH)
page = doc[0]

fb_drawings = [d for d in page.get_drawings() if 1910 <= d['rect'].y0 <= 1940 and d['rect'].x1 < 300]
ig_drawings = [d for d in page.get_drawings() if 1910 <= d['rect'].y0 <= 1940 and d['rect'].x1 > 300]

def render_vector_icon(drawings, out_name, target_size=104):
    bbox = pymupdf.Rect()
    for d in drawings:
        bbox.include_rect(d['rect'])
    
    # Padding of 1.0pt corresponds to half stroke-width (1.843 / 2 = 0.92pt) + safety
    pad = 1.2
    bbox.x0 -= pad
    bbox.y0 -= pad
    bbox.x1 += pad
    bbox.y1 += pad
    
    size = max(bbox.width, bbox.height)
    cx = (bbox.x0 + bbox.x1) / 2
    cy = (bbox.y0 + bbox.y1) / 2
    
    new_doc = pymupdf.open()
    new_page = new_doc.new_page(width=size, height=size)
    shape = new_page.new_shape()
    ox, oy = cx - size/2, cy - size/2
    
    for d in drawings:
        for item in d['items']:
            cmd = item[0]
            pts = [pymupdf.Point(p.x - ox, p.y - oy) for p in item[1:]]
            if cmd == 'l':
                shape.draw_line(pts[0], pts[1])
            elif cmd == 'c':
                shape.draw_bezier(pts[0], pts[1], pts[2], pts[3])
            elif cmd == 're':
                r = pymupdf.Rect(pts[0].x - ox, pts[0].y - oy, pts[1].x - ox, pts[1].y - oy)
                shape.draw_rect(r)
        
        stroke_color = (1.0, 1.0, 1.0) if d.get('color') else None
        fill_color = (1.0, 1.0, 1.0) if d.get('fill') else None
        width = d.get('width', 1.0) if stroke_color else 0
        
        lj = d.get('lineJoin')
        line_join = int(lj) if lj is not None else 0
        
        lc = d.get('lineCap')
        line_cap = lc[0] if isinstance(lc, tuple) else (int(lc) if lc is not None else 0)
        
        shape.finish(
            color=stroke_color,
            fill=fill_color,
            width=width,
            lineCap=line_cap,
            lineJoin=line_join,
            closePath=True
        )
    
    shape.commit()
    
    # Render at high DPI (600 DPI gives ~215px)
    pix = new_page.get_pixmap(dpi=600, alpha=True)
    temp_path = os.path.join(ASSETS_DIR, f"_temp_{out_name}")
    pix.save(temp_path)
    
    # Resize with high-quality Lanczos to exact target_size (104x104 = 4x retina for 26px)
    img = Image.open(temp_path)
    resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    out_path = os.path.join(ASSETS_DIR, out_name)
    resized.save(out_path, "PNG", optimize=True)
    os.remove(temp_path)
    
    sz = os.path.getsize(out_path)
    print(f"Generated {out_path}: {resized.width}x{resized.height} ({sz} bytes)")
    return out_path

# Generate FB icons
render_vector_icon(fb_drawings, "icon-fb-2x.png", 104)
render_vector_icon(fb_drawings, "icon-facebook.png", 104)

# Generate IG icons
render_vector_icon(ig_drawings, "icon-ig-2x.png", 104)
render_vector_icon(ig_drawings, "icon-instagram.png", 104)

print("Social icons generation complete!")
