from langchain_mistralai import  ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda,RunnablePassthrough

import os 

def get_llm():
    return ChatMistralAI(model = "mistral-small-latest",
                         mistral_api_key= os.getenv("MISTRAL_API_KEY"),
                         temperature=0.5)

def split_transcript(transcript: str )-> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap = 200,

    )
    return splitter.split_text(transcript)

def summarize(transcrpit: str) -> str:
    llm = get_llm()
    map_prompt = ChatPromptTemplate.from_messages(
        [
        ("system","Summarize this portion of a meeting transcrpit concisely"),
        ("human","{text}"),
        ]
    )
    map_chain = map_prompt | llm | StrOutputParser()
    chunks = split_transcript(transcrpit)
    chunks_summaries = [map_chain.invoke({'text':chunk}) for chunk in chunks]
    
    combined = "\n\n".join(chunks_summaries)

    combined_prompt =  ChatPromptTemplate.from_messages(
        [
        (
            "system","""You are an expert summarizer. Combine these partial summaries",
            "into one final professional meeting summary in bullet point""",
        ),("human","{text}"),
        ]
    )

    final_chain = RunnablePassthrough() | RunnableLambda(lambda x : {"text":x} )| combined_prompt| llm | StrOutputParser()
    return final_chain.invoke(combined)

def generate_title(transcrpit: str) -> str:
    llm = get_llm()
    title_chain =(
        RunnablePassthrough()| RunnableLambda(lambda x : {"text": x}) |
        ChatPromptTemplate.from_messages([
            ("system","""Based on the meeting transcrpit, generate a shor professional summary meeting title
             (Max of 8 words). Only return the title , nothing else.""",),
              ("human","{text}"),]
        ) | llm | StrOutputParser()
        
    )
    return title_chain.invoke(transcrpit[:3000])