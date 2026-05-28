import os
import re
import datetime
import struct

# Paths
GALLERY_DIR = "assets/image/photography"
DATA_YML = "_data/gallery.yml"

def parse_exif(image_path):
    """
    Pure Python JPEG EXIF reader. Parses SOI and APP1 markers to read
    TIFF header & Exif sub-IFD directory tags.
    """
    try:
        with open(image_path, 'rb') as f:
            # Check JPEG Start Of Image marker
            data = f.read(2)
            if data != b'\xff\xd8':
                return None
            
            # Loop segments to find APP1 (EXIF)
            while True:
                marker_header = f.read(2)
                if len(marker_header) < 2:
                    break
                if marker_header[0] != 0xff:
                    break
                marker = marker_header[1]
                if marker == 0xd9: # EOI (End of Image)
                    break
                
                # Length of current segment
                len_bytes = f.read(2)
                if len(len_bytes) < 2:
                    break
                segment_len = struct.unpack('>H', len_bytes)[0]
                
                if marker == 0xe1: # APP1 (EXIF)
                    payload = f.read(segment_len - 2)
                    if payload.startswith(b'Exif\x00\x00'):
                        return parse_exif_payload(payload[6:])
                    break
                else:
                    # Skip other segments
                    f.seek(segment_len - 2, 1)
    except Exception as e:
        print(f"Error parsing EXIF for {os.path.basename(image_path)}: {e}")
    return None

def parse_exif_payload(tiff_data):
    """
    Parses the TIFF structure from the EXIF payload.
    """
    if tiff_data[:2] == b'II':
        byte_order = '<'
    elif tiff_data[:2] == b'MM':
        byte_order = '>'
    else:
        return None
    
    # Check Magic number
    magic = struct.unpack(byte_order + 'H', tiff_data[2:4])[0]
    if magic != 42:
        return None
    
    # Offset of first IFD
    ifd0_offset = struct.unpack(byte_order + 'I', tiff_data[4:8])[0]
    tags = {}
    
    def parse_ifd(offset):
        if offset >= len(tiff_data) or offset == 0:
            return 0
        try:
            num_entries = struct.unpack(byte_order + 'H', tiff_data[offset:offset+2])[0]
            entry_offset = offset + 2
            for _ in range(num_entries):
                if entry_offset + 12 > len(tiff_data):
                    break
                entry = tiff_data[entry_offset:entry_offset+12]
                tag, val_type, count, val_offset = struct.unpack(byte_order + 'HHII', entry)
                
                # Type sizes
                type_sizes = {1:1, 2:1, 3:2, 4:4, 5:8, 7:1, 9:4, 10:8}
                size = type_sizes.get(val_type, 1) * count
                
                if size <= 4:
                    raw_val = entry[8:8+size]
                else:
                    raw_val = tiff_data[val_offset:val_offset+size]
                
                val = None
                # Parse depending on type
                if val_type == 2: # ASCII
                    try:
                        val = raw_val.split(b'\x00')[0].decode('utf-8', errors='ignore').strip()
                    except Exception:
                        val = ""
                elif val_type in (3, 4): # SHORT, LONG
                    fmt = 'H' if val_type == 3 else 'I'
                    val_list = []
                    for i in range(count):
                        o = i * (2 if val_type == 3 else 4)
                        if o + (2 if val_type == 3 else 4) <= len(raw_val):
                            val_list.append(struct.unpack(byte_order + fmt, raw_val[o:o+(2 if val_type == 3 else 4)])[0])
                    val = val_list[0] if len(val_list) == 1 else val_list
                elif val_type in (5, 10): # RATIONAL, SRATIONAL
                    fmt = 'II' if val_type == 5 else 'ii'
                    val_list = []
                    for i in range(count):
                        o = i * 8
                        if o + 8 <= len(raw_val):
                            num, den = struct.unpack(byte_order + fmt, raw_val[o:o+8])
                            if den != 0:
                                val_list.append(num / den)
                            else:
                                val_list.append(0.0)
                    val = val_list[0] if len(val_list) == 1 else val_list
                
                tags[tag] = val
                entry_offset += 12
            
            if entry_offset + 4 <= len(tiff_data):
                return struct.unpack(byte_order + 'I', tiff_data[entry_offset:entry_offset+4])[0]
        except Exception as e:
            print(f"Error parsing IFD entries: {e}")
        return 0

    # Parse main IFD
    parse_ifd(ifd0_offset)
    
    # Parse EXIF sub-IFD (tag 0x8769)
    exif_offset = tags.get(0x8769)
    if exif_offset:
        parse_ifd(exif_offset)
        
    return tags

def load_gallery_yml(path):
    """
    Custom basic YAML loader to preserve manual edits in gallery.yml.
    """
    if not os.path.exists(path):
        return []
    entries = []
    current = None
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if stripped.startswith('- '):
                if current:
                    entries.append(current)
                current = {}
                parts = stripped[2:].split(':', 1)
            else:
                parts = stripped.split(':', 1)
            
            if len(parts) == 2 and current is not None:
                key = parts[0].strip()
                val = parts[1].strip()
                # strip surrounding quotes
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                current[key] = val
        if current:
            entries.append(current)
    return entries

