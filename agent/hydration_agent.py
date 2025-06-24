from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from agent.tools import get_tools

def run_agent(user_input: str, api_key: str, goal_ml: int) -> str:
    try:
        llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192")
        tools = get_tools(goal_ml)

        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        return agent.run(user_input)
    except Exception as e:
        return f"[Agent Error] {str(e)}"
