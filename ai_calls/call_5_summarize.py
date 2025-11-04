def create_summary(client, exemptions: list[dict], reference_context: str = "") -> str:
    """AI Call 5: Create executive summary"""
    
    system_content = """Create executive summary with:
1. Total exemptions found
2. Breakdown by type
3. Key recommendations
4. Risk areas

Write clearly for decision-makers."""
    
    if reference_context:
        system_content += f"\n\nReference context:\n{reference_context[:1500]}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Exemptions:\n\n{exemptions}"}
        ],
        temperature=0.4
    )
    
    return response.choices[0].message.content
    
    