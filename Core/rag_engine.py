import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage
from operator import itemgetter
from Core.vectorestore import build_vector_store, load_vector_store, get_retriver
 
 
def getllm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )
 
 
def format_doc(docs):
    return "\n\n".join([doc.page_content for doc in docs])
 
 
SYSTEM_PROMPT = """You are expert meeting assistant. Answer the user question based only
on the meeting transcript context provided below, and the conversation so far.You can greet the user if user greet's you
If the answer is not found in the context, say:
"I could not find this information in the transcript which i have got from your input"
 
Always be concise and precise. If quoting someone, mention it clearly.
Use the chat history to resolve follow-up questions (e.g. "what about the second one?"),
but always ground factual answers in the transcript context, not memory of earlier answers.

Also if user give you the tone so explain them in that tone like
 
Context from meeting transcript:
{context}
"""
 
 
def _build_chain(retriver, llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ])
 
    # question drives retrieval; chat_history passes through untouched
    rag_chain = (
        {
            "context": itemgetter("question") | retriver | RunnableLambda(format_doc),
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain
 
 
def build_rag_chain(transcript: str):
    vector_store = build_vector_store(transcript)
    retriver = get_retriver(vector_store, k=5)
    llm = getllm()
    return _build_chain(retriver, llm)
 
 
def load_rag_chain():
    vector_store = load_vector_store()
    retriver = get_retriver(vector_store, k=5)
    llm = getllm()
    return _build_chain(retriver, llm)
 
 
def ask_question(rag_chain, questions: str, chat_history: list | None = None) -> str:
    """
    chat_history: list of (role, text) tuples, e.g. [("user", "..."), ("assistant", "...")]
    Converted here into LangChain message objects for the prompt.
    """
    chat_history = chat_history or []
 
    lc_history = []
    for role, text in chat_history:
        if role == "user":
            lc_history.append(HumanMessage(content=text))
        else:
            lc_history.append(AIMessage(content=text))
 
    print(f"Question: {questions}")
    answer = rag_chain.invoke({"question": questions, "chat_history": lc_history})
    print(f"Answer: {answer}")
    return answer