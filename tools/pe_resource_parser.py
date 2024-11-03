#!/usr/bin/env python3
import pefile
import sys

def print_resource_info(dll_path):
    print("\nResource Information:")
    print("=" * 50)
    
    try:
        pe = pefile.PE(dll_path)
        
        # Get the .rsrc section
        rsrc_section = None
        for section in pe.sections:
            if section.Name.decode().strip('\x00') == '.rsrc':
                rsrc_section = section
                break
                
        if not rsrc_section:
            print("No .rsrc section found")
            return
            
        print(f"Resource section size: {rsrc_section.SizeOfRawData} bytes")
        
        # Try to find VS_VERSION_INFO
        for entry in pe.FileInfo:
            for st in entry:
                if hasattr(st, 'StringTable'):
                    for string_table in st.StringTable:
                        for key, value in string_table.entries.items():
                            print(f"{key.decode('utf-8'):<20}: {value.decode('utf-8')}")

    except Exception as e:
        print(f"Error processing DLL: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./parse_version.py <path_to_dll>")
        sys.exit(1)
    
    print_resource_info(sys.argv[1])
