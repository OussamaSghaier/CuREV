import json

results_path = "../data/reform_results/reform_results_postprocessed.jsonl"

with open(results_path, 'r') as jsonl_file:
    results = [json.loads(line) for line in jsonl_file]

results = [result['judgments'] for result in results]

# compute avg_conciseness
avg_conciseness = sum([result['Conciseness'] for result in results]) / len(results)
print(f"> Average conciseness: {avg_conciseness}")
print("---------------------------------------------")

# compute avg_clarity
avg_clarity = sum([result['Clarity'] for result in results]) / len(results)
print(f"> Average clarity: {avg_clarity}")
print("---------------------------------------------")

# compute % civil and uncivil
civil = sum([1 if result['Civility']=="Civil" else 0 for result in results])
uncivil = sum([1 if result['Civility']=="Uncivil" else 0 for result in results])
print(f"> % Civil: {civil/len(results)} [{civil}]")
print(f"> % Uncivil: {uncivil/len(results)} [{uncivil}]")
print("---------------------------------------------")

# compute % nature
prescriptive = sum([1 if "Prescriptive" in result['Nature'] else 0 for result in results])
descriptive = sum([1 if "Descriptive" in result['Nature'] else 0 for result in results])
clarification = sum([1 if "Clarification" in result['Nature'] else 0 for result in results])
other = sum([1 if "Other" in result['Nature'] else 0 for result in results])

print(f"> % Prescriptive: {prescriptive/len(results)} [{prescriptive}]")
print(f"> % Descriptive: {descriptive/len(results)} [{descriptive}]")
print(f"> % Clarification: {clarification/len(results)} [{clarification}]")
print(f"> % Other: {other/len(results)} [{other}]")
print("---------------------------------------------")

# compute % type, types = ["Refactoring", "Bugfix", "Testing", "Logging", "Documentation", "Other"]
refactoring = sum([1 if "Refactoring" in result['Type'] else 0 for result in results])
bugfix = sum([1 if "Bugfix" in result['Type'] else 0 for result in results])
testing = sum([1 if "Testing" in result['Type'] else 0 for result in results])
logging = sum([1 if "Logging" in result['Type'] else 0 for result in results])
documentation = sum([1 if "Documentation" in result['Type'] else 0 for result in results])
other2 = sum([1 if "Other" in result['Type'] else 0 for result in results])

print(f"> % Refactoring: {refactoring/len(results)} [{refactoring}]")
print(f"> % Bugfix: {bugfix/len(results)} [{bugfix}]")
print(f"> % Testing: {testing/len(results)} [{testing}]")
print(f"> % Logging: {logging/len(results)} [{logging}]")
print(f"> % Documentation: {documentation/len(results)} [{documentation}]")
print(f"> % Other: {other2/len(results)} [{other2}]")
print("---------------------------------------------")


print("-------------------- Nature stats-------------------------")

# compute avg_conciseness for each nature
prescriptive_conciseness = sum([result['Conciseness'] for result in results if "Prescriptive" in result['Nature']]) / prescriptive
descriptive_conciseness = sum([result['Conciseness'] for result in results if "Descriptive" in result['Nature']]) / descriptive
clarification_conciseness = sum([result['Conciseness'] for result in results if "Clarification" in result['Nature']]) / clarification
other_conciseness = sum([result['Conciseness'] for result in results if "Other" in result['Nature']]) / other

print(f"> Average conciseness for Prescriptive: {prescriptive_conciseness}")
print(f"> Average conciseness for Descriptive: {descriptive_conciseness}")
print(f"> Average conciseness for Clarification: {clarification_conciseness}")
print(f"> Average conciseness for Other: {other_conciseness}")

# compute avg_clarity for each nature
prescriptive_clarity = sum([result['Clarity'] for result in results if "Prescriptive" in result['Nature']]) / prescriptive
descriptive_clarity = sum([result['Clarity'] for result in results if "Descriptive" in result['Nature']]) / descriptive
clarification_clarity = sum([result['Clarity'] for result in results if "Clarification" in result['Nature']]) / clarification
other_clarity = sum([result['Clarity'] for result in results if "Other" in result['Nature']]) / other