def save_gallery_yml(path, entries):
    """
    Saves gallery data back to gallery.yml.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# _data/gallery.yml\n")
        f.write("# 本設定檔由 process_gallery.py 自動產生，可自由調整順序及新增備註。\n\n")
        for entry in entries:
            f.write(f"- image: \"{entry.get('image', '')}\"\n")
            f.write(f"  title: \"{entry.get('title', '')}\"\n")
            f.write(f"  date: \"{entry.get('date', '')}\"\n")
            f.write(f"  location: \"{entry.get('location', '')}\"\n")
            f.write(f"  metadata: \"{entry.get('metadata', '')}\"\n\n")

def process():
    print("=== 開始掃描攝影相片 ===")
    
    # Load current gallery.yml configuration to preserve manual edits
    existing_entries = load_gallery_yml(DATA_YML)
    existing_map = {e['image']: e for e in existing_entries if 'image' in e}
    
    new_entries = []
    
    # Check directory
    if not os.path.exists(GALLERY_DIR):
        os.makedirs(GALLERY_DIR)
        print(f"建立資料夾: {GALLERY_DIR}")
        print("請將您的攝影相片 (.jpg, .jpeg) 放入該資料夾後重新執行本腳本。")
        return

    # Scan files in assets/image/photography
    files = sorted(os.listdir(GALLERY_DIR))
    image_extensions = ('.jpg', '.jpeg')
    
    img_count = 0
    for filename in files:
        if not filename.lower().endswith(image_extensions):
            continue
        
        img_count += 1
        img_path = os.path.join(GALLERY_DIR, filename)
        web_path = f"/assets/image/photography/{filename}"
        
        # If the image was already configured, preserve existing custom fields
        existing = existing_map.get(web_path)
        
        title = ""
        date_str = ""
        location = ""
        metadata = ""
        
        if existing:
            title = existing.get('title', '')
            date_str = existing.get('date', '')
            location = existing.get('location', '')
            metadata = existing.get('metadata', '')
        
        # If any info is missing or new, parse EXIF
        tags = parse_exif(img_path)
        
        parsed_metadata_parts = []
        
        # 1. Camera model
        camera_model = ""
        if tags:
            make = tags.get(0x010f, "")
            model = tags.get(0x0110, "")
            if model:
                camera_model = model
                if make and make.lower() not in model.lower():
                    camera_model = f"{make} {model}"
            
            # Format and clean up camera name
            camera_model = re.sub(r'\s+', ' ', camera_model).strip()
            if camera_model:
                parsed_metadata_parts.append(camera_model)
                
            # 2. ISO
            iso = tags.get(0x8827)
            if iso:
                parsed_metadata_parts.append(f"ISO {iso}")
                
            # 3. Aperture (F-number)
            fnumber = tags.get(0x829d)
            if fnumber:
                if fnumber == int(fnumber):
                    parsed_metadata_parts.append(f"f/{int(fnumber)}")
                else:
                    parsed_metadata_parts.append(f"f/{fnumber:.1f}")
                    
            # 4. Shutter speed (Exposure time)
            exp_time = tags.get(0x829a)
            if exp_time:
                if exp_time < 1.0:
                    den = round(1.0 / exp_time)
                    parsed_metadata_parts.append(f"1/{den}s")
                else:
                    parsed_metadata_parts.append(f"{exp_time}s")
                    
            # 5. Focal length
            focal = tags.get(0x920a)
            if focal:
                parsed_metadata_parts.append(f"{int(focal)}mm")
        
        # Compute default values if not defined/existing
        if not title:
            # Use filename without extension as default title
            title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
            
        if not date_str:
            # Try to read date taken from EXIF
            exif_date = tags.get(0x9003) if tags else None
            if exif_date and len(exif_date) >= 7:
                # Format: YYYY-MM
                date_str = exif_date[:7].replace(':', '-')
            else:
                # Use current date as fallback
                date_str = datetime.datetime.now().strftime("%Y-%m")
                
        if not location:
            location = "攝影地點"
            
        if not metadata:
            if parsed_metadata_parts:
                metadata = ", ".join(parsed_metadata_parts)
            else:
                metadata = "無相片參數"
        elif parsed_metadata_parts and metadata == "無相片參數":
            # Update if metadata was previously unknown but tags are now read
            metadata = ", ".join(parsed_metadata_parts)

        new_entries.append({
            'image': web_path,
            'title': title,
            'date': date_str,
            'location': location,
            'metadata': metadata
        })
        print(f"已處理: {filename} -> 參數: {metadata}")
        
    if img_count == 0:
        print("未在資料夾內發現相片 (.jpg, .jpeg) 檔案。")
    else:
        # Save updated list
        save_gallery_yml(DATA_YML, new_entries)
        print(f"\n成功更新 {DATA_YML}! 共 {img_count} 張相片。")
    print("========================")

if __name__ == "__main__":
    process()
