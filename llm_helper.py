from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile",temperature=0.7,max_tokens=1024)


if __name__ == "__main__":
    response = llm.invoke("Write a short motivational post about learning AI.")
    print(response.content)





