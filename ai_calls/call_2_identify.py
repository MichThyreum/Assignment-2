import json

def identify_exemptions(client, chunks: list[str], exemption_types: list[str], reference_context: str = "") -> list[dict]:
    """AI Call 2: Identify ALL potential Victorian FOI exemptions in chunks"""
    
    all_text = "\n\n---CHUNK---\n\n".join(chunks)
    
    system_content = """Identify ALL applicable Victorian FOI exemptions in this document.

CRITICAL INSTRUCTIONS:
1. Use ONLY the FOI Guidelines Part IV (Victorian) provided in the reference documents
2. Check for ALL Part IV exemptions (s 28 through s 38)
3. For secrecy provisions (s 38), check against TA Act sections 91, 92, and 93 (NOT s 355)
4. Cite the exact section numbers from the Victorian FOI Act
5. Use the guidelines to determine if exemptions apply

Return JSON array with objects containing:
- text: exact excerpt from document (50-200 chars)
- type: exemption name (e.g. "Personal Privacy", "Secrecy Provisions")
- section: exact Victorian FOI section (e.g. "s 33", "s 38")
- confidence: High/Medium/Low
- ta_act_section: if s 38, specify which TA Act section (s 91, 92, or 93)"""
    
    if reference_context:
        system_content += f"\n\nREFERENCE DOCUMENTS (USE ONLY THESE):\n{reference_context[:4000]}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Analyse this document and find ALL applicable Victorian FOI exemptions:\n\n{all_text[:8000]}"}
        ],
        temperature=0.2
    )
    
    try:
        content = response.choices[0].message.content
        start = content.find('[')
        end = content.rfind(']') + 1
        if start >= 0 and end > 0:
            return json.loads(content[start:end])
        return []
    except:
        return []
        
        
