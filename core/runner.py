##runner.py
import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_prompt(prompt: str, retries: int = 3, delay: int = 1):
    """
    Run LLM prompt with retry + latency tracking
    """

    for attempt in range(retries):
        try:
            start_time = time.time()

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            end_time = time.time()
            latency = round(end_time - start_time, 3)

            output = response.choices[0].message.content.strip()

            return {
                "output": output,
                "latency": latency,
                "error": None
            }

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return {
                    "output": "",
                    "latency": None,
                    "error": str(e)
                }