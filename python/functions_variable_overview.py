import os
import pandas as pd
import numpy as np

from functions_questions import add_to_file


def create_description_table(
    table, waves, language, return_links_as_symbols=True, routing=True,
):
    """ Create variable overview from data description table of liss data."""
    out = table.copy()
    selected_waves = [f"wave#{i}" for i in waves]

    # Drop observations that are not included in selected waves.
    out.dropna(axis=0, how="all", subset=selected_waves, inplace=True)

    # Fill in nans as -.
    out = out.fillna("-")
    # Drop columns.
    out = out.drop(["label_english", "categories_english"], axis=1)
    out = out[out["question_group"] != "-"]
    out = out[out["Variable"] != "-"]

    # Drop waves that should not be included in table.
    wave_columns = out.columns[out.columns.str.contains("wave#")]
    drop_waves = set(wave_columns) - set(selected_waves)
    out.drop(drop_waves, axis=1, inplace=True)



    # Create question group id.
    for i in waves:
        out[f"group_w{i}"] = np.where(
            out[f"wave#{i}"] == "-", out[f"wave#{i}"], out["question_group"]
        )

    # create question link ":ref:`wNL-{question_group}`.
    for i in waves:
        if return_links_as_symbols:
            out[f"group_w{i}"] = out[f"group_w{i}"].apply(
                lambda x: f":ref:`🔗 <w{str(i)}{language}-{x}>`"
            )
        else:
            out[f"group_w{i}"] = out[f"group_w{i}"].apply(
                lambda x: f"w{str(i)}{language}-{x}"
            )
        out[f"group_w{i}"] = np.where(
            out[f"group_w{i}"].str.contains("--") == False, out[f"group_w{i}"], "-"
        )

    # Final formatting
    # Replace ordered categoricals to drop 'ordered' column.
    out["Type"] = np.where(
        out["ordered"] != True, out["Type"], "Ordered Categorical"
    )

    # Ensure correct formatting for reference period column,
    # create as new column to esnure it is last in table.
    out = out.replace("-", " ")
    out["Reference Period Other Than Survey Period"] = out[
        "reference period other than survey period"
    ]  # .astype(str)

    # Drop unneeded columns.
    out = out.drop(
        ["question_group", "reference period other than survey period"], axis=1,
    )

    # Final ordering and rename wave link headers.
    final_table = pd.DataFrame()
    final_table["Variable"] = out["Variable"]

    for i in waves:
        final_table[
            ["Type", "Topic", "Reference Period Other Than Survey Period"]
        ] = out[["Type", "Topic", "Reference Period Other Than Survey Period"]]
        final_table[f"Links Wave {i}"] = out[f"group_w{i}"]
        if len(waves) == 1:
            final_table["Question Id"] = out[f"wave#{i}"]
        if routing:
            final_table[f"Routing"] = out[f"routing_wave_{i}"]
        final_table[f"Links Wave {i}"] = out[f"group_w{i}"]

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
