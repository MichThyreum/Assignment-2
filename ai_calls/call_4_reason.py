import json

def generate_reasoning(client, exemptions: list[dict]) -> list[dict]:
    """AI Call 4: Generate legal reasoning for each exemption"""
    
    if not exemptions:
        return []
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Provide legal reasoning for each exemption.

For each exemption object in the array, add these fields:
- reasoning: why this qualifies (2-3 sentences)
- recommendation: Exempt/Partially Exempt/Not Exempt

Return the complete JSON array with all original fields plus the new ones."""
            },
            {
                "role": "user",
                "content": f"Add reasoning to these exemptions:\n\n{json.dumps(exemptions, indent=2)}"
            }
        ],
        temperature=0.3
    )
    
    try:
        content = response.choices[0].message.content
        start = content.find('[')
        end = content.rfind(']') + 1
        if start >= 0 and end > 0:
            result = json.loads(content[start:end])
            # Ensure each exemption has the required fields
            for ex in result:
                if 'reasoning' not in ex:
                    ex['reasoning'] = 'Reasoning not provided by AI'
                if 'recommendation' not in ex:
                    ex['recommendation'] = 'Not determined'
            return result
        return exemptions
    except Exception as e:
        # If parsing fails, add default values to original exemptions
        for ex in exemptions:
            if 'reasoning' not in ex:
                ex['reasoning'] = 'Error generating reasoning'
            if 'recommendation' not in ex:
                ex['recommendation'] = 'Error'
        return exemptions
        


