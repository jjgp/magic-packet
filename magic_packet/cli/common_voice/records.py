from typing import NamedTuple

from magic_packet.database import sql_table, sql_update


class AbbrClips(NamedTuple):
    fname: str
    sentence: str


@sql_table(primary_keys=["id"])
class Clips(NamedTuple):
    id: int
    fname: str
    sentence: str
    split: str


@sql_table(primary_keys=["clip_id", "loc"])
class Phones(NamedTuple):
    clip_id: int
    loc: int
    phone: str
    begin: float
    end: float


@sql_table(primary_keys=["clip_id", "loc"])
class Words(NamedTuple):
    clip_id: int
    loc: int
    word: str
    begin: float = None
    end: float = None


@sql_update(Words)
class Alignments(NamedTuple):
    begin: float
    end: float
