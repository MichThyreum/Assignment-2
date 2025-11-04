import json

def match_provisions(client, exemptions: list[dict], reference_context: str = "") -> list[dict]:
    """AI Call 3: Match exemptions against FOI Act provisions"""
    
    if not exemptions:
        return []
    
    system_content = """Verify each exemption against FOI Act. 

Add to each object:
- statutory_provision: the exact law
- legal_test: what must be proven
- exemption_nature: mandatory or discretionary"""
    
    if reference_context:
        system_content += f"\n\nUse these reference documents:\n{reference_context[:2000]}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Verify these:\n\n{json.dumps(exemptions, indent=2)}"}
        ],
        temperature=0.2
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
        

