import re
from collections.abc import Callable
from pathlib import Path

from pydantic import BaseModel, Field


# Defining core functions
def cleaner(text : str) -> str:
    
    cleaned_punctuations = re.sub(r"[^\w\s]", "",text)
    cleaned = " ".join(cleaned_punctuations.lower().split())
    return cleaned


def tokenizer(text: str) -> str:
    cleaned = cleaner(text)
    return cleaned.split()

def counter(text: str) -> str:
    tokens = tokenizer(text)
    return {word: tokens.count(word) for word in set(tokens)}


# Pydantic model to validate our analyzer

class AnalysisReport(BaseModel):
    total_tokens: int = Field(..., description="Total token count")
    unique_words : int = Field(..., description="Total unique words")
    cleaned_text : str = Field(..., description="Snippet of processed text")
    
    def format_report(self) -> str:
        report = [
            "=== Text Analysis Report ===",
            f"Total Tokens: {self.total_tokens}",
            f"Unique Words: {self.unique_words}",
            f"\nCleaned Text: {self.cleaned_text[:25]}"
        ]
        return "\n".join(report)


def analyzer(text: str) -> AnalysisReport:
    clean_text = cleaner(text)
    tokenized_text = tokenizer(text)
    counted_text = counter(text)
    
    return AnalysisReport (
        total_tokens = len(tokenized_text),
        unique_words = len(counted_text),
        cleaned_text = clean_text
    )
    
    


#Defining I/O function

def process_file(input_path: Path, output_path: Path, processor_func: Callable[[str], any]) -> Path:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    raw_text = input_path.read_text(encoding="utf-8")
    
    result = processor_func(raw_text)
    
    if not isinstance(result, str):
        result = str(result)
        
    output_path.write_text(result, encoding="utf-8")
    
    return output_path