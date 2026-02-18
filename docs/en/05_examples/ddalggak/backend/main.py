import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

# 허용할 파일 확장자 (yaml, md, json 등)
ALLOWED_EXTENSIONS = {".yaml", ".yml", ".md", ".json", ".txt"}
# 최대 파일 크기 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024
# 업로드 디렉토리
UPLOAD_DIR = Path(__file__).parent / "uploads"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    yaml, md, json, txt 등 파일 업로드 API.
    파일은 backend/uploads/ 에 저장됩니다.
    """
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"허용되지 않는 확장자입니다. 허용: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # 파일 크기 검증
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"파일 크기 제한 초과 (최대 {MAX_FILE_SIZE // 1024 // 1024}MB)",
        )

    # 업로드 디렉토리 생성
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # 저장 파일명: 원본명_고유ID.확장자 (중복 방지)
    unique_id = uuid.uuid4().hex[:8]
    safe_name = Path(file.filename or "unnamed").stem
    saved_name = f"{safe_name}_{unique_id}{suffix}"
    saved_path = UPLOAD_DIR / saved_name

    with open(saved_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "saved_as": saved_name,
        "path": str(saved_path),
        "size": len(content),
        "content_type": file.content_type or "application/octet-stream",
    }