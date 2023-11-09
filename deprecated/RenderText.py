import datetime

# 변수 해석과 템플릿 렌더링을 담당하는 함수
def render_text(text, variables):
    for key, value in variables.items():
        if callable(value):  # 값이 호출 가능한 객체(함수 등)인지 확인
            value = value()  # 함수를 호출해서 결과를 얻습니다.
        placeholder = "{" + key + "}"
        template = template.replace(placeholder, str(value))
    return template



    