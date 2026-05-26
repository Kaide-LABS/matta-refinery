import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from packages.outbox.models import Outbox, OutboxDLQ
from typing import Any

async def dispatch_outbox_row(session: AsyncSession, outbox_id: str, adapters: dict[str, Any]):
    # Stage E audit fix: SKIP LOCKED prevents two workers from
    # serializing on the same outbox row. Without it, throughput
    # caps at one worker regardless of replicas. Idempotency is
    # handled at the surface-adapter layer, so skipping a locked
    # row is safe — another worker will pick it up on the next pass.
    stmt = select(Outbox).where(Outbox.id == outbox_id).with_for_update(skip_locked=True)
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()

    if not row:
        return

    if row.state != "pending" or row.next_attempt_at > datetime.datetime.utcnow():
        return

    row.state = "in_flight"
    await session.commit()

    try:
        adapter = adapters.get(row.surface)
        if adapter:
            await adapter.send(row.payload_jsonb)
        
        row.state = "delivered"
        row.last_attempt_at = datetime.datetime.utcnow()
        await session.commit()
    except Exception as e:
        row.delivery_attempts += 1
        row.last_error = str(e)
        if row.delivery_attempts >= 6:
            dlq_entry = OutboxDLQ(
                id=f"dlq-{row.id}",
                original_outbox_id=row.id,
                surface=row.surface,
                payload_jsonb=row.payload_jsonb,
                delivery_attempts=row.delivery_attempts,
                final_error=str(e),
                failed_at=datetime.datetime.utcnow()
            )
            session.add(dlq_entry)
            await session.delete(row)
        else:
            backoff_seconds = [10, 30, 90, 240, 1200, 3600]
            delay = backoff_seconds[min(row.delivery_attempts - 1, len(backoff_seconds) - 1)]
            row.next_attempt_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=delay)
            row.state = "pending"
        
        await session.commit()
