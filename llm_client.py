import os
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from prompts import DDR_SYSTEM_PROMPT

load_dotenv()

class DDRGenerator:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            print("WARNING: GROQ_API_KEY not found in environment. Please set it.")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"

    def _call_llm_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Call Groq API with retry logic and exponential backoff."""
        delay = 2  # initial delay in seconds
        
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1, # Using low temperature for consistent reporting
                    max_completion_tokens=4096, # High max tokens as DDR report might be long
                    top_p=1,
                    stream=False, # We don't really stream to text file
                    stop=None
                )
                
                return completion.choices[0].message.content
                
            except Exception as e:
                # Groq exceptions can be rate limits (429) or internal errors
                status_code = getattr(e, 'status_code', None)
                if status_code in (429, 500, 503) and attempt < max_retries - 1:
                    print(f"API Error {status_code} encountered. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # exponential backoff
                elif attempt < max_retries - 1:
                    print(f"Unexpected error encountered: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2
                else:
                    print(f"Failed after {attempt + 1} attempts. Error: {e}")
                    raise e
                    
        return "Failed to generate report due to persistent errors."

    def generate_report(self, inspection_text: str, thermal_text: str) -> str:
        """
        Takes the raw text from the site inspection and thermal imaging reports
        and uses the LLM to generate the DDR.
        """
        # Format the prompt
        report_date = datetime.now().strftime("%Y-%m-%d")
        
        formatted_prompt = DDR_SYSTEM_PROMPT.format(
            INSPECTION_REPORT_TEXT=inspection_text,
            THERMAL_REPORT_TEXT=thermal_text,
            REPORT_DATE=report_date
        )
        
        print("Sending request to Groq API. This may take a few seconds...")
        
        result = self._call_llm_with_retry(formatted_prompt)
        return result
