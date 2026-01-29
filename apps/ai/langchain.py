import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def analyze_records(records):
    examples = [
        {"records": "dog", "analysis": "le chien"},
        {"records": "university", "analysis": "l'université"},
        {
            "records": "bridge",
            "analysis": "la porte",
        },
    ]

    example_prompt = PromptTemplate.from_template(
        "Records: {records}\n Analysis: {analysis}"
    )

    prefix = "You are a personal finance expert. Please provide an analysis based on the expenses and income provided. And at the end, in one sentence, suggest what the user can do to improve their finances."

    prompt_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix="Records: {records}",
        input_variables=["records"],
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro", api_key=os.getenv("GOOGLE_API_KEY")
    )

    llm_chain = prompt_template | llm | StrOutputParser()
    ai_msg = llm_chain.invoke({"records": records})

    return ai_msg
