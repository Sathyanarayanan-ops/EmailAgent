# EmailAgent


First set up lang graph , 

Learned concepts - State 

Next is Tavily search engine to give llm the ability to handle websearch 

Below, we implement a BasicToolNode that checks the most recent message
in the state and calls tools if the message contains tool_calls. 

We will later replace this with LangGraph's prebuilt ToolNode to speed things up,
but building it ourselves first is instructive.
