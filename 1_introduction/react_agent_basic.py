from langchain_community.tools import tool
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from dotenv import load_dotenv
import datetime

load_dotenv()

llm = ChatOpenAI(model="gpt-4")

search_tool = TavilySearch(search_depth="basic")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns current date and time in specified format """

    current_time = datetime.datetime.now()
    return current_time.strftime(format)

tools = [search_tool, get_system_time]

agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)

agent.invoke("When SpaceX's last launch and how many days ago was that from this instant?")