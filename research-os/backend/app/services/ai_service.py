import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("HACKCLUB_API_KEY"),
    base_url="https://ai.hackclub.com/proxy/v1",
)

def create_research_card(text: str):
    prompt=f"""
You are an expert research analyst.
Read this research paper and return only valid JSON. (Don't  wrap JSON in markdown, dont include explanations, dont include ```json, return null if unknown field)

Fields:
- title
- summary
- objective
- doi
- hypothesis
- methods
- dataset
- public_datadet
- key_findings
- conclusion
- limitations
- future_work
- research_gap
- keywords

Paper:

{text[:12000]}
"""
    response=client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    content = response.choices[0].message.content
    print("\n===== AI RAW RESPONSE =====\n")
    print(content)
    print("\n===========================\n")
    return json.loads(response.choices[0].message.content)