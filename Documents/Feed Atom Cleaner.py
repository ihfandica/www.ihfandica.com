import xml.etree.ElementTree as ET
import re

def clean_html(html_text):
    if not html_text:
        return ""
    clean = re.sub(r'<[^>]+>', '', html_text)
    clean = re.sub(r'&lt;[^&>]+&gt;', '', clean)
    lines = [line.strip() for line in clean.split('\n') if line.strip()]
    return '\n'.join(lines)

def extract_feed_data():
    try:
        tree = ET.parse('feed.atom')
        root = tree.getroot()
    except Exception as e:
        print(f"--> Error membaca file: {e}")
        return

    ns = 'http://www.w3.org/2005/Atom'
    
    with open('feed.txt', 'w', encoding='utf-8') as f:
        for entry in root.iterfind(f'{{{ns}}}entry'):
            title_node = entry.find(f'{{{ns}}}title')
            content_node = entry.find(f'{{{ns}}}content')
            published_node = entry.find(f'{{{ns}}}published')
            
            title = title_node.text.strip() if title_node is not None and title_node.text else "Tanpa Judul"
            content_raw = content_node.text if content_node is not None and content_node.text else ""
            published = published_node.text.strip() if published_node is not None and published_node.text else "Tanpa Tanggal"
            
            content = clean_html(content_raw)
            
            f.write(f"Judul Postingan: {title}\n")
            f.write(f"Tanggal Diposting: {published}\n")
            f.write("Postingan:\n")
            if content:
                f.write(f"{content}\n")
            f.write("-" * 50 + "\n\n")
            
    print("--> Ekstraksi selesai. Data disimpan di feed.txt")

if __name__ == "__main__":
    extract_feed_data()
