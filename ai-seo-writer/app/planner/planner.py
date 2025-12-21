import json
from app.ai.provider import BaseAIProvider

class ContentPlanner:
    def __init__(self, ai_provider: BaseAIProvider):
        self.ai = ai_provider

    def create_plan(self, keyword: str, research_data: dict) -> dict:
        snippets = "\n\n".join(research_data.get('snippets', []))
        
        prompt = f"""
        You are an SEO Content Strategist.
        Target Keyword: "{keyword}"
        
        Research Context from Top Search Results:
        {snippets}
        
        Task: Create a detailed content plan for an article targeting this keyword.
        Identify the user search intent and structure the article accordingly.
        
        Output MUST be valid JSON only in the following format:
        {{
            "main_topic": "Engaging H1 Title",
            "search_intent": "informational|transactional|commercial|navigational",
            "target_audience": "Target audience description",
            "outline": [
                {{"heading": "Section H2 Title", "subheadings": ["H3 Subpoint 1", "H3 Subpoint 2"], "notes": "What to cover here"}}
            ],
            "secondary_keywords": ["keyword1", "keyword2", "keyword3"]
        }}
        """
        
        response_text = self.ai.generate_content(prompt)
        
        # Robust JSON extraction
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON block found in AI response")
        except Exception as e:
            print(f"Error parsing plan JSON: {e}")
            print(f"Raw response: {response_text}")
            # Fallback plan structure
            return {
                "main_topic": f"Comprehensive Guide to {keyword}",
                "search_intent": "Informational",
                "outline": [
                    {"heading": "Introduction", "subheadings": [], "notes": "Introduce the topic"},
                    {"heading": "Main Concepts", "subheadings": [], "notes": "Explain core concepts"},
                    {"heading": "Conclusion", "subheadings": [], "notes": "Summarize"}
                ],
                "secondary_keywords": [keyword]
            }
