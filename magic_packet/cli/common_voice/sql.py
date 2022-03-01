from typing import NamedTuple, Optional


class Clip(NamedTuple):
    id: int
    fname: str
    sentence: str
    split: str


class Utterance(NamedTuple):
    clip_id: int
    loc: int
    label: str
    begin: Optional[float] = None
    end: Optional[float] = None


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


def _label_equal_qmarks(n_qmarks):
    return " or ".join(["label = ?"] * n_qmarks)


def select_clips_where_id_between():
    return "select * " "from clips " "where id between ? and ?"


def select_clips_where_words_equal(n_words):
    return (
        "select distinct c.* "
        "from clips as c "
        "inner join words "
        "on id = clip_id "
        f"where {_label_equal_qmarks(n_words)} "
    )


def select_pct_of_clips_where_words_not_equal(n_words):
    return (
        "select distinct c.* "
        "from clips as c "
        "left join "
        f"(select clip_id from words where {_label_equal_qmarks(n_words)}) "
        "on id = clip_id "
        "where clip_id is null "
        "and abs(cast(random() as real)) / 9223372036854775808 < ? "
    )
