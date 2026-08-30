"""Abstract interface for database implementations.

Concrete databases (SQLite, PostgreSQL, etc.) should implement this interface
without making the rest of the application depend on a particular driver.
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from types import TracebackType
from typing import Self


Parameters = Sequence[object] | Mapping[str, object] | None


class AbstractDB(ABC):
    """Minimal synchronous database interface."""

    @abstractmethod
    def connect(self) -> None:
        """Open the database connection."""

    @abstractmethod
    def execute(self, query: str, parameters: Parameters = None) -> None:
        """Execute an INSERT, UPDATE, DELETE, or DDL statement."""

    @abstractmethod
    def fetch_one(
        self, query: str, parameters: Parameters = None
    ) -> Mapping[str, object] | None:
        """Return the first matching row, or ``None``."""

    @abstractmethod
    def fetch_all(
        self, query: str, parameters: Parameters = None
    ) -> list[Mapping[str, object]]:
        """Return all matching rows."""

    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""

    def __enter__(self) -> Self:
        """Allow ``with Database(...) as db:`` usage."""
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
