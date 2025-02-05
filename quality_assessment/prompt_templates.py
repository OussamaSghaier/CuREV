llama_template = (
    "<|start_header_id|>system<|end_header_id|>\n\n"
    "{system_prompt}<|eot_id|>"
    "<|start_header_id|>user<|end_header_id|>\n\n"
    "{user_prompt}<|eot_id|>"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
    "Generated review comment: "
)

review_classification_system_prompt = """You are an expert in coding and code peer-reviewing."""

review_classification_template = """### Code review comment generation
Generate a review comment that you consider perfect for the code change without considering the given input comment.
A review comment should highlight the main issues, improvements, or suggestions for the code changes.
The generated review comment should be concise, relevant, clear, useful, and complete.

### Code review comment assessment
Then, evaluate and categorize only the given review comment, written by a reviewer, based on the below criteria.
You can use the generated review comment as a reference to evaluate the given review comment.
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

4. Conciseness: Assess how effectively the comment conveys its message using the fewest necessary words while remaining fully informative. 
A concise comment should be completely brief but informative, avoiding unnecessary details, repetition, or verbosity.  
Use a 1-to-10 rating scale.

5. Clarity: Evaluate how clear and specific the comment is.
A clear comment should be specific, straightforward, well-structured, and  easy to understand, providing precise and clear feedback or questions without any ambiguity or unnecessary details. 
Use a 1-to-10 rating scale.

6. Relevance: Assess the relevance of the review comment. 
A relevant comment provides a comprehensive, applicable, and useful feedback.
A review comment should be useful and complete, addressing all potential improvements and existing issues in the given code changes. 
Use a 1-to-10 rating scale.
---

### Example of output
- Generated review comment: [generated review comment]
- Given review comment evaluation:
    Type: [Refactoring, Bug fix]
    Nature: [Prescriptive, Clarification]
    Civility: Civil
    Conciseness: 8
    Clarity: 5
    Relevance: 1
    Rationale: [Explain the reasons for the evaluation scores]

---

### Given review comment:
{review_comment}

### Code changes:
{code_diffs}
"""