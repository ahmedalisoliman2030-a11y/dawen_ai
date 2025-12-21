import os
import re
from datetime import datetime

class FileExporter:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def save_article(self, keyword: str, content: str, extension="md") -> str:
        slug = self._slugify(keyword)
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{slug}-{date_str}.{extension}"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return filepath

    def _slugify(self, text: str) -> str:
        """
        Creates a filename-safe slug from the keyword.
        Supports Arabic characters by allowing certain regex classes.
        """
        # Lowercase
        text = text.lower()
        # Replace spaces with hyphens
        text = re.sub(r'\s+', '-', text)
        # Remove special characters but keep arabic letters, english letters, numbers, and hyphens
        # This regex keeps word characters (\w) which includes unicode letters (Arabic), and hyphens.
        # We might want to be more strict if the OS has issues, but Windows usually handles unicode filenames fine.
        text = re.sub(r'[^\w\-]', '', text)
        # Remove repeated hyphens
        text = re.sub(r'-+', '-', text).strip('-')
        return text
