from typing import TypeVar

from amdb.domain.constants import Unset


class Entity:
    """Base class for Entities"""

    def _update(self, **fields) -> None:
        """
        Updates Entity's fields where `fields` values
        are not `Unset`.

        Example:

        .. code-block::python
        @dataclass
        class Foo(Entity):

            bar: int
            baz: Optional[float]

            def update(
                self,
                bar: Union[int, Type[Unset]] = Unset,
                baz: Union[float, None, Type[Unset]] = Unset,
            ):
                self._update(bar=bar, baz=baz)

        foo = Foo(1, 1.5)
        foo.update(bar=2)
        print(foo) # Foo(bar=2, baz=1.5)
        """
        for name, value in fields.items():
            if value == Unset:
                continue
            setattr(self, name, value)


Entity_T = TypeVar("Entity_T", bound=Entity)
