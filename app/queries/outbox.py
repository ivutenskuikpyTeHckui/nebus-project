from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.databases.orm.outbox import Outbox


async def get_unpublished_outbox(db: AsyncSession, limit: int = 20) -> list[Outbox]:
    statement = (
        select(Outbox)
        .where(Outbox.published_at.is_(None))
        .order_by(Outbox.created_at)
        .limit(limit)
        .with_for_update(skip_locked=True)
    )
    return list((await db.execute(statement)).scalars().all())


def mark_outbox_published(row: Outbox) -> None:
    row.published_at = datetime.now(timezone.utc)
