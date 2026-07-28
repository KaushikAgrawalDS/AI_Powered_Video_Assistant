from dotenv import load_dotenv
from Utils.Audio_processing import process_input
from Core.transcriber import transcribe_all
from Core.summarizer import summarize,generate_title
from Core.Actionables import extarct_action_items,extarct_key_decisions,extract_questions
from Core.rag_engine import build_rag_chain,ask_question

load_dotenv()

def run_pipeline(source: str, language: str ="english"):
    print("Strating AI Video Assistant")
    chunks = process_input(source)
    transcrpit = transcribe_all(chunks,language = language)
    print("Raw transcrpit")
    
    title = generate_title(transcrpit)

    summary = summarize(transcrpit)
    action_items =extarct_action_items(transcrpit)
    questions = extract_questions(transcrpit)
    decision = extarct_key_decisions(transcrpit)
    rag_chain = build_rag_chain(transcrpit)

    return(
         {
             'title':title,
            'summarize':summary,
            'action_items':action_items,
            'key_decisions': decision,
            'open_question':questions,
            'rag_chain': rag_chain
        }
        
    )
if __name__ == "__main__":
    source = input('Enter a YouTubr URL or Local file path:').strip()
    language = input("Language (English/Hinglish)").strip() or 'english'
    result = run_pipeline(source,language)
    print("\n"+"="*60)
    print(f"Title:{result['title']}")
    print(f"\n Summary :\n{result['summary']}")
    print(f"\nAction Items :\n{result['action_items']}")
    print(f"\nKey Decisions :\n{result['key_decisions']}")
    print(f"\nOpen Questions:\n{result['open_question']}")
    print('= '*60)
    

    #Phase 2 Chat with your meeting via RAG
    print("\n Chat with your meeting {type 'exit','quit','q'}\n")
    rag_chain = result['rag_chain']
    while True:
        question = input("You:").strip()
        if question.lower() in ['exit','quit','q']:
            print('Thank-you  and Goodbye !!!!')
            break
        if not question:
            continue
        answer = ask_question(rag_chain=rag_chain,questions=question)
        print(f"\n Assistant{answer}\n")







