from database.uni_info_db import get_all_universities, get_university_sections_id

def all_universities_json():
    """
    Lấy thông tin tất cả các trường đại học từ database và chuyển đổi thành định dạng JSON.
    """
    universities = get_all_universities()
    universities_json = []
    for university in universities:
        university_json = {
            "id": university["id"],
            "name": university["name"]
        }
        universities_json.append(university_json)

    return universities_json


def process_data(list_data: list) -> list:
    str = list_data[4]['content']
    str = str.split('\n\n\n## Thẻ')[0]
    list_data[4]['content'] = str
    return list_data




def format_university_sections(university_id: int):
    """
    Lấy thông tin các section của trường đại học từ database và chuyển đổi thành định dạng JSON.
    """
    sections = get_university_sections_id(university_id)
    # Chuyển đổi danh sách các section thành định dạng JSON
    sections_json = []
    for section in sections:
        section_json = {
            "id": section["university_id"],
            "section": section["section_title"],
            "content": section["content"]
        }
        sections_json.append(section_json)
    return process_data(sections_json)


# print(all_universities_json())

