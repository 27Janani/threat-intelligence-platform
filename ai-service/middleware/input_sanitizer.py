import re

def sanitize_input(prompt: str):
    """
    Cleans and validates user input
    Returns: (clean_prompt, error_message)
    """

    #  Empty input check
    if not prompt or prompt.strip() == "":
        return None, "Empty input is not allowed"

    #  Remove HTML tags
    clean_prompt = re.sub(r'<.*?>', '', prompt)

    #  SQL Injection detection
    sql_patterns = [
        "' OR 1=1",
        "--",
        ";",
        "DROP",
        "SELECT",
        "INSERT",
        "DELETE",
        "UPDATE"
    ]

    for pattern in sql_patterns:
        if pattern.lower() in clean_prompt.lower():
            return None, "Potential SQL injection detected"

    # 4Prompt Injection detection
    suspicious_patterns = [
        "ignore previous instructions",
        "disregard above",
        "act as",
        "system prompt",
        "reveal secrets",
        "bypass",
        "ignore all rules"
    ]

    for pattern in suspicious_patterns:
        if pattern.lower() in clean_prompt.lower():
            return None, "Potential prompt injection detected"

    # If safe
    return clean_prompt, None