import json

def match_provisions(client, exemptions: list[dict], reference_context: str = "") -> list[dict]:
    """AI Call 3: Match exemptions against Victorian FOI provisions"""
    
    if not exemptions:
        return []
    
    system_content = """Verify each exemption against the Victorian FOI reference documents provided. 

CRITICAL INSTRUCTIONS:
1. Use ONLY the FOI Guidelines Part IV (Victorian) for FOI exemptions
2. Use ONLY the TA Act for secrecy provisions (sections 91, 92, 93 - NOT s 355)
3. Cite exact sections from the Victorian FOI Act
4. Follow the guidelines' interpretation of each exemption

Add to each object:
- statutory_provision: exact law from Victorian FOI Act or TA Act
- legal_test: what must be proven according to the Victorian guidelines
- exemption_nature: mandatory or discretionary (per Victorian Act)"""
    
    if reference_context:
        system_content += f"\n\nREFERENCE DOCUMENTS:\n{reference_context[:4000]}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Verify these Victorian FOI exemptions:\n\n{json.dumps(exemptions, indent=2)}"}
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
        
        

