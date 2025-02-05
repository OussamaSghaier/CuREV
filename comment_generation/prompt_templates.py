review_classification_system_prompt = """You are an expert in coding and code peer-reviewing."""

review_classification_template = """### Code review comment generation
Generate a review comment that you consider perfect for the given code changes.
A review comment should highlight the main issues, improvements, or suggestions for the code changes.
The generated review comment should be concise, relevant, clear, useful, and complete.

### Code changes:
{code_diff}
"""