from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model
llm = ChatOpenAI(temperature=0.7, model="gpt-4", openai_api_key=OPENAI_API_KEY)

# Prompt for career recommendation
prompt_recommender = """Bạn là một chuyên gia tư vấn hướng nghiệp. Dựa vào thông tin cá nhân dưới đây, hãy đề xuất 3 ngành nghề phù hợp nhất, sắp xếp theo mức độ phù hợp từ cao đến thấp. Giải thích lý do chọn mỗi ngành.

Trả lời theo định dạng JSON như sau:
    {{
        "career_1": {{
            "name": "Tên ngành nghề",
            "reason": "Lý do chọn ngành nghề này"
        }},
        "career_2": {{
            "name": "Tên ngành nghề",
            "reason": "Lý do chọn ngành nghề này"
        }},
        "career_3": {{
            "name": "Tên ngành nghề",
            "reason": "Lý do chọn ngành nghề này"
        }}
    }}
Thông tin cá nhân:
{user_profile}
"""

# Prompt for learning path
prompt_career_path = """Bạn là một cố vấn học tập. Hãy xây dựng lộ trình học tập 4 năm cho học sinh chuẩn bị học ngành {career} tại trường {university}. Bao gồm:

- Các môn học quan trọng mỗi học kỳ
- Kỹ năng cần rèn luyện theo từng giai đoạn
- Hoạt động ngoại khóa và thực tập nên tham gia
- Gợi ý tài liệu/học online nếu có
- Tips để đạt thành tích tốt và chuẩn bị nghề nghiệp

Trả lời theo định dạng JSON như sau:
{{
    "year_1": {{
        "semester_1": {{
            "subjects": ["Môn học 1", "Môn học 2"],
            "skills": ["Kỹ năng 1", "Kỹ năng 2"],
            "activities": ["Hoạt động 1", "Hoạt động 2"],
            "resources": ["Tài liệu 1", "Tài liệu 2"],
            "tips": ["Tip 1", "Tip 2"]
        }},
        "semester_2": {{
            "subjects": ["Môn học 3", "Môn học 4"],
            "skills": ["Kỹ năng 3", "Kỹ năng 4"],
            "activities": ["Hoạt động 3", "Hoạt động 4"],
            "resources": ["Tài liệu 3", "Tài liệu 4"],
            "tips": ["Tip 3", "Tip 4"]
        }}
    }}
    // Tương tự cho các năm tiếp theo
}}
"""

def recommend_career(user_profile: str):
    """Generate career recommendations based on user profile."""
    prompt = prompt_recommender.format(user_profile=user_profile)
    response = llm.invoke(prompt)
    return response

def generate_learning_path(career: str, university: str):
    """Generate a 4-year learning path for a given career and university."""
    prompt = prompt_career_path.format(career=career, university=university)
    response = llm.invoke(prompt)
    return response