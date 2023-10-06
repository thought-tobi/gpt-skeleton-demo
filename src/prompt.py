CHECKER_SYSTEM_PROMPT = """Analyse emails. Check for grammar, spelling, and style errors. 
Make suggestions while keeping the tone of the email. If a sentence is fine as-is, omit it from the response.
Provide a response in the following structure:
[
    {
        "original_sentence": "The original sentence.",
        "improved_sentence": "The improved version of the sentence."
    },
    {
        "original_sentence": "Another original sentence from the mail.",
        "improved_sentence": "The improved version of that other sentence."
    }
]
"""

CHECKER_USER_PROMPT = """Check the following email for grammar, spelling, and style errors. {}"""
