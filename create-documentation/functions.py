""" Functions used in create-documentation notebook"""
import os
import pandas as pd
import numpy as np

button = ":raw-html:`&#10063;`"
csv_header ="\n{}\n"
csv_entry = "\n.. csv-table::"
csv_columns = "       {}"
csv_row = "\n            {}"  
bool_entry = ":raw-html:`&#10063;` Yes :raw-html:`&#10063;` No – {}\n"
open_question = "\n{}  .............. \n"


def add_to_file(msg, path):
    """ Adds line to file specified in path."""
    with open(path, "a") as f:
        f.write(msg + "\n")
        

def get_rst_names(name_list):
    """ Get list of group .rst-file names. """
    files =[]
    for name in name_list:
        file_name = name
        file_name = ''.join(file_name.split())
        files.append(file_name)
        
    return files

        
def insert_question(df, idx, q_type, q_label, q_categories, path):
    """ Inserts question based on question type using q_label as question title."""
    
    if df.loc[idx, q_type] == 'Categorical':
        add_to_file(csv_header.format(df.loc[idx, q_label]), path)
        add_to_file(csv_entry.format(), path)
        add_to_file(csv_columns.format(df.loc[idx, q_categories]), path)
        
        items = df.loc[idx, q_categories].count(",") 
        add_to_file(csv_row.format((button + ",")*(items) + button), path)

    elif df.loc[idx, q_type] == 'bool':
        add_to_file(bool_entry.format(df.loc[idx, q_label]), path)

    elif df.loc[idx, q_type] in ('int', 'float', 'str'):
        add_to_file(open_question.format(df.loc[idx, q_label]),path)

    else:
        raise ValueError("Question type (q_type) must be in ['Categorical','bool', 'int', 'float', 'str']")
        
def create_topic_folders(codebook, q_topics, target_dir):
    
    topics_list = list(codebook[q_topics].unique())

    for topic in topics_list:
        path = target_dir + topic
        os.mkdir(path)
        
        
def create_group_file(codebook, q_topics, q_groups, q_type, q_label, q_categories, target_dir):
    """ Create reStructuredText files for all groups specified in q_groups. Each file holds all questions that belong to a respective group.
    """
    
    group_list = list(codebook[q_groups].unique())
    
    data = codebook.copy()
    data = data.set_index([codebook.index, q_groups])
    
    for idx, group in enumerate(group_list):
        
        df = data[data.index.get_level_values(q_groups) == group]
        topic = list(df[q_topics].unique())[0]
        # Create rst-file.
        file_name = group
        file_name = ''.join(file_name.split())
        path = target_dir + topic + "/" + file_name +".rst"
 
        # Write header with anchor, group name and add role to use raw-html.                                             
        add_to_file(".. _"+ file_name +":", path) 
        add_to_file("\n \n .. role:: raw-html(raw) \n        :format: html \n", path)
        add_to_file(group + "\n"+ "="*len(group), path)
        
        # Insert questions.
        for i in df.index:
            insert_question(df=df,idx=i, q_type=q_type,q_label=q_label,q_categories=q_categories, path=path)

        # Insert link to previous and next group at the bottom of the page.
        if idx == 0:
            next_group = group_list[idx+1]
            next_group = ''.join(next_group.split())
            add_to_file("\n :ref:`"+ next_group + "` :raw-html:`&rarr;`", path)

        elif idx == (len(group_list)-1):
            previous_group = group_list[idx-1]
            previous_group = ''.join(previous_group.split())
            add_to_file("\n :raw-html:`&larr;` :ref:`" + previous_group +"`", path)
        else:
            previous_group = group_list[idx-1]
            previous_group = ''.join(previous_group.split())

            next_group = group_list[idx+1]
            next_group = ''.join(next_group.split())
            add_to_file("\n\n:raw-html:`&larr;` :ref:`" + previous_group +"` | :ref:`"+ next_group + "` :raw-html:`&rarr;`", path)
