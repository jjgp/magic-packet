create_table_clips = (
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
        "primary key (clip_id, loc)) "
        ")"
    )


create_table_phones = _create_table_utterances("phones")
create_table_words = _create_table_utterances("words")
drop_all_tables = "drop table if exists clips, phones, words"
insert_into_clips = "insert into clips values (?, ?, ?, ?)"
insert_into_phones = "insert into phones values (?, ?, ?, ?, ?)"
insert_into_words = "insert into words values (?, ?, ?, ?, ?)"


def select_distinct_clips_where_word_equals(n_word_qmarks):
    word_equals = " or ".join(["word = ?"] * n_word_qmarks)
    return (
        "select distinct fname, sentence "
        "from clips "
        "inner join words "
        "on clip_id = id "
        f"where {word_equals}"
    )
