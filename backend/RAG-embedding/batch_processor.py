import os
import glob
from File_entry import process_file
import Embedding_C.Text_To_Embeddings as Text_To_Embeddings

def process_all_documents(documents_dir="Documents"):
    """
    Process all supported documents in the Documents directory.
    
    Args:
        documents_dir (str): Directory containing documents to process
    """
    if not os.path.exists(documents_dir):
        print(f"❌ Documents directory not found: {documents_dir}")
        return
    
    # Supported file extensions
    supported_extensions = ["*.pdf", "*.docx", "*.doc", "*.pptx", "*.ppt"]
    
    processed_files = []
    failed_files = []
    
    print(f"🔍 Scanning {documents_dir} for supported documents...")
    
    # Find all supported files
    all_files = []
    for ext in supported_extensions:
        pattern = os.path.join(documents_dir, ext)
        all_files.extend(glob.glob(pattern))
    
    if not all_files:
        print(f"❌ No supported documents found in {documents_dir}")
        return
    
    print(f"📁 Found {len(all_files)} document(s) to process")
    
    for file_path in all_files:
        print(f"\n{'='*60}")
        print(f"🔄 Processing: {os.path.basename(file_path)}")
        print(f"{'='*60}")
        
        try:
            # Process file to extract text
            if process_file(file_path):
                # Create embeddings
                base_filename = os.path.splitext(os.path.basename(file_path))[0]
                text_file_path = f"Text_files/{base_filename}.txt"
                
                if os.path.exists(text_file_path):
                    embeddings_path = Text_To_Embeddings.text_to_embeddings(text_file_path)
                    processed_files.append({
                        'original': file_path,
                        'text': text_file_path,
                        'embeddings': embeddings_path
                    })
                    print(f"✅ Successfully processed: {os.path.basename(file_path)}")
                else:
                    failed_files.append(file_path)
                    print(f"❌ Text file not created for: {os.path.basename(file_path)}")
            else:
                failed_files.append(file_path)
                print(f"❌ Failed to process: {os.path.basename(file_path)}")
                
        except Exception as e:
            failed_files.append(file_path)
            print(f"❌ Error processing {os.path.basename(file_path)}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successfully processed: {len(processed_files)} files")
    print(f"❌ Failed to process: {len(failed_files)} files")
    
    if processed_files:
        print(f"\n📁 Successfully processed files:")
        for file_info in processed_files:
            print(f"  • {os.path.basename(file_info['original'])}")
    
    if failed_files:
        print(f"\n❌ Failed files:")
        for file_path in failed_files:
            print(f"  • {os.path.basename(file_path)}")

def process_single_file(file_path):
    """
    Process a single file and create embeddings.
    
    Args:
        file_path (str): Path to the file to process
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔄 Processing: {os.path.basename(file_path)}")
    
    try:
        # Process file to extract text
        if process_file(file_path):
            # Create embeddings
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            text_file_path = f"Text_files/{base_filename}.txt"
            
            if os.path.exists(text_file_path):
                embeddings_path = Text_To_Embeddings.text_to_embeddings(text_file_path)
                print(f"🎉 Process completed successfully!")
                print(f"📁 Text file: {os.path.abspath(text_file_path)}")
                print(f"🔗 Embeddings: {os.path.abspath(embeddings_path)}")
                return True
            else:
                print(f"❌ Text file not created: {text_file_path}")
                return False
        else:
            print(f"❌ Failed to process file")
            return False
            
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Process specific file
        file_path = sys.argv[1]
        process_single_file(file_path)
    else:
        # Process all files in Documents directory
        process_all_documents()