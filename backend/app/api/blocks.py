from fastapi import APIRouter, HTTPException
from typing import List, Optional
from sqlmodel import Session, select
from ..models import Block
from ..db import engine
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class BlockCreate(BaseModel):
    user_id: str
    title: str
    start_iso: datetime
    end_iso: datetime

class BlockUpdate(BaseModel):
    title: Optional[str] = None
    start_iso: Optional[datetime] = None
    end_iso: Optional[datetime] = None
    completed: Optional[bool] = None

@router.post("/", response_model=Block)
def create_block(data: BlockCreate):
    block = Block(user_id=data.user_id, title=data.title, start_iso=data.start_iso, end_iso=data.end_iso)
    with Session(engine) as session:
        session.add(block)
        session.commit()
        session.refresh(block)
    return block

@router.get("/", response_model=List[Block])
def list_blocks():
    with Session(engine) as session:
        blocks = session.exec(select(Block)).all()
    return blocks

@router.get("/{block_id}", response_model=Block)
def get_block(block_id: int):
    with Session(engine) as session:
        block = session.get(Block, block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block

@router.patch("/{block_id}", response_model=Block)
def update_block(block_id: int, patch: BlockUpdate):
    with Session(engine) as session:
        block = session.get(Block, block_id)
        if not block:
            raise HTTPException(status_code=404, detail="Block not found")
        update_data = patch.dict(exclude_unset=True)
        for k, v in update_data.items():
            if hasattr(block, k):
                setattr(block, k, v)
        session.add(block)
        session.commit()
        session.refresh(block)
    return block

@router.delete("/{block_id}")
def delete_block(block_id: int):
    with Session(engine) as session:
        block = session.get(Block, block_id)
        if not block:
            raise HTTPException(status_code=404, detail="Block not found")
        session.delete(block)
        session.commit()
    return {"ok": True}
