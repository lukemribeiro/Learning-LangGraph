from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver


memory = MemorySaver()

class State(TypedDict):
    value: str

def node_a(state: State): 
    print("Node A")
    return Command(
        goto="node_b", 
        update={
            "value": state["value"] + "a"
        }
    )

def node_b(state: State): 
    print("Node B")

    human_response = interrupt("Do you want to go to C or D? Type C/D")

    print("Human Review Values: ", human_response)
    
    if(human_response == "C"): 
        return Command(
            goto="node_c", 
            update={
                "value": state["value"] + "b"
            }
        ) 
    elif(human_response == "D"): 
        return Command(
            goto="node_d", 
            update={
                "value": state["value"] + "b"
            }
        )


def node_c(state: State): 
    print("Node C")
    return Command(
        goto=END, 
        update={
            "value": state["value"] + "c"
        }
    )

def node_d(state: State): 
    print("Node D")
    return Command(
        goto=END, 
        update={
            "value": state["value"] + "d"
        }
)

graph = StateGraph(State)

graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_node("node_c", node_c)
graph.add_node("node_d", node_d)

graph.set_entry_point("node_a") 

app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

initialState = {
    "value": ""
}

first_result = app.invoke(initialState, config, stream_mode="updates")
print(first_result)

# Because of the interrupt, the graph has stopped.
# invoking it now, to continue the same process, 
# requires a Command instance class with a value for the user's coice.

final_result = app.invoke(Command(resume=input()), config=config, stream_mode="updates")
print(final_result)

# running the lines above BEFORE running the graph initalization steps will result in nothing,
# as there is no memory data about before the interrupt.