from strands import Agent
from tools import get_weather

agent = Agent(
    system_prompt="You are a helpful weather assistant. Use the get_weather tool to answer questions about weather.",
    tools=[get_weather],
)

if __name__ == "__main__":
    response = agent("What's the weather in Dallas, TX?")
    print(response)
