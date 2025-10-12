import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract.exe"  

def pdf_to_text(pdf_path, output_dir="Text_files", output_name=None):
    """
    Extract text from normal PDFs including:
    - Direct text
    - Tables (roughly via text block positions)
    - Charts/diagrams (via OCR)
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = output_name if output_name else os.path.splitext(os.path.basename(pdf_path))[0]
    output_txt_path = os.path.join(output_dir, f"{base_name}.txt")

    doc = fitz.open(pdf_path)
    all_text = ""

    for page_num, page in enumerate(doc, start=1):
        all_text += f"\n\n--- Page {page_num} ---\n"

        # 1️⃣ Extract selectable text
        page_text = page.get_text("text")
        if page_text.strip():
            all_text += "[Text]:\n" + page_text.strip() + "\n"

        # 2️⃣ Roughly detect tables using text blocks (position-based)
        blocks = page.get_text("blocks")
        table_text = ""
        for block in blocks:
            x0, y0, x1, y1, block_text, block_type = block[:6]
            # Simple heuristic: multiple lines close together horizontally → table
            lines = block_text.strip().split("\n")
            if len(lines) > 1 and "\t" in lines[0] or len(lines[0].split()) > 1:
                table_text += "\n".join(lines) + "\n"
        if table_text.strip():
            all_text += "[Table Detected]:\n" + table_text.strip() + "\n"

        # 3️⃣ Extract text from images (charts/diagrams) via OCR
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        ocr_text = pytesseract.image_to_string(img, lang="eng")
        if ocr_text.strip():
            all_text += "[Text in Images (Charts/Diagrams)]:\n" + ocr_text.strip() + "\n"

    doc.close()

    # Save output
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(all_text.strip())

    print(f"\n✅ Extraction complete! Text saved to: {os.path.abspath(output_txt_path)}")
    return output_txt_path
