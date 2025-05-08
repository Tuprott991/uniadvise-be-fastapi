# Define tools like get_knowledge_tool, create_quiz_tool, create_study_guide_tool, create_exam_tool, etc.
# In backend/app/services/agent_tools.py.
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Dict, Annotated

# Này t ghi đại, tức là mình sẽ traverse knowledge graph để lấy thông tin
from utils.lightrag_functions import query_rag
from decimal import Decimal


class GetInfoInput(BaseModel):
    query: str = Field(..., title="Query", description="Query to get information from knowledge graph")
    mode: Optional[str] = Field("naive", title="Query Mode", description="Query mode ('naive', 'local', 'global', or 'hybrid')")
    only_need_context: Optional[bool] = Field(False, title="Only Need Context", description="Whether to return only the context")

class GetInfoTool(BaseTool):
    """
    Tool lấy thông tin từ knowledge graph
    """
    name: Annotated[str, Field(description="Tool name")] = "get_info_tool"
    description: Annotated[str, Field(description="Tool description")] = "Tool for search university information in knowledge graph"
    args_schema: type[BaseModel] = GetInfoInput

    async def _arun(self, query: str, 
             mode: str = "naive", only_need_context: bool = True) -> Dict:
        """
        Run the tool to query the knowledge graph
        
        Args:
            query: The query string to search for
            mode: Query mode ('naive', 'local', 'global', or 'hybrid')
            only_need_context: Whether to return only the context
            
        Returns:
            Dictionary containing the query results
        """
        result = await query_rag(
            query=query,
            mode=mode,
            only_need_context=only_need_context
        )
        return result
    
    def _run(self, query: str,
             mode: str = "naive", only_need_context: bool = True) -> Dict:
        """
        Synchronous run method - calls the async version
        """
        import asyncio
        return asyncio.run(self._arun(query, mode, only_need_context))

    
    
# class CreateStudyGuideTool(BaseTool):
#     """
#     Tool tạo bài học
#     """
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#     def execute(self, **kwargs) -> Dict:
#         """
#         Hàm thực thi tool
#         """
#         # Lấy bài học
#         result = get_study_guide(kwargs["topic"])
        
#         return result
    
# class CreateExamTool(BaseTool):
#     """
#     Tool tạo đề thi
#     """
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#     def execute(self, **kwargs) -> Dict:
#         """
#         Hàm thực thi tool
#         """
#         # Lấy đề thi
#         result = get_exam_questions(kwargs["topic"])
        
#         return result
    
