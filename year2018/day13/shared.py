from typing import NamedTuple

from aoc.map import ParsedMap, Coordinate, Direction


CORNERS = {
    (Direction.NORTH, '/'): Direction.EAST,
    (Direction.EAST, '/'): Direction.NORTH,
    (Direction.SOUTH, '/'): Direction.WEST,
    (Direction.WEST, '/'): Direction.SOUTH,
    (Direction.NORTH, '\\'): Direction.WEST,
    (Direction.WEST, '\\'): Direction.NORTH,
    (Direction.SOUTH, '\\'): Direction.EAST,
    (Direction.EAST, '\\'): Direction.SOUTH,
}


class Cart(NamedTuple):
    location: Coordinate
    direction: Direction
    turn_count: int

    def next_cart(self, next_location: Coordinate, feature: str) -> Cart:
        match feature:
            case '|' | '-':
                return Cart(next_location, self.direction, self.turn_count)
            case '/' | '\\':
                return Cart(next_location, CORNERS[(self.direction, feature)], self.turn_count)
            case '+':
                return Cart(next_location, self.next_turn(), (self.turn_count + 1) % 3)
            case _:
                raise ValueError(f'Unexpected feature at {next_location}: {feature}')

    def next_turn(self) -> Direction:
        match self.turn_count:
            case 0:
                return self.direction.left()
            case 1:
                return self.direction
            case 2:
                return self.direction.right()
            case _:
                raise ValueError(f'Unexpected turn count: {self.turn_count}')


class CartMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, '/\\-|+<>v^')

        self.carts: list[Cart] = []
        for location in self.features['^']:
            self.carts.append(Cart(location, Direction.NORTH, 0))
            self.features['|'].add(location)
        del self.features['^']
        for location in self.features['v']:
            self.carts.append(Cart(location, Direction.SOUTH, 0))
            self.features['|'].add(location)
        del self.features['v']
        for location in self.features['>']:
            self.carts.append(Cart(location, Direction.EAST, 0))
            self.features['-'].add(location)
        del self.features['>']
        for location in self.features['<']:
            self.carts.append(Cart(location, Direction.WEST, 0))
            self.features['-'].add(location)
        del self.features['<']

    def simulate_turn(self) -> list[Coordinate]:
        """Simulate a turn of carts moving. Any collision locations are returned and carts removed."""
        cart_locations = set(cart.location for cart in self.carts)
        self.carts.sort()
        next_carts: list[Cart] = []
        collisions: list[Coordinate] = []
        for cart in self.carts:
            if cart.location in collisions:
                continue
            next_location = cart.location.add(cart.direction.offset())
            if next_location in cart_locations:
                collisions.append(next_location)
                continue
            cart_locations.remove(cart.location)
            cart_locations.add(next_location)
            next_carts.append(cart.next_cart(next_location, self.at_location(next_location)))

        self.carts = [cart for cart in next_carts if cart.location not in collisions]
        return collisions
