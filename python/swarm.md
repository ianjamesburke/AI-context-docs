# EXAMPLE CODE FOR OpenAI Swarm
### AI Agent framework for Python


from swarm import Swarm, Agent

client = Swarm()

def transfer_to_agent_b():
    return agent_b


agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    instructions="Only speak in Haikus.",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B."}],
)

print(response.messages[-1]["content"])

from swarm import Swarm

client = Swarm()
client.run()
Swarm's run() function is analogous to the chat.completions.create() function in the Chat Completions API – it takes messages and returns messages and saves no state between calls. Importantly, however, it also handles Agent function execution, hand-offs, context variable references, and can take multiple turns before returning to the user.

At its core, Swarm's client.run() implements the following loop:

Get a completion from the current Agent
Execute tool calls and append results
Switch Agent if necessary
Update context variables, if necessary
If no new function calls, return
Arguments
Argument	Type	Description	Default
agent	Agent	The (initial) agent to be called.	(required)
messages	List	A list of message objects, identical to Chat Completions messages	(required)
context_variables	dict	A dictionary of additional context variables, available to functions and Agent instructions	{}
max_turns	int	The maximum number of conversational turns allowed	float("inf")
model_override	str	An optional string to override the model being used by an Agent	None
execute_tools	bool	If False, interrupt execution and immediately returns tool_calls message when an Agent tries to call a function	True
stream	bool	If True, enables streaming responses	False
debug	bool	If True, enables debug logging	False
Once client.run() is finished (after potentially multiple calls to agents and tools) it will return a Response containing all the relevant updated state. Specifically, the new messages, the last Agent to be called, and the most up-to-date context_variables. You can pass these values (plus new user messages) in to your next execution of client.run() to continue the interaction where it left off – much like chat.completions.create(). (The run_demo_loop function implements an example of a full execution loop in /swarm/repl/repl.py.)

Response Fields
Field	Type	Description
messages	List	A list of message objects generated during the conversation. Very similar to Chat Completions messages, but with a sender field indicating which Agent the message originated from.
agent	Agent	The last agent to handle a message.
context_variables	dict	The same as the input variables, plus any changes.
Agents
An Agent simply encapsulates a set of instructions with a set of functions (plus some additional settings below), and has the capability to hand off execution to another Agent.

While it's tempting to personify an Agent as "someone who does X", it can also be used to represent a very specific workflow or step defined by a set of instructions and functions (e.g. a set of steps, a complex retrieval, single step of data transformation, etc). This allows Agents to be composed into a network of "agents", "workflows", and "tasks", all represented by the same primitive.

Agent Fields
Field	Type	Description	Default
name	str	The name of the agent.	"Agent"
model	str	The model to be used by the agent.	"gpt-4o"
instructions	str or func() -> str	Instructions for the agent, can be a string or a callable returning a string.	"You are a helpful agent."
functions	List	A list of functions that the agent can call.	[]
tool_choice	str	The tool choice for the agent, if any.	None
Instructions
Agent instructions are directly converted into the system prompt of a conversation (as the first message). Only the instructions of the active Agent will be present at any given time (e.g. if there is an Agent handoff, the system prompt will change, but the chat history will not.)

agent = Agent(
   instructions="You are a helpful agent."
)
The instructions can either be a regular str, or a function that returns a str. The function can optionally receive a context_variables parameter, which will be populated by the context_variables passed into client.run().

def instructions(context_variables):
   user_name = context_variables["user_name"]
   return f"Help the user, {user_name}, do whatever they want."

agent = Agent(
   instructions=instructions
)
response = client.run(
   agent=agent,
   messages=[{"role":"user", "content": "Hi!"}],
   context_variables={"user_name":"John"}
)
print(response.messages[-1]["content"])
Hi John, how can I assist you today?
Functions
Swarm Agents can call python functions directly.
Function should usually return a str (values will be attempted to be cast as a str).
If a function returns an Agent, execution will be transferred to that Agent.
If a function defines a context_variables parameter, it will be populated by the context_variables passed into client.run().
def greet(context_variables, language):
   user_name = context_variables["user_name"]
   greeting = "Hola" if language.lower() == "spanish" else "Hello"
   print(f"{greeting}, {user_name}!")
   return "Done"

agent = Agent(
   functions=[greet]
)

client.run(
   agent=agent,
   messages=[{"role": "user", "content": "Usa greet() por favor."}],
   context_variables={"user_name": "John"}
)
Hola, John!
If an Agent function call has an error (missing function, wrong argument, error) an error response will be appended to the chat so the Agent can recover gracefully.
If multiple functions are called by the Agent, they will be executed in that order.
Handoffs and Updating Context Variables
An Agent can hand off to another Agent by returning it in a function.

sales_agent = Agent(name="Sales Agent")

def transfer_to_sales():
   return sales_agent

agent = Agent(functions=[transfer_to_sales])

response = client.run(agent, [{"role":"user", "content":"Transfer me to sales."}])
print(response.agent.name)
Sales Agent
It can also update the context_variables by returning a more complete Result object. This can also contain a value and an agent, in case you want a single function to return a value, update the agent, and update the context variables (or any subset of the three).

sales_agent = Agent(name="Sales Agent")

def talk_to_sales():
   print("Hello, World!")
   return Result(
       value="Done",
       agent=sales_agent,
       context_variables={"department": "sales"}
   )

agent = Agent(functions=[talk_to_sales])

response = client.run(
   agent=agent,
   messages=[{"role": "user", "content": "Transfer me to sales"}],
   context_variables={"user_name": "John"}
)
print(response.agent.name)
print(response.context_variables)
Sales Agent
{'department': 'sales', 'user_name': 'John'}

# examples

from swarm import Swarm, Agent

client = Swarm()

english_agent = Agent(
    name="English Agent",
    instructions="You only speak English.",
)

spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish.",
)


def transfer_to_spanish_agent():
    """Transfer spanish speaking users immediately."""
    return spanish_agent


english_agent.functions.append(transfer_to_spanish_agent)

messages = [{"role": "user", "content": "Hola. ¿Como estás?"}]
response = client.run(agent=english_agent, messages=messages)

print(response.messages[-1]["content"])



import json

from swarm import Agent


def get_weather(location, time="now"):
    """Get the current weather in a given location. Location MUST be a city."""
    return json.dumps({"location": location, "temperature": "65", "time": time})


def send_email(recipient, subject, body):
    print("Sending email...")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return "Sent!"


weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a helpful agent.",
    functions=[get_weather, send_email],
)