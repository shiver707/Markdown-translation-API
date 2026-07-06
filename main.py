import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from translator import translate_markdown_by_splitting

#FastAPI 앱 초기화
app = FastAPI(
    title="Open Source Markdown translation API",
    description="API for LLM-based translation that preserves Markdown structure",
    version="1.0.0"
)

#사용자가 API를 호출할 때 보낼 데이터의 형식을 정의 Dato Transfer Object
class TranslationRequest(BaseModel):
    markdown_text: str = Field(..., description="Original Markdown text to be translated")
    target_language: str = Field("Korean", description="target langage (예: Korean, English, Japanese)")

#실제 번역을 수행하는 엔드포인트/주소를 생성.
@app.post("/api/v1/translate")
async def translate_markdown_api(payload: TranslationRequest):
    try:
        #요청받은 데이터에서 텍스트와 언어를 꺼냄.
        source_text = payload.markdown_text
        target_lang = payload.target_language
        
        #우리가 Step 1에서 만든 완벽한 쪼개기 번역 함수를 실행.
        translated_text = translate_markdown_by_splitting(source_text, target_lang)
        
        #에러 없을경우 결과를 반환.
        return {
            "status": "success",
            "target_language": target_lang,
            "translated_markdown": translated_text
        }
        
    except Exception as e:
        #에러가 발생하면 500 에러와 함께 원인을 반환.
        raise HTTPException(status_code=500, detail=str(e))

#서버가 잘 켜졌는지 확인하기 위한 기본 주소
@app.get("/")
def read_root():
    return {"message": "API of Markdown transation correctly is working"}