from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from database import SessionLocal, init_db, Document
from misc import add_qr_to_docx

app = FastAPI()
# Настройка CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # разрешите все методы
    allow_headers=["*"],  # разрешите все заголовки
)

# Инициализация базы данных
init_db()


# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload/")
async def upload_document(
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...)
):
    db: Session = next(get_db())

    # Создание нового документа
    new_document = Document(title=title, description=description)

    # Сохранение в базу данных
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    # Сохранение файла (если необходимо)
    input_docx_path = f"./uploads/{file.filename}"
    with open(input_docx_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Генерация QR-кода из названия и описания
    qr_data = f"Title: {title}\nDescription: {description}"
    output_docx_path = f"./uploads/updated_{file.filename}"

    # Добавление QR-кода в документ
    add_qr_to_docx(input_docx_path, qr_data, output_docx_path)

    # Возвращаем обновленный документ
    return FileResponse(output_docx_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"updated_{file.filename}")


@app.get("/documents")
def read_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    return documents

