from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Fullname:
    firstname: str
    middlename: str
    lastname: str

    def __str__(self) -> str:
        return f"{self.firstname} {self.middlename} {self.lastname}"

    def __repr__(self) -> str:
        return f"Fullname({self.firstname}, {self.middlename}, {self.lastname})"
