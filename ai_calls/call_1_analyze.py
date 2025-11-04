import json

def analyze_chunks(client, chunks: list[str], reference_context: str = "") -> dict:
    """AI Call 1: Analyze document chunks to understand content"""
    
    # Combine first few chunks for overview
    sample_text = "\n\n".join(chunks[:3])
    
    system_content = "Analyze this document. Return JSON with: document_type, key_topics, sensitive_areas"
    if reference_context:
        system_content += f"\n\nReference documents:\n{reference_context[:1500]}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Analyze:\n\n{sample_text[:3000]}"}
        ],
        temperature=0.3
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {"summary": response.choices[0].message.content}
        
        