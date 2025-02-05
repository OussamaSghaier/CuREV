review_classification_system_prompt = """You are an expert in coding and code peer-reviewing."""

review_classification_template = """### Instruction
Given the following initial code changes and a review comment, generate new code changes based on the review comment.
The old code file is provided for context.
You don't need to output the entire code file, just the code difference that implements the review comment.

### Initial code changes:
{code_diff}

### Review comment:
{review_comment}


### Old code file:
{old_file}

"""
