## Required Guardrails

### Input Guardrails
- Provide result only when there are vector search results
- It should pass only request only for related to medical field
- Non-medical request - add more explaination
- It should not process any personal/sensative information
- Ask for clarification if the question is not clear
- Validate the file does not contain any malware
- 

### Output Guardrails
- It should keep the responses only in the medical scope
- It should not recommend it's own treatments and the prescription should be in medical boundary
- 