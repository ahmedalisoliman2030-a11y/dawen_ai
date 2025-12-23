import os
import re
from datetime import datetime
import markdown

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

    def save_article_html(self, keyword: str, content: str) -> str:
        """
        Converts Markdown to HTML and saves it with a nice blog template.
        """
        html_content = markdown.markdown(content, extensions=['fenced_code', 'tables', 'nl2br'])
        
        template = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{keyword}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        article {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        h1, h2, h3 {{ color: #2c3e50; margin-top: 1.5em; }}
        h1 {{ border-bottom: 2px solid #3498db; padding-bottom: 10px; font-size: 2.5em; }}
        h2 {{ border-right: 5px solid #3498db; padding-right: 15px; font-size: 1.8em; }}
        blockquote {{
            background: #eef7fa;
            border-right: 5px solid #3498db;
            margin: 20px 0;
            padding: 15px 20px;
            font-style: italic;
            color: #555;
        }}
        pre {{
            background: #2d3436;
            color: #f1f2f6;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-right: 5px solid #e17055;
        }}
        code {{ font-family: 'Consolas', monospace; }}
        ul, ol {{ padding-right: 40px; }}
        li {{ margin-bottom: 10px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <article>
        {html_content}
    </article>
</body>
</html>"""
        
        return self.save_article(keyword, template, "html")

    def _slugify(self, text: str) -> str:
        """
        Creates a filename-safe slug from the keyword.
        Supports Arabic characters by allowing certain regex classes.
        """
        # Lowercase
        text = text.lower()
        # Replace spaces with hyphens
        text = re.sub(r'\s+', '-', text)
        # Keep word chars (including arabic), numbers, hyphens
        text = re.sub(r'[^\w\-]', '', text)
        # Remove repeated hyphens
        text = re.sub(r'-+', '-', text).strip('-')
        return text
