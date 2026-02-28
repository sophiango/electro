import numpy as np
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def hybrid_score(cosine_score, feeder):
    growth_score = (feeder.queued_dg or 0) - (feeder.existing_dg or 0)
    return 0.7 * cosine_score + 0.3 * growth_score

def summarize_results(query, feeders):
    formatted = "\n".join([
        f"{f.substation_name}, voltage: {f.voltage_kv}, existing DG: {f.existing_dg}, queued DG: {f.queued_dg}"
        for f in feeders
    ])

    prompt = f"""
    User query: 
    {query}
    Relevant grid data:
    {formatted}
    Provide a concise analytical recommendation
    """
    system_prompt = "You are a PGE electric expert and you have experience planning grid location"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content