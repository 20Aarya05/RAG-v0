import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract.exe"

def scanned_pdf_to_text(pdf_path, output_dir="Text_files", output_name=None):
    """
    Extract text from scanned PDFs including:
    - Normal text via OCR
    - Tables and diagrams (extract text from them)
    
    Saves a text file with the same base name in the output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = output_name if output_name else os.path.splitext(os.path.basename(pdf_path))[0]
    output_txt_path = os.path.join(output_dir, f"{base_name}.txt")

    doc = fitz.open(pdf_path)
    all_text = ""

    for i, page in enumerate(doc, start=1):
        print(f"🖼️ Converting page {i} to image...")
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # 1️⃣ OCR full page
        text = pytesseract.image_to_string(img, lang="eng")
        all_text += f"\n\n--- Page {i} ---\n{text.strip()}"

        # 2️⃣ Extract tables and structured text using pytesseract data
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        n_boxes = len(data['level'])
        table_text = ""
        for j in range(n_boxes):
            conf = int(data['conf'][j])
            if conf > 40:  # filter low-confidence OCR
                table_text += data['text'][j] + "\t"
            if data['text'][j] == "":
                table_text += "\n"
        if table_text.strip():
            all_text += "\n[Table/Text Layout Detected via OCR]:\n" + table_text.strip()

        # 3️⃣ Optionally, you can save diagrams/charts as separate images
        # img.save(f"{output_dir}/{base_name}_page_{i}.png")

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(all_text.strip())

    print(f"\n✅ OCR completed! Text saved to: {os.path.abspath(output_txt_path)}")
    return output_txt_path
