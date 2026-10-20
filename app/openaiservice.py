from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE) if OPENAI_API_KEY else None


def analyze_text(text: str) -> dict:
    if not client:
        return {"error": "API key not configured"}
    
    system_prompt = """Ты — эксперт по анализу конкурентов в сфере графического дизайна и анимации. 
Ответ должен быть строго в формате JSON со следующими полями:
{
  "competitor_name": "название или вывод",
  "strong_sides": ["список сильных сторон"],
  "weak_sides": ["список слабых сторон"],
  "key_services": ["ключевые услуги"],
  "pricing_hints": ["подсказки по ценообразованию"],
  "target_audience": "целвая аудитория",
  "design_score": 0-10,
  "animation_potential": 0-10,
  "recommendations": ["рекомендации"],
  "overall_summary": "краткое резюме"
}"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}


def analyze_image(image_base64: str, prompt: str = "") -> dict:
    if not client:
        return {"error": "API key not configured"}
    
    system_prompt = """Ты — эксперт по визуальному анализу конкурентов в сфере графического дизайна и анимации.
Проанализируй изображение/лендинг конкурента. Ответь строго в формате JSON:
{
  "style_analysis": "анализ стиля",
  "color_palette": ["основные цвета"],
  "typography": "типографика",
  "layout_quality": 0-10,
  "design_score": 0-10,
  "animation_potential": 0-10,
  "visual_strengths": ["визуальные сильные стороны"],
  "visual_weaknesses": ["визуальные слабости"],
  "inspiration_takeaways": ["что можно позаимствовать"],
  "recommendations": ["рекомендации"],
  "summary": "краткое резюме"
}"""
    
    user_content = prompt or "Проанализируй это изображение лендинга конкурента"
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_content},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}
