import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from utils.timer import async_timeit


load_dotenv()

@async_timeit
async def build_sql_chain(config):
    
    db_uri = (
            f'postgresql+psycopg2://{config["POSTGRES_USER"]}:'
            f'{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:'
            f'{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'
        )

    db = SQLDatabase.from_uri(
        db_uri,
        view_support=True  # Esta línea permite incluir vistas
    )    

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no está definido en el archivo .env")

    # Este es el constructor correcto con langchain-openai==0.1.3
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",           # Puedes cambiar a "gpt-3.5-turbo" si es necesario
        temperature=0,
        api_key=api_key          # Usa `api_key`, no `openai_api_key`
    )

    # usa agent_type compatible con tu modelo (usa "openai-functions" si da problemas)
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="zero-shot-react-description",
        verbose=True,
    )

    return agent_executor
