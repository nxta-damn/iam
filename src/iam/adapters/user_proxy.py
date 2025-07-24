from iam.adapters.persistence.uow_tracker import UoWTracker
from iam.domain.identity.user import IdentifiedUser, UserType
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.user_id import UserIdentity


class UserProxy:
    def __init__(self, user: IdentifiedUser, uow_tracker: UoWTracker) -> None:
        self.user = user
        self.uow_tracker = uow_tracker

    def change_fullname(self, fullname: Fullname) -> None:
        self.user.change_fullname(fullname=fullname)
        self.uow_tracker.register_dirty(model=self.user)

    def change_username(self, username: str) -> None:
        self.user.change_username(username=username)
        self.uow_tracker.register_dirty(model=self.user)

    def change_password(self, password: bytes) -> None:
        self.user.change_password(password=password)
        self.uow_tracker.register_dirty(model=self.user)

    @property
    def identity(self) -> UserIdentity:
        return self.user.identity

    @property
    def fullname(self) -> Fullname:
        return self.user.fullname

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def password(self) -> bytes:
        return self.user.password

    @property
    def user_type(self) -> UserType:
        return self.user.user_type
