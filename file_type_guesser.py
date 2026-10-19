from pathlib import Path

def guess_file_type(file_path):
    # Common file magic numbers (leading byte sequences)
    signatures = {
        b'\xFF\xD8\xFF': 'JPEG image',
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG image',
        b'GIF87a': 'GIF image',
        b'GIF89a': 'GIF image',
        b'%PDF': 'PDF file',
        b'PK\x03\x04': 'ZIParchive (may also be Word/Excel, etc.)',
        b'Rar!\x1a\x07': 'RAR archive',
        b'\x1f\x8b\x08': 'GZIP compressed file',
        b'\x7fELF': 'ELF executable (Linux等)',
        b'MZ': 'Windows executable (EXE / DLL)',
    }
    
    path = Path(file_path)
    if not path.is_file():
        return "The specified file does not exist."

    try:
        with open(path, 'rb') as f:
            # Read the first few bytes
            header = f.read(32)
            
        # Compare magic numbers
        for sig, file_type in signatures.items():
            if header.startswith(sig):
                return file_type
                
        # If it doesn't match any magic number, do a simple check for a text file
        # (considered text if there are very few extreme control characters in the binary)
        f.seek(0)
        sample = f.read(1024)
        if not b'\x00' in sample: # High probability of being a text file if it contains no null bytes
            return "Text file (guessed)"
            
        return "Unknown file format"
        
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    target_file = r'example_file'  # File path without extension
    print(f"ファイルの種類: {guess_file_type(target_file)}")