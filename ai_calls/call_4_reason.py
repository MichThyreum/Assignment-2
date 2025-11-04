import json

def generate_reasoning(client, exemptions: list[dict], reference_context: str = "") -> list[dict]:
    """AI Call 4: Generate legal reasoning for each exemption"""
    
    if not exemptions:
        return []
    
    system_content = """Provide legal reasoning for each exemption.

Add to each object:
- reasoning: why this qualifies (2-3 sentences)
- recommendation: Exempt/Partially Exempt/Not Exempt"""
    
    if reference_context:
        system_content += f"\n\nReference FOI guidelines:\n{reference_context[:2000]}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Analyze:\n\n{json.dumps(exemptions, indent=2)}"}
        ],
        temperature=0.3
    )
    
    try:
        content = response.choices[0].message.content
        start = content.find('[')
        end = content.rfind(']') + 1
        if start >= 0 and end > 0:
            return json.loads(content[start:end])
        return exemptions
    except:
        return exemptions
        
        


