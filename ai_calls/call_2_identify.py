import json

def identify_exemptions(client, chunks: list[str], exemption_types: list[str]) -> list[dict]:
    """AI Call 2: Identify potential FOI exemptions in chunks"""
    
    exemption_focus = ", ".join(exemption_types)
    
    # Analyze all chunks
    all_text = "\n\n---CHUNK---\n\n".join(chunks)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""Find FOI exemptions. Focus on: {exemption_focus}
                
Return JSON array with objects containing:
- text: exact excerpt (50-200 chars)
- type: exemption type
- section: FOI section (e.g. "s 47F")
- confidence: High/Medium/Low"""
            },
            {
                "role": "user",
                "content": f"Document:\n\n{all_text[:8000]}"
            }
        ],
        temperature=0.2
    )
    
    try:
        content = response.choices[0].message.content
        # Extract JSON array
        start = content.find('[')
        end = content.rfind(']') + 1
        if start >= 0 and end > 0:
            return json.loads(content[start:end])
        return []
    except:
        return []

