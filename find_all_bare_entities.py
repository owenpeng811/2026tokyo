import re

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Strip all markdown links first: [ ... ]( ... )
text_without_links = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', 'LINK_PLACEHOLDER', text)

# Find all remaining **Name (Japanese)**
matches = re.findall(r'\*\*([^\*\n]+?\([^\)\n]+[\u3040-\u30ff\u4e00-\u9fafA-Za-z0-9]+[^\)\n]*\))\*\*', text_without_links)

print("Found bare bold entities with Japanese names:")
for m in sorted(set(matches)):
    print(f" - **{m}**")
