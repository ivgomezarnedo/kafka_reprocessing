from dataclasses import dataclass

@dataclass
class Odd:
    """ Dataclass for an odd """
    betting_office: str
    odd: float


@dataclass
class Match_odd:
    """ Dataclass for a match odd """
    odd_win: Odd
    odd_lose: Odd
