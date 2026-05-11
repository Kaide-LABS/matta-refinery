from sqlalchemy.ext.asyncio import AsyncSession
from packages.outbox.models import Outbox
from packages.schemas.outbox import OutboxEnvelope

async def enqueue_in_tx(session: AsyncSession, envelope: OutboxEnvelope) -> None:
    row = Outbox(
        id=envelope.id,
        surface=envelope.surface,
        payload_jsonb=envelope.payload,
        delivery_attempts=envelope.delivery_attempts,
        next_attempt_at=envelope.next_attempt_at,
        state=envelope.state,
        last_error=envelope.last_error
    )
    session.add(row)
