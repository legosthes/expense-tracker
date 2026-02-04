import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def analyze_records(records, days=30):
    examples = [
        {
            "records": "{{'amount': Decimal('12.34'), 'type': 'Expense', 'category': 'Restaurants'}}, {{'amount': Decimal('56.00'), 'type': 'Expense', 'category': 'Life & Entertainment'}}, {{'amount': Decimal('100.00'), 'type': 'Expense', 'category': 'Shopping'}}",
            "analysis": "You've spent 12.34 in total on Restaurants, 56.00 in total on Life & Entertainment, 100.00 on Shopping.",
        },
        {
            "records": "{{'amount': Decimal('1.00'), 'type': 'Expense', 'category': 'Transportation'}}, {{'amount': Decimal('23.00'), 'type': 'Expense', 'category': 'Restaurants'}}, {{'amount': Decimal('12.00'), 'type': 'Expense', 'category': 'Restaurants'}}",
            "analysis": "You've spent 1.00 in total on Transportation, 35.00 in total on Restaurants.",
        },
        {
            "records": "{{'amount': Decimal('5000.00'), 'type': 'Income', 'category': 'Income'}}, {{'amount': Decimal('100000.00'), 'type': 'Income', 'category': 'Income'}}, {{'amount': Decimal('12.00'), 'type': 'Expense', 'category': 'Shopping'}}",
            "analysis": "You've had a total income of 105000.00 and you've spent 12.00 in total on Shopping.",
        },
    ]

    example_prompt = PromptTemplate.from_template(
        "Records: {records}\n Analysis: {analysis}"
    )

    prefix = "You are a personal finance expert. Please provide an analysis based on the expenses and income that were recorded within {days} days. And at the end, in one sentence, suggest what the user can do to improve their finances."

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

    records_str = ", ".join(str(record) for record in records)

    llm_chain = prompt_template | llm | StrOutputParser()
    ai_msg = llm_chain.invoke({"records": records_str, "days": days})

    return ai_msg
