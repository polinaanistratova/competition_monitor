from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import base64
import json
from app.openaiservice import analyze_text, analyze_image
from app.parsingservice import CompetitorParser

app = FastAPI(title="Competition Monitor", version="1.0.0")


@app.get("/")
async def root():
    return {"status": "ok", "message": "Competition Monitor API"}


@app.post("/analyzetext")
async def analyze_text_endpoint(text: str = Form(...)):
    result = analyze_text(text)
    if isinstance(result, str):
        try:
            return JSONResponse(content=json.loads(result))
        except:
            return JSONResponse(content={"raw": result})
    return JSONResponse(content=result)


@app.post("/analyzeimage")
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    prompt: str = Form("")
):
    try:
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode('utf-8')
        result = analyze_image(image_base64, prompt)
        if isinstance(result, str):
            try:
                return JSONResponse(content=json.loads(result))
            except:
                return JSONResponse(content={"raw": result})
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/parsedemo")
async def parsedemo():
    parser = CompetitorParser()
    results = parser.parse_all()
    return {"results": results, "count": len(results)}


@app.get("/history")
async def history():
    parser = CompetitorParser()
    return parser.get_history()
