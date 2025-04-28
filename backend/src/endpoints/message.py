import asyncio
import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from starlette.responses import StreamingResponse
from core.sse_manager import remove_connection, add_connection, send_message_to_user
from models import Message
from schemas.message import MessageCreate, MessageOut
from database import get_db
from repositories.message import MessageRepository
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/messages", tags=["Messages"], dependencies=[Depends(get_current_user)])
message_repo = MessageRepository()

@router.get("/", response_model=list[MessageOut])
async def get_conversations(user_id: UUID, db: Session = Depends(get_db)):
    return message_repo.get_all_for_user(db,user_id)


@router.get("/direct", response_model=list[MessageOut])
def get_conversation(
    sender_id: UUID = Query(...),
    receiver_id: UUID = Query(...),
    db: Session = Depends(get_db)
) -> list[Message]:
    return message_repo.get_conversation(db, sender_id, receiver_id)


@router.get("/stream")
async def stream_messages(current_user=Depends(get_current_user)):
    user_id = str(current_user.id)
    queue = asyncio.Queue()
    add_connection(user_id, queue)

    async def event_stream():
        try:
            while True:
                message = await queue.get()
                yield f"data: {message}\n\n"
        finally:
            remove_connection(user_id)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@router.post("/send", response_model=MessageOut)
async def send_message(
    message: MessageCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Message:
    # Attach the sender from token to prevent faking sender_id
    message.sender_id = current_user.id

    saved = message_repo.create(db, message)
    message_json = json.dumps(MessageOut.model_validate(saved).model_dump())

    # Send message to both sender and receiver (like WhatsApp echo)
    send_message_to_user(str(saved.receiver_id), message_json)
    send_message_to_user(str(saved.sender_id), message_json)

    return saved