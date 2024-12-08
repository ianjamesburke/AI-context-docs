# CrewAI Coding examples for syntax reference


# Human in the loop intigration

```python

from humanlayer import HumanLayer
from crewai import Agent, Task, Crew
hl = HumanLayer()
human_chat = hl.human_as_tool()

customer_service_agent = Agent(
    role="Customer Service Rep",
    goal="Provide excellent customer support",
    backstory="You are a helpful customer service agent who adapts based on user. 
   responses",
    tools=[human_chat],  # This allows the agent to interact with humans
)

task = Task(
    description="""
    Engage in a conversation with the user. Adapt your responses and questions
    based on their previous answers. Continue the conversation until the user
    indicates they're done.
    """,
    agent=customer_service_agent
)

crew = Crew(
    agents=[customer_service_agent],
    tasks=[task]
)

# Start the conversation
crew.kickoff()
```


# Basic Agent
