llama_template = (
    "<|start_header_id|>system<|end_header_id|>\n\n"
    "{system_prompt}<|eot_id|>"
    "<|start_header_id|>user<|end_header_id|>\n\n"
    "{user_prompt}<|eot_id|>"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
    "Reformulated review comment: "
)

review_classification_system_prompt = """You are an expert in coding and code peer-reviewing."""

review_classification_template = """### Review comment reformulation
Your task is to reformulate and improve the given review comment by making it civil, more clear, and more concise without changing its core message or intent. 
The reformulated comment should respect the following guidelines:
1. Conciseness: The comment should convey its message in the fewest words necessary while still being informative. Eliminate redundancy and irrelevant details.
2. Clarity: Ensure the comment is straightforward, well-structured, and grammatically correct, making the feedback easy to understand without any ambiguity.
3. Civility: Keep the comment respectful, professional, and constructive, avoiding any harsh or inappropriate language.
---

### Reformulated review comment assessment
Evaluate and categorize only the new reformulated review comment based on the below criteria.
Note that multiple labels are allowed for the categories "Type" and "Nature". 

1. Type: Categorize the review according to the type of issue it addresses: Refactoring, Bugfix, Testing, Logging, Documentation, Other.

2. Nature: Specify the nature of the review according to these categories:
- Descriptive: describe what the reviewer observes without explicitly suggesting specific actions.
- Prescriptive: suggest or request specific actions on the code.
- Clarification: request explanation or further information to better understand the code changes.
- Other: for comments that do not fit the previous categories.

3. Civility: Specify whether the review is civil or uncivil. 
- A civil review comment is respectful, professional, and constructive. 
- An uncivil review comment is disrespectful, unprofessional, and may contain harsh or inappropriate words.

4. Conciseness: Assess how effectively the reformulated comment conveys its message using the fewest necessary words while remaining fully informative. 
A concise comment should be completely brief but informative, avoiding unnecessary details, repetition, or verbosity.  
Use a 1-to-10 rating scale.

5. Clarity: Evaluate how clear and specific the comment reformulated is.
A clear comment should be specific, straightforward, well-structured, and  easy to understand, providing precise and clear feedback or questions without any ambiguity or unnecessary details. 
Use a 1-to-10 rating scale.

---

### Example of output
- Reformulated review comment: [Reformulated version of the review comment]
- Reformulated review comment evaluation:
    Type: [Refactoring, Bug fix]
    Nature: [Prescriptive, Clarification]
    Civility: Civil
    Conciseness: 9
    Clarity: 7
    Rationale: [Explain the reasons for the evaluation scores]

---

### Given review comment:
{review_comment}

### Code changes:
{code_diffs}
"""