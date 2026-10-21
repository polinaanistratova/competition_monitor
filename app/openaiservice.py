from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL, YANDEX_FOLDER_ID
import json
import re

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE, project=YANDEX_FOLDER_ID) if OPENAI_API_KEY else None


def _extract_json(content: str) -> dict:
    if not content:
        raise ValueError("Empty response from model")

    text = content.strip()

    # Убираем markdown-блоки с json
    text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()

    # Пробуем распарсить как есть
    try:
        return json.loads(text)
    except Exception:
        pass

    # Ищем первый JSON-объект в тексте
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception as e:
            raise ValueError(f"Failed to parse JSON: {e}\nRaw: {match.group(0)[:200]}...")

    raise ValueError(f"No JSON object found in response: {text[:200]}...")


def analyze_text(text: str) -> dict:
    if not client:
        return {"error": "API key not configured"}

    system_prompt = """Ты — эксперт по анализу конкурентов в сфере графического дизайна и анимации.
Ответь ТОЛЬКО валидным JSON без пояснений, без ```json```, без текста до или после.

Строго используй следующую структуру:
{
  "competitor_name": "название или вывод",
  "strong_sides": ["список сильных сторон"],
  "weak_sides": ["список слабых сторон"],
  "key_services": ["ключевые услуги"],
  "pricing_hints": ["подсказки по ценообразованию"],
  "target_audience": "целевая аудитория",
  "design_score": 0,
  "animation_potential": 0,
  "recommendations": ["рекомендации"],
  "overall_summary": "краткое резюме"
}

Оцени design_score и animation_potential по шкале от 0 до 10."""

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
        content = response.choices[0].message.content
        return _extract_json(content)
    except Exception as e:
        return {"error": str(e)}


def analyze_image(image_base64: str, prompt: str = "") -> dict:
    if not client:
        return {"error": "API key not configured"}

    system_prompt = """Ты — эксперт по визуальному анализу конкурентов в сфере графического дизайна и анимации.
Проанализируй изображение/лендинг конкурента.
Ответь ТОЛЬКО валидным JSON без пояснений, без ```json```, без текста до или после.

Строго используй следующую структуру:
{
  "style_analysis": "анализ стиля",
  "color_palette": ["основные цвета"],
  "typography": "типографика",
  "layout_quality": 0,
  "design_score": 0,
  "animation_potential": 0,
  "visual_strengths": ["визуальные сильные стороны"],
  "visual_weaknesses": ["визуальные слабости"],
  "inspiration_takeaways": ["что можно позаимствовать"],
  "recommendations": ["рекомендации"],
  "summary": "краткое резюме"
}

Все оценки — от 0 до 10."""

    user_content = prompt or "Проанализируй это изображение лендинга конкурента. Дай объективную оценку с акцентом на визуальный стиль и потенциал анимации."

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
        content = response.choices[0].message.content
        return _extract_json(content)
    except Exception as e:
        return {"error": str(e)}
