# llmMutation

Repository work in progress

## Objective
- Usage of llm in mutation testing

## Steps
- Install mutmut <TBD steps>
- Install google gemini via pip3 : pip3 install google-generativeai
- Export google key as env variable via : export GOOGLE_API_KEY=<YOUR_KEY>
- Run mutmut in the repository first : mutmut run
- Store a copy of /mutants/example.py.meta file
- Notice the presence of 0 in one of the exit codes
- Once the mutants folder is generated run the generate_tests.py : python3 generate_tests.py
- Additional tests will be stored under the tests folder
- (Currently it requires us to manually remove 2 extra lines of code)
- Delete the mutants folder and generate it again via : mutmut run
- Verify that all exit codes in newly generated /mutants/example.py.meta file are 1
