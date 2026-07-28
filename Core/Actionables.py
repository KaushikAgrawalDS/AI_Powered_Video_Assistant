# Action,Decision and Questtion

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnablePassthrough
import os

def get_llm():
    return ChatMistralAI(model = "mistral-small-latest",
                         mistral_api_key= os.getenv("MISTRAL_API_KEY"),
                         temperature=0.2)

def build_chain(system_prompt : str) -> str:
    llm = get_llm()
    return (
        RunnablePassthrough()| RunnableLambda(lambda x:{"text":x})|
            ChatPromptTemplate.from_messages([("system",system_prompt),("human","{text}"),])|
            llm|StrOutputParser() 
    )

def extarct_action_items(tarnscrpit:str) -> str:
    chain = build_chain("""
                        You are an expert meeting analyst. from the meeting transcrpit
                        extract all action items.For each provide:\n
                        -Task Descrption \n
                        -Owner (Who is responsible)\n
                        -Deadline (if mentioned , else write "Notspecified")\n\n
                        Format as numbered list. If none found say "No action items found"
                        """
                        )
    return chain.invoke(tarnscrpit)

def extarct_key_decisions(tarnscrpit:str) -> str:
    chain = build_chain("""
                        You are an expert meeting analyst. from the meeting transcrpit
                        extract all key decisions made.Foramt as a numbered list
                        If none found say "No key Decision found"
                        """
                        )
    return chain.invoke(tarnscrpit)

def extract_questions(tarnscrpit:str) -> str:
    chain = build_chain("""
                        You are an expert meeting analyst. from the meeting transcrpit
                        extract all unresolved questions or topics follow up. Format as anumbered list
                        Format as numbered list. If none found say "No action items found"
                        """
                        )
    return chain.invoke(tarnscrpit)
     