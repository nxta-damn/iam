from typing import cast
from uuid import uuid4

from iam.adapters.persistence.uow_tracker import UoWTracker
from iam.adapters.user_proxy import UserProxy
from iam.domain.identity.contracts.factory import UserFactory
from iam.domain.identity.events import UserCreated
from iam.domain.identity.user import IdentifiedUser, UserType
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.user_id import UserIdentity


class UserFactoryImpl(UserFactory):
    def __init__(self, uow_tracker: UoWTracker) -> None:
        self.uow_tracker = uow_tracker

    async def create_user(
        self, fullname: Fullname, username: str, password: bytes, user_type: UserType
    ) -> IdentifiedUser:
        user_id = UserIdentity(uuid4())
        user = IdentifiedUser(
            identity=user_id, fullname=fullname, username=username, password=password, user_type=user_type
        )
        event = UserCreated(
            identity=user_id, fullname=fullname, username=username, password=password, user_type=user_type
        )
        user_proxy = UserProxy(user=user, uow_tracker=self.uow_tracker)

        user.add_event(event=event)
        return cast("IdentifiedUser", user_proxy)
