""" Functions used in create-documentation notebook"""
import os
import pandas as pd
import numpy as np

button = ":raw-html:`&#10063;`"
csv_header = "\n{}`\n"
csv_entry = ".. csv-table::"
csv_columns = "   :header: {}{}\n"
csv_delim = "   :delim: |"
csv_row = "           {} | {}"
csv_singlerow = "           {}"
bool_entry = ":raw-html:`&#10063;` – {}\n"
open_question = "\n{} \n"
header_question = "\n{}\n"
insert_image = "\n.. image:: {}"
empty_field = ':raw-html:`<form><input type="text" id="fname" name="fname"><br></form>`'


def create_pages(
    codebook,
    waveid,
    lanid,
    q_ids,
    q_filter,
    q_groups,
    q_layout,
    q_text,
    q_sub_text,
    q_categories,
    target_dir,
    image_path,
):
    """ Create reStructuredText files for all groups specified in q_groups. Each file holds all questions that belong to a respective group.
    """

    qids = list(codebook[q_ids].unique())

    data = codebook.copy()
    data = data.set_index([codebook.index, q_ids])

    for idx, qid in enumerate(qids):
        df = data[data.index.get_level_values(q_ids) == qid]
        # Create rst-file.
        file_name = f"{waveid}{lanid}-{qid}"
        group_name = df.loc[df.index[0], q_groups]
        path = f"{target_dir}{file_name}.rst"
        add_to_file(".. _" + file_name + ":", path)
        add_to_file("\n \n .. role:: raw-html(raw) \n        :format: html \n", path)

        add_to_file(
            f"`{qid}` – {group_name}\n{'='*len(file_name*2 + group_name)}", path
        )
        # Insert arrows to next & pervious
        insert_arrows(waveid, lanid, qids, idx, path)
        # Add routing if present:
        if df.loc[df.index[0], q_filter] != "-":
            add_to_file(
                f"*Routing to the question depends on answer in:* :ref:`{waveid}{lanid}-{str(df.loc[df.index[0], q_filter])}`",
                path,
            )
        else:
            pass

        if df[q_layout].all() == "open":
            for i in df.index:
                add_to_file(open_question.format(df.loc[i, q_text]), path)
        elif df[q_layout].all() == "multi":
            add_to_file(header_question.format(df.loc[df.index[0], q_text]), path)
            for i in df.index:
                add_to_file(bool_entry.format(df.loc[i, q_sub_text]), path)
        elif df[q_layout].all() == "table":
            insert_table_question(df, path, q_text, q_sub_text, q_categories)
        elif df[q_layout].all() == "grid":
            insert_grid_question(df, path, q_text, q_sub_text, q_categories)
        elif df[q_layout].all() == "cat":
            insert_cat_question(df, path, q_text, q_categories)
        else:
            raise ValueError(f"Unknown layout type for question {qid}.")

        add_to_file(insert_image.format(f"{image_path}{waveid}-{qid}.png"), path)
        # Insert arrows to next & pervious
        insert_arrows(waveid, lanid, qids, idx, path)


def insert_arrows(waveid, lanid, qids, idx, path):
    """Insert arrows pointing to next and previous question."""
    if idx == 0:
        next_q = waveid + lanid + "-" + qids[idx + 1]
        add_to_file(f"\n\n:ref:`{next_q}` :raw-html:`&rarr;` \n", path)

    elif idx == (len(qids) - 1):
        previous_q = f"{waveid}{lanid}-{qids[idx-1]}"
        add_to_file(f"\n\n:raw-html:`&larr;` :ref:`{previous_q}` \n", path)
    else:
        previous_q = f"{waveid}{lanid}-{qids[idx-1]}"
        next_q = f"{waveid}{lanid}-{qids[idx+1]}"
        add_to_file(
            f"\n\n:raw-html:`&larr;` :ref:`{previous_q}` | :ref:`{next_q}` :raw-html:`&rarr;` \n",
            path,
        )


def insert_table_question(df, path, q_text, q_sub_text, q_categories):
    """Insert question of type table with radio buttons."""
    add_to_file(header_question.format(df.loc[df.index[0], q_text]), path)
    add_to_file(csv_entry.format(), path)
    add_to_file(csv_delim.format(), path)
    add_to_file(csv_columns.format(",", df.loc[df.index[0], q_categories]), path)
    for i in df.index:
        items = df.loc[i, q_categories].count(",")
        add_to_file(
            csv_row.format(df.loc[i, q_sub_text], (button + "|") * (items) + button),
            path,
        )


def insert_grid_question(df, path, q_text, q_sub_text, q_categories):
    """Insert question of type grid with entry fields."""
    add_to_file(header_question.format(df.loc[df.index[0], q_text]), path)
    add_to_file(csv_entry.format(), path)

    if pd.isna(df.loc[df.index[0], q_categories]) == False:
        add_to_file(csv_delim.format(), path)
        add_to_file(csv_columns.format(",", df.loc[df.index[0], q_categories]), path)
        for i in df.index:
            items = df.loc[i, q_categories].count(",")
            add_to_file(
                csv_row.format(
                    df.loc[i, q_sub_text], (f"{empty_field} |") * items + empty_field
                ),
                path,
            )
    else:
        add_to_file(f"{csv_delim.format()} \n", path)
        for i in df.index:
            add_to_file(csv_row.format(df.loc[i, q_sub_text], empty_field), path)


def insert_cat_question(df, path, q_text, q_categories):
    """Insert question of type cat with categorical answers."""
    add_to_file(header_question.format(df.loc[df.index[0], q_text]), path)
    add_to_file(csv_entry.format(), path)
    add_to_file(csv_delim.format(), path)
    add_to_file(csv_columns.format("", df.loc[df.index[0], q_categories]), path)
    for i in df.index:
        items = df.loc[i, q_categories].count(",")
        add_to_file(csv_singlerow.format((button + "|") * (items) + button), path)


def add_to_file(msg, path):
    """ Adds line to file specified in path."""
    with open(path, "a") as f:
        f.write(f"{msg} \n")
