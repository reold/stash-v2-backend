import random
import time
from uuid import uuid4 as uuid
from .state_pb2 import GameState, Player, PlayerState
from .bindings import MiddlewareWork, MWStatus, MWSignal, MWClient


class CardType:
    NUMBER = 0
    PLUS_2 = 1
    PLUS_4 = 2
    REVERSE = 3


class Engine:
    def __init__(self):
        pass

    def create_game(self, name: str, player_count: int, card_count: int):
        self.state = GameState()
        self.state.creator = name
        self.state.player_count = player_count
        self.state.card_count = card_count
        self.state.creation = str(time.time())

        self.state.id = f"{self.state.creator}-{uuid().hex}"

        creator_player = self.state.players.add()

        creator_player.name = self.state.creator
        creator_player.id = 0
        creator_player.cards[:] = self.random_cards(self.state.card_count)

        self.state.ref = self.random_card(only_type=CardType.NUMBER)

        return MiddlewareWork(
            status=MWStatus.OK,
            signal=MWSignal.CLIENT,
            client=MWClient.APPEND,
            client_id=0,
        )

    def join_game(self, name: str):

        if len(self.state.players) >= self.state.player_count:
            return MiddlewareWork(status=MWStatus.ERROR, status_msg="game is full")

        player = Player()
        player.name = name
        player.id = len(self.state.players)
        player.cards[:] = self.random_cards(self.state.card_count)

        self.state.players.append(player)

        # TODO: shall start with a random player instead
        if len(self.state.players) == self.state.player_count:
            self.state.current = player.id

        return MiddlewareWork(
            status=MWStatus.OK,
            signal=MWSignal.CLIENT_AND_BROADCAST,
            signal_name="player_joined",
            signal_content={
                "opponent": {
                    "name": player.name,
                    "cardCount": len(player.cards),
                    "id": player.id,
                }
            },
            client=MWClient.APPEND,
            client_id=player.id,
        )

    def place_card(self, player_id, card):

        if not self.state.players[player_id]:
            return MiddlewareWork(
                status=MWStatus.ERROR, status_msg="player is not in game"
            )

        if not self.state.current == player_id:
            return MiddlewareWork(status=MWStatus.ERROR, status_msg="not player's turn")

        if not card in self.state.players[player_id].cards:
            return MiddlewareWork(
                status=MWStatus.ERROR, status_msg="player doesn't own card"
            )

        if not self.match_card(self.state.ref, card):
            return MiddlewareWork(
                status=MWStatus.ERROR, status_msg="card doesn't match"
            )

        self.state.ref = card
        self.state.players[player_id].cards.remove(card)

        current_id = self.state.current
        current_i: int = 0

        for pi, player in enumerate(self.state.players):
            if player.id == current_id:
                current_i = pi

        self.state.current = self.state.players[
            (current_i + 1) % self.state.player_count
        ].id

        return MiddlewareWork(
            status=MWStatus.OK,
            signal=MWSignal.BROADCAST,
            signal_name="placed_card",
            signal_content={
                "playerId": player_id,
                "cardCount": len(self.state.players[player_id].cards),
                "ref": self.state.ref,
            },
        )

    def player_state(self, player_id: int):
        player_state = PlayerState()

        player_state.creator = self.state.creator
        player_state.player_count = self.state.player_count
        player_state.card_count = self.state.player_count
        player_state.id = self.state.id
        player_state.player_id = player_id
        player_state.creation = self.state.creation
        player_state.current = self.state.current
        player_state.ref = self.state.ref
        player_state.cards[:] = self.state.players[player_id].cards

        for pi, player in enumerate(self.state.players):
            if pi == player_id:
                continue

            opponent = player_state.opponents.add()
            opponent.name = player.name
            opponent.card_count = len(player.cards)
            opponent.id = pi

        return player_state.SerializeToString()

    def match_card(self, base, new):
        """
        check if `new` card can be placed above `base` card using [UUR](https://github.com/reold/stashdoc/blob/master/UUR.md)
        """

        new_type = new >> 6
        base_type = base >> 6

        # +4 cards
        if new_type == CardType.PLUS_4:
            return True

        new_color = (new >> 4) & 3
        base_color = (base >> 4) & 3

        # colored cards
        if base_color == new_color:
            return True

        # number cards
        if new_type == base_type and base_type == CardType.NUMBER:
            new_number = new & 15
            base_number = base & 15

            print(f"{new_number:b=}")
            print(f"{base_number:b=}")

            if new_number == base_number:
                return True

        self.random_card()

        return False

    def random_card(self, only_type: int = -1):
        """
        generate a random card using [UUR](https://github.com/reold/stashdoc/blob/master/UUR.md)\n
        optionally of `only_type` type
        """
        card = 0

        if only_type == -1:
            card_type = random.choices(
                range(0, 4),
                [0.79166666666, 0.08333333333, 0.04166666666, 0.08333333333],
            )[0]
        else:
            card_type = only_type

        card += card_type << 6

        card_color = random.randint(0, 3)

        if card_type != CardType.PLUS_4:
            card += card_color << 4

        match card_type:

            case CardType.NUMBER:
                card_number = random.randint(0, 9)
                card += card_number

        return card

    def random_cards(self, no_cards: int):
        cards = []

        for _ in range(no_cards):
            cards.append(self.random_card())

        return cards
