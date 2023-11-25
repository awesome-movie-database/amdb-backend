from typing import TypeVar

from amdb.domain.constants import Unset


class Entity:
    """Base class for Entities"""

    def update(self, **fields) -> None:
        """
        Updates Entity's fields where `fields` values
        are not `Unset`.

        Example:

        .. code-block::python
        @dataclass
        class Foo(Entity):

            bar: int
            baz: Optional[float]


        class UpdateFoo(Service):

            def __call__(
                self,
                foo: Foo,
                bar: Union[int, Type[Unset]] = Unset,
                baz: Union[float, None, Type[Unset]] = Unset,
            ) -> None:
                foo.update(bar=bar, baz=baz)

        foo = Foo(1, 1.5)
        update_foo = UpdateFoo()
        update_foo(foo=foo, bar=2)
        print(foo) # Foo(bar=2, baz=1.5)
        """
        for name, value in fields.items():
            if value == Unset:
                continue
            setattr(self, name, value)


Entity_T = TypeVar("Entity_T", bound=Entity)
