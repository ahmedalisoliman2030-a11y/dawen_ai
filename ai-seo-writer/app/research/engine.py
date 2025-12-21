from duckduckgo_search import DDGS

class ResearchEngine:
    def __init__(self, max_results=5):
        self.max_results = max_results

    def search(self, query: str) -> dict:
        """
        Searches the web for the given query.
        Returns a dictionary with sources, snippets, and titles.
        """
        results = []
        try:
            with DDGS() as ddgs:
                # DDGS.text() returns an iterator or list depending on version, 
                # but iterating is safe.
                ddgs_gen = ddgs.text(query, max_results=self.max_results)
                if ddgs_gen:
                    for r in ddgs_gen:
                        results.append({
                            "title": r.get('title', ''),
                            "href": r.get('href', ''),
                            "body": r.get('body', '')
                        })
        except Exception as e:
            print(f"Error during web search: {e}")
            # Fail gracefully as per requirements
            pass

        return {
            "sources": [r['href'] for r in results],
            "snippets": [r['body'] for r in results],
            "titles": [r['title'] for r in results],
            "raw_results": results
        }
