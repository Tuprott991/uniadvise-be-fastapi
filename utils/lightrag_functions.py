import asyncio
import logging
import os
import time
from dotenv import load_dotenv

from lightrag import LightRAG, QueryParam
from lightrag.llm.zhipu import zhipu_complete
from lightrag.llm.openai import openai_complete, gpt_4o_mini_complete
from lightrag.llm.openai import openai_embed
# from lightrag.llm.ollama import ollama_embedding
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status
import asyncio

load_dotenv()

ROOT_DIR = os.getcwd()

WORKING_DIR = f"{ROOT_DIR}/unirag-pg"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# AGE
os.environ["AGE_GRAPH_NAME"] = "unirag"

os.environ["POSTGRES_HOST"] = os.getenv("POSTGRES_HOST", "localhost")
os.environ["POSTGRES_PORT"] = os.getenv("POSTGRES_PORT", "5432")
os.environ["POSTGRES_USER"] = os.getenv("POSTGRES_USER", "rag")
os.environ["POSTGRES_PASSWORD"] = os.getenv("POSTGRES_PASSWORD", "rag")
os.environ["POSTGRES_DATABASE"] = os.getenv("POSTGRES_DATABASE", "rag")


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=gpt_4o_mini_complete,
        llm_model_name="gpt-4o-mini",
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        enable_llm_cache_for_entity_extract=True,
        embedding_func= openai_embed,
        kv_storage="PGKVStorage",
        doc_status_storage="PGDocStatusStorage",
        graph_storage="PGGraphStorage",
        vector_storage="PGVectorStorage",
        auto_manage_storages_states=False,
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag

rag = None

async def initialize_rag_instance():
    global rag
    if rag is None:
        rag = await initialize_rag()

async def query_rag(query: str, mode: str = "naive", only_need_context: bool = True):
    """
    Query the RAG instance with the given parameters.
    
    Args:
        query (str): The query string to search for.
        course_name (str, optional): Name of the course to query. Defaults to None.
        mode (str, optional): Query mode ('naive', 'local', 'global', or 'hybrid'). Defaults to "naive".
        only_need_context (bool, optional): Whether to return only the context. Defaults to True.
        
    Returns:
        dict: The result of the query.
    """
    print("It's work")
    await initialize_rag_instance()
    result = await rag.aquery(
            query=query,
            param=QueryParam(mode="hybrid", only_need_context=only_need_context, top_k=23),
        )
    return result

# async def main():
#     # Initialize RAG instance
#     rag = await initialize_rag()

#     # add embedding_func for graph database, it's deleted in commit 5661d76860436f7bf5aef2e50d9ee4a59660146c
#     rag.chunk_entity_relation_graph.embedding_func = rag.embedding_func

#     # print("==== Trying to test the rag queries ====")
#     # print("**** Start Naive Query ****")
#     # start_time = time.time()
#     # # Perform naive search
#     # print(
#     #     await rag.aquery(
#     #         "What are the top themes in this story?", param=QueryParam(mode="naive")
#     #     )
#     # )
#     # print(f"Naive Query Time: {time.time() - start_time} seconds")
#     # # Perform local search
#     # print("**** Start Local Query ****")
#     # start_time = time.time()
#     # print(
#     #     await rag.aquery(
#     #         "What are the top themes in this story?", param=QueryParam(mode="local")
#     #     )
#     # )
#     # print(f"Local Query Time: {time.time() - start_time} seconds")
#     # # Perform global search
#     # print("**** Start Global Query ****")
#     # start_time = time.time()
#     # print(
#     #     await rag.aquery(
#     #         "What are the top themes in this story?", param=QueryParam(mode="global")
#     #     )
#     # )
#     # print(f"Global Query Time: {time.time() - start_time}")
#     # # Perform hybrid search
#     # print("**** Start Hybrid Query ****")
#     # print(
#     #     await rag.aquery(
#     #         "What are the top themes in this story?", param=QueryParam(mode="hybrid")
#     #     )
#     # )
#     # print(f"Hybrid Query Time: {time.time() - start_time} seconds")


# if __name__ == "__main__":
#     asyncio.run(main())