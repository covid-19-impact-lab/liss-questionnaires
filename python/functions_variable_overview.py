import os
import pandas as pd
import numpy as np


def create_description_table(
    table, waves, language, return_links_as_symbols=True, routing=True,
):
    """ Create variable overview from data description table of liss data."""
    table = table.copy()
    # Fill in nans as -.
    table = table.fillna("-")
    # Drop columns.
    table = table.drop(["label_english", "categories_english"], axis=1)
    table = table[table["question_group"] != "-"]
    table = table[table["Variable"] != "-"]

    # Drop waves that should not be included in table.
    wave_columns = table.columns[table.columns.str.contains("wave#")]
    selected_waves = [f"wave#{i}" for i in waves]
    drop_waves = set(wave_columns) - set(selected_waves)
    table.drop(drop_waves, axis=1)

    # Drop observations that are not included in selected waves.
    drop_indices = table[table[selected_waves] == "-"].index
    table.drop(drop_indices, axis=0)

    # Create question group id.
    for i in waves:
        table[f"group_w{i}"] = np.where(
            table[f"wave#{i}"] == "-", table[f"wave#{i}"], table["question_group"]
        )

    # create question link ":ref:`wNL-{question_group}`.
    for i in waves:
        if return_links_as_symbols:
            table[f"group_w{i}"] = table[f"group_w{i}"].apply(
                lambda x: f":ref:`🔗 <w{str(i)}{language}-{x}>`"
            )
        else:
            table[f"group_w{i}"] = table[f"group_w{i}"].apply(
                lambda x: f"w{str(i)}{language}-{x}"
            )
        table[f"group_w{i}"] = np.where(
            table[f"group_w{i}"].str.contains("--") == False, table[f"group_w{i}"], "-"
        )

    # Final formatting
    # Replace ordered categoricals to drop 'ordered' column.
    table["Type"] = np.where(
        table["ordered"] != True, table["Type"], "Ordered Categorical"
    )

    # Ensure correct formatting for reference period column,
    # create as new column to esnure it is last in table.
    table = table.replace("-", " ")
    table["Reference Period Other Than Survey Period"] = table[
        "reference period other than survey period"
    ]  # .astype(str)

    # Drop unneeded columns.
    table = table.drop(
        ["question_group", "reference period other than survey period"], axis=1,
    )

    # Final ordering and rename wave link headers.
    final_table = pd.DataFrame()
    final_table["Variable"] = table["Variable"]

    for i in waves:
        final_table[
            ["Type", "Topic", "Reference Period Other Than Survey Period"]
        ] = table[["Type", "Topic", "Reference Period Other Than Survey Period"]]
        final_table[f"Links Wave {i}"] = table[f"group_w{i}"]
        if len(waves) == 1:
            final_table["Question Id"] = table[f"wave#{i}"]
        if routing:
            final_table[f"Routing"] = table[f"routing_wave_{i}"]
        final_table[f"Links Wave {i}"] = table[f"group_w{i}"]

    return final_table



def create_overview_page(topic_dict, wave, language, path):

    file_name = f"wave{wave}_questions_{language}_topics"
    target = f"{path}{file_name}.rst"
    if os.path.exists(target):
        os.remove(target)
    add_to_file(f".. _{file_name}:", target)
    add_to_file("\n", target)
    title = (
        f"Overview of Questions Wave {wave} ({language.capitalize()}) Grouped by Topic"
    )
    add_to_file(title, target)
    add_to_file("=" * len(title), target)
    add_to_file(
        "This page contains the questions grouped by topic. "
        "When clicking into a question, please note that internally the questions are "
        "ordered according to their appearance in the questionnaire. Clicking on "
        "the next or previous question will thus not preseve the grouping by topic.",
        target,
    )
    add_to_file("\n", target)

    for key in topic_dict.keys():
        add_to_file(key, target)
        add_to_file("-" * len(key), target)
        add_to_file("", target)
        add_to_file(".. toctree::", target)
        add_to_file("   :maxdepth: 1", target)
        add_to_file("", target)
        for question in topic_dict[key]:
            add_to_file(f"   {language}/{question}", target)
        add_to_file("\n", target)