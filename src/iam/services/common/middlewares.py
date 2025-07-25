from collections.abc import Callable, Coroutine
from typing import Any

from iam.domain.shared.events import Event, EventTracker
from iam.services.common.markers import Command, Middleware
from iam.services.ports.event_publisher import EventPublisher
from iam.services.ports.id_provider import IdProvider
from iam.services.ports.time_provider import TimeProvider
from iam.services.ports.transaction import Transaction


class EventProcessorMiddleware[C: Command, R](Middleware[C, R]):
    def __init__(
        self,
        event_tracker: EventTracker,
        publisher: EventPublisher,
        id_provider: IdProvider,
        time_provider: TimeProvider,
    ) -> None:
        self._event_tracker = event_tracker
        self._event_publisher = publisher
        self._time_provider = time_provider
        self._id_provider = id_provider

    async def handle(self, request: C, process: Callable[[C], Coroutine[Any, Any, R]]) -> R:
        response = await process(request)
        events = self._event_tracker.raise_events()

        for event in events:
            prepared_event = self._prepare_event(event)
            await self._event_publisher.publish(prepared_event)

        return response

    def _prepare_event(self, event: Event) -> Event:
        event.set_event_date(event_date=self._time_provider.provider_current_time())
        event.set_event_id(event_id=self._id_provider.generate_event_id())
        return event


class CommitionMiddleware[C: Command, R](Middleware[C, R]):
    def __init__(self, transaction: Transaction) -> None:
        self._transaction = transaction

    async def handle(self, request: C, process: Callable[[C], Coroutine[Any, Any, R]]) -> R:
        response = await process(request)
        await self._transaction.commit()
        return response