print(f"> Average clarity for Prescriptive: {prescriptive_clarity}")
print(f"> Average clarity for Descriptive: {descriptive_clarity}")
print(f"> Average clarity for Clarification: {clarification_clarity}")
print(f"> Average clarity for Other: {other_clarity}")

print("-------------------- Type stats-------------------------")

# compute avg_conciseness for each type
refactoring_conciseness = sum([result['Conciseness'] for result in results if "Refactoring" in result['Type']]) / refactoring
bugfix_conciseness = sum([result['Conciseness'] for result in results if "Bugfix" in result['Type']]) / bugfix
testing_conciseness = sum([result['Conciseness'] for result in results if "Testing" in result['Type']]) / testing
logging_conciseness = sum([result['Conciseness'] for result in results if "Logging" in result['Type']]) / logging
documentation_conciseness = sum([result['Conciseness'] for result in results if "Documentation" in result['Type']]) / documentation
other2_conciseness = sum([result['Conciseness'] for result in results if "Other" in result['Type']]) / other2

print(f"> Average conciseness for Refactoring: {refactoring_conciseness}")
print(f"> Average conciseness for Bugfix: {bugfix_conciseness}")
print(f"> Average conciseness for Testing: {testing_conciseness}")
print(f"> Average conciseness for Logging: {logging_conciseness}")
print(f"> Average conciseness for Documentation: {documentation_conciseness}")
print(f"> Average conciseness for Other: {other2_conciseness}")

# compute avg_clarity for each type
refactoring_clarity = sum([result['Clarity'] for result in results if "Refactoring" in result['Type']]) / refactoring
bugfix_clarity = sum([result['Clarity'] for result in results if "Bugfix" in result['Type']]) / bugfix
testing_clarity = sum([result['Clarity'] for result in results if "Testing" in result['Type']]) / testing
logging_clarity = sum([result['Clarity'] for result in results if "Logging" in result['Type']]) / logging
documentation_clarity = sum([result['Clarity'] for result in results if "Documentation" in result['Type']]) / documentation
other2_clarity = sum([result['Clarity'] for result in results if "Other" in result['Type']]) / other2

print(f"> Average clarity for Refactoring: {refactoring_clarity}")
print(f"> Average clarity for Bugfix: {bugfix_clarity}")
print(f"> Average clarity for Testing: {testing_clarity}")
print(f"> Average clarity for Logging: {logging_clarity}")
print(f"> Average clarity for Documentation: {documentation_clarity}")
print(f"> Average clarity for Other: {other2_clarity}")

print("-------------------- Civility stats-------------------------")

# compute avg_conciseness for each civility
civil_conciseness = sum([result['Conciseness'] for result in results if "Civil" in result['Civility']]) / civil

print(f"> Average conciseness for Civil: {civil_conciseness}")

# compute avg_clarity for each civility
civil_clarity = sum([result['Clarity'] for result in results if "Civil" in result['Civility']]) / civil

print(f"> Average clarity for Civil: {civil_clarity}")




# Compute the distribution of the conciseness scores
print("-------------------- Conciseness distribution-------------------------")
conciseness_scores = [result['Conciseness'] for result in results]
conciseness_distribution = {i: conciseness_scores.count(i) for i in range(1, 11)}

print(conciseness_distribution)

print("-------------------- Conciseness Cumulative distribution-------------------------")

# Compute cumulative distribution of conciseness scores
cumulative_distribution = {i: sum([conciseness_distribution[j] for j in range(1, i+1)]) for i in range(1, 11)}

print(cumulative_distribution)

# Compute the distribution of the clarity scores
print("-------------------- Clarity distribution-------------------------")
clarity_scores = [result['Clarity'] for result in results]
clarity_distribution = {i: clarity_scores.count(i) for i in range(1, 11)}

print(clarity_distribution)

print("-------------------- Clarity Cumulative distribution-------------------------")

# Compute cumulative distribution of clarity scores
cumulative_distribution = {i: sum([clarity_distribution[j] for j in range(1, i+1)]) for i in range(1, 11)}

print(cumulative_distribution)













