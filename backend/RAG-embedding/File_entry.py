import os
import fitz
import PDF.PDF_To_Text as PDF_To_Text
import PDF.Scanned_PDF_To_Text as Scanned_PDF_To_Text
import PPT.PPT_To_Text as PPT_To_Text  
import DOCX.DOCX_To_Text as DOCX_To_Text
import Embedding_C.Text_To_Embeddings as Text_To_Embeddings
from embedding_config import get_embedding_config

def is_scanned_pdf(pdf_path):
    """Check if a PDF is scanned (mostly images) or contains real text."""
    doc = fitz.open(pdf_path)
    text_pages = 0

    for page in doc:
        text = page.get_text("text").strip()
        if text:
            text_pages += 1

    total_pages = len(doc)
    doc.close()

    return (text_pages / total_pages) < 0.3  # True if scanned

def process_file(file_path, generate_embeddings=True, output_base_name=None):
    """Detect file type and process accordingly."""
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return False
        
    ext = os.path.splitext(file_path)[1].lower()

    try:
        # Get the directory where this script is located (RAG-embedding folder)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        text_output_dir = os.path.join(script_dir, "Text_files")
        
        # Ensure Text_files directory exists
        os.makedirs(text_output_dir, exist_ok=True)
        
        # Use custom output name if provided, otherwise use original filename
        if output_base_name:
            base_filename = output_base_name
        else:
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # Step 1: Extract text from file
        print(f"📄 Extracting text from {os.path.basename(file_path)}...")
        
        if ext == ".pdf":
            if is_scanned_pdf(file_path):
                Scanned_PDF_To_Text.scanned_pdf_to_text(file_path, output_dir=text_output_dir, output_name=base_filename)
            else:
                PDF_To_Text.pdf_to_text(file_path, output_dir=text_output_dir, output_name=base_filename)

        elif ext in [".ppt", ".pptx"]:
            PPT_To_Text.ppt_to_text(file_path, output_dir=text_output_dir, output_name=base_filename)

        elif ext in [".doc", ".docx"]:
            DOCX_To_Text.docx_to_text(file_path, output_dir=text_output_dir, output_name=base_filename)

        else:
            print(f"❌ Unsupported file type: {ext}")
            return False
        
        print(f"✅ Text extraction completed for {os.path.basename(file_path)}")
        
        # Step 2: Generate embeddings if requested
        if generate_embeddings:
            text_file_path = os.path.join(text_output_dir, f"{base_filename}.txt")
            
            # Check if text file was created successfully
            if not os.path.exists(text_file_path):
                print(f"❌ Text file not found: {text_file_path}")
                return False
            
            print(f"🔄 Generating embeddings for {base_filename}...")
            
            try:
                # Get embedding configuration
                config = get_embedding_config()
                provider_type = config["provider"]
                provider_config = config["providers"][provider_type]
                
                # Set embeddings output directory
                embeddings_output_dir = os.path.join(script_dir, "Embeddings")
                os.makedirs(embeddings_output_dir, exist_ok=True)
                
                # Create embeddings from the text file
                embeddings_path = Text_To_Embeddings.text_to_embeddings(
                    text_file_path, 
                    embeddings_dir=embeddings_output_dir,
                    provider_type=provider_type,
                    **provider_config
                )
                print(f"✅ Embeddings generated: {os.path.basename(embeddings_path)}")
                
            except Exception as e:
                print(f"❌ Error creating embeddings: {e}")
                return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def main():
    """Main function to process file and create embeddings."""
    file_path = "Documents/CS_Module_01.pdf"
    
    print(f"🚀 Processing file: {file_path}")
    
    # Process the file (extract text + generate embeddings)
    if process_file(file_path, generate_embeddings=True):
        print(f"🎉 Process completed successfully!")
        
        # Show results
        base_filename = os.path.splitext(os.path.basename(file_path))[0]
        text_file_path = f"Text_files/{base_filename}.txt"
        embeddings_file_path = f"Embeddings/{base_filename}.json"
        
        if os.path.exists(text_file_path):
            print(f"📁 Text file: {os.path.abspath(text_file_path)}")
        if os.path.exists(embeddings_file_path):
            print(f"🔗 Embeddings: {os.path.abspath(embeddings_file_path)}")
    else:
        print("❌ Failed to process file.")

if __name__ == "__main__":
    main()