from typing import NamedTuple


class Clip(NamedTuple):
    id: int
    fname: str
    sentence: str
    split: str


class Utterance(NamedTuple):
    clip_id: int
    loc: int
    label: str
    begin: float = None
    end: float = None


CREATE_TABLE_CLIPS = (
    "create table clips "
    "("
    "id integer, "
    "fname varchar, "
    "sentence varchar, "
    "split varchar, "
    "primary key (id)"
    ")"
)


def _create_table_utterances(utterance_type):
    return (
        f"create table {utterance_type} "
        "("
        "clip_id integer, "
        "loc integer, "
        "label varchar, "
        "begin real, "
        "end real, "
        "primary key (clip_id, loc) "
        ")"
    )


CREATE_TABLE_PHONES = _create_table_utterances("phones")
CREATE_TABLE_WORDS = _create_table_utterances("words")
CREATE_TABLES = (CREATE_TABLE_CLIPS, CREATE_TABLE_PHONES, CREATE_TABLE_WORDS)
DROP_TABLE_CLIPS = "drop table if exists clips"
DROP_TABLE_PHONES = "drop table if exists phones"
DROP_TABLE_WORDS = "drop table if exists words"
DROP_TABLES = (DROP_TABLE_CLIPS, DROP_TABLE_PHONES, DROP_TABLE_WORDS)
INSERT_INTO_CLIPS = "insert into clips values (:id, :fname, :sentence, :split)"
INSERT_INTO_PHONES = "insert into phones values (:clip_id, :loc, :label, :begin, :end)"
INSERT_INTO_WORDS = "insert into words values (:clip_id, :loc, :label, :begin, :end)"


def select_distinct_clips_where_word_equals(n_word_qmarks):
    word_equals = " or ".join(["word = ?"] * n_word_qmarks)
    return (
        "select distinct fname, sentence "
        "from clips "
        "inner join words "
        "on clip_id = id "
        f"where {word_equals}"
    )
