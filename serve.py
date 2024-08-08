from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


#creating prompt template
generic_template="Translate the following into {language}:"
prompt=ChatPromptTemplate.from_messages(
    [("system",generic_template),("user","{text}")]
)

parser=StrOutputParser()

#creating chain
chain=prompt|model|parser

#app definition
app=FastAPI(title="Langchain_server",
            version="1.0",
            description="A simple API server using LangChain runnable interfaces")


#adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
