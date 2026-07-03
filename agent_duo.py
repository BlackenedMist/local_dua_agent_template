from crewai import Agent, Task, Crew, LLM

# 1. Define your local Ollama models
qwen_lead = LLM(
    model="ollama/qwen2.5-coder:7b",
    base_url="http://localhost:11434"
)

starcoder_dev = LLM(
    model="ollama/starcoder2:3b",
    base_url="http://localhost:11434"
)

# 2. Define the Tech Lead Agent (Qwen)
tech_lead = Agent(
    role='Senior Software Architect',
    goal='Break down user requests into perfect technical specifications and software architecture.',
    backstory='You are a strict, experienced architect. You design systems using Python, TypeScript, and Node.js best practices.',
    llm=qwen_lead,
    verbose=True
)

# 3. Define the Developer Agent (StarCoder)
developer = Agent(
    role='Software Engineer',
    goal='Write clean, bug-free production code based strictly on technical specifications.',
    backstory='You are an elite programmer. You take technical requirements and turn them into functional, well-commented code.',
    llm=starcoder_dev,
    verbose=True
)

# 4. Define the sequence of tasks
task_spec = Task(
    description='Design a robust Node.js backend route for user authentication using JWT.',
    expected_output='A markdown file detailing the endpoints, security requirements, and data structures.',
    agent=tech_lead
    output_file='src/auth_spec.md'  # <-- Saves the architecture plan here

)

task_code = Task(
    description='Take the architectural design provided by the Senior Software Architect and write the actual TypeScript implementation code.',
    expected_output='The complete, production-ready TypeScript code file.',
    agent=developer
    output_file='src/auth_spec.md'  # <-- Saves the architecture plan here

)

# 5. Form the Crew and run it
dev_team = Crew(
    agents=[tech_lead, developer],
    tasks=[task_spec, task_code],
    verbose=True
    output_file='src/auth_spec.md'  # <-- Saves the architecture plan here

)

result = dev_team.kickoff()
print("\n--- FINAL CODE OUTPUT ---")
print(result)
