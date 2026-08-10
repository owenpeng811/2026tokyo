import re, json

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all time slot headings: ### **HH:MM ...**
sections = re.split(r'\n(?=### \*\*)', text)

transit_slots = []
all_slots = []

for sec in sections:
    if not sec.startswith('### **'):
        continue
    heading_match = re.match(r'### \*\*([^\*\n]+)\*\*', sec)
    if not heading_match:
        continue
    heading = heading_match.group(1)
    
    # Check if this heading is an activity/transit slot (has time or icon)
    # Extract links in the section
    links = re.findall(r'(?<!\!)\[\s*\*?\*?([^\*\]\n]+)\*?\*?\s*\]\((https?://[^\)]+)\)', sec)
    
    # First link that is a google maps link
    maps_links = [l for l in links if 'google.com/maps' in l[1] or 'maps.app.goo.gl' in l[1]]
    
    target_place = None
    target_match = re.search(r'目標地點：\[\s*\*?\*?([^\*\]\n]+)\*?\*?\s*\]\((https?://[^\)]+)\)', sec)
    if target_match:
        target_place = (target_match.group(1), target_match.group(2))
    elif maps_links:
        target_place = maps_links[0]
        
    all_slots.append({
        'heading': heading,
        'target_place': target_place,
        'all_maps_links_count': len(maps_links),
        'snippet': sec[:300].replace('\n', ' ')
    })

print(f"Total time slots found: {len(all_slots)}")
print("=" * 80)
for idx, s in enumerate(all_slots, 1):
    dest_str = f"[{s['target_place'][0]}] -> {s['target_place'][1][:45]}..." if s['target_place'] else "❌ 無導航連結"
    print(f"[{idx:02d}] {s['heading']}")
    print(f"     第一個目的地: {dest_str}")
