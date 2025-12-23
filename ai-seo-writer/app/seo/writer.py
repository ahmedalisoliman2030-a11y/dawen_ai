from app.ai.provider import BaseAIProvider

class SEOWriter:
    def __init__(self, ai_provider: BaseAIProvider):
        self.ai = ai_provider

    def write_article(self, plan: dict, research_data: dict) -> str:
        snippets = "\n\n".join(research_data.get('snippets', []))
        # Convert plan to a readable string for the prompt
        plan_str = json_to_markdown_view(plan)
        
        prompt = f"""
        You are a Professional SEO Copywriter.
        
        # Content Plan
        {plan_str}
        
        # Research Context
        {snippets}
        
        # Assignment
        Write a high-quality, comprehensive article based strictly on the above plan.
        
        # Requirements
        1. **Format**: Use Markdown (H1, H2, H3, bullet points).
        2. **Length**: Aim for in-depth coverage (1000+ words).
        3. **Tone**: Professional, authoritative, yet accessible. 
        4. **SEO**: Naturally weave in the secondary keywords provided in the plan.
        5. **Structure**: Follow the outline provided.
        6. **Language**: The article MUST be written in **Arabic** (اللغة العربية). Do NOT write in English or any other language even if the keywords are in English.
        7. **Structure**: Use blockquotes (>) for tips or mental maps.
        
        Do not include any conversational filler before or after the article. Start directly with the H1 title.
        Ensure the output is 100% Arabic.
        """
        
        return self.ai.generate_content(prompt)

def json_to_markdown_view(data):
    """Helper to make JSON readable for the AI prompt"""
    import json
    return json.dumps(data, indent=2, ensure_ascii=False)
