import re
from config.settings import Config

class InputHandler:
    @staticmethod
    def cleanup_keyword(keyword: str) -> str:
        """
        Cleans and normalizes the keyword string.
        Removes extra whitespace and newlines.
        """
        if not keyword:
            return ""
        return " ".join(keyword.strip().split())

    @staticmethod
    def validate_keyword(keyword: str) -> bool:
        """
        Validates the keyword based on rules:
        - Not empty
        - Max 6 words
        """
        cleaned = InputHandler.cleanup_keyword(keyword)
        
        if not cleaned:
            raise ValueError("Keyword cannot be empty.")
            
        word_count = len(cleaned.split())
        if word_count > Config.MAX_KEYWORD_WORDS:
            raise ValueError(f"Keyword is too long ({word_count} words). Max allowed is {Config.MAX_KEYWORD_WORDS}.")
            
        return True

    @staticmethod
    def process(keyword: str) -> str:
        """
        Main entry point to clean and validate a keyword.
        Returns the cleaned keyword or raises ValueError.
        """
        cleaned = InputHandler.cleanup_keyword(keyword)
        InputHandler.validate_keyword(cleaned)
        return cleaned
