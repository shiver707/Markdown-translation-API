import os
import marko
from openai import OpenAI
from dotenv import load_dotenv
from marko.block import CodeBlock
from marko.inline import RawText, Link

#.env 파일에 저장된 환경변수(API 키)를 불러옵니다.
load_dotenv()

#OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def translate_text_node(text: str, target_language: str) -> str:
    """순수 텍스트만 LLM에 보내어 번역합니다."""
    if not text.strip():
        return text

    system_prompt = (
        f"너는 문서 전문 번역기야. 주어진 관련 문장을 {target_language}로 번역해줘.\n"
        f"조건: 개발자 관용어(API, Webhook, Repository 등)는 자연스럽게 두거나 그대로 두고, 문맥을 살려 번역해."
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

def process_node(node, target_language: str):
    """마크다운 노드를 재귀적으로 탐색하며 번역이 필요한 곳만 처리합니다."""
    if isinstance(node, CodeBlock):
        return  #코드 블록은 무시

    if isinstance(node, RawText):
        node.children = translate_text_node(node.children, target_language)
        return

    if hasattr(node, "children") and isinstance(node.children, list):
        for child in node.children:
            if isinstance(node, Link) and child == node.dest:
                continue
            process_node(child, target_language)

def translate_markdown_by_splitting(markdown_text: str, target_language: str) -> str:
    """마크다운을 쪼개서 번역한 뒤 다시 합칩니다."""
    doc = marko.parse(markdown_text)
    process_node(doc, target_language)
    return marko.render(doc)

#VS Code에서 테스트 실행
if __name__ == "__main__":
    
    test_md = "# Introduction\n\nWelcome to my repository. Check this `npm install` command."
    
    print(" - translation has been begun - ")
    result = translate_markdown_by_splitting(test_md, "Korean")
    print("\n- translation has been completed \n")
    print(result)