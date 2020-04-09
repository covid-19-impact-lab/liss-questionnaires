""" Functions used in create-documentation notebook"""
import os
import pandas as pd
import numpy as np

button = ":raw-html:`&#10063;`"
csv_header ="\n{} ``{}``\n"
csv_entry = ".. csv-table::"
csv_columns = "   :header: {}{}\n"
csv_delim ="   :delim: |"
csv_row = "           {}|{}"
bool_entry = ":raw-html:`&#10063;` Yes :raw-html:`&#10063;` No – {} ``{}``\n"
open_question = "\n{}  .............. ``{}`` \n"
header_question = "\n{}\n"



def create_pages(codebook, q_ids, q_groups, q_layout, q_text, q_sub_text, q_categories, q_varname, target_dir):
    """ Create reStructuredText files for all groups specified in q_groups. Each file holds all questions that belong to a respective group.
    """
    
    qids = list(codebook[q_ids].unique())
    
    data = codebook.copy()
    data = data.set_index([codebook.index, q_ids])
    
    for idx, qid in enumerate(qids):
        
        df = data[data.index.get_level_values(q_ids) == qid]
        # Create rst-file.
        file_name = qid
        group_name = df.loc[df.index[0], q_groups]        
        path = target_dir + file_name +".rst"
        add_to_file(".. _"+ file_name +":", path) 
        add_to_file("\n \n .. role:: raw-html(raw) \n        :format: html \n", path)
        add_to_file(qid + " " + group_name + "\n"+ "="*len(qid + " " + group_name), path)
        
        if df[q_layout].all()== "open":
            for i in df.index:
                add_to_file(open_question.format(df.loc[i, q_text], df.loc[i, q_varname]),path)
        
        elif df[q_layout].all()== "multi":
            add_to_file(header_question.format(df.loc[df.index[0], q_text]), path)
            for i in df.index:
                add_to_file(bool_entry.format(df.loc[i, q_sub_text], df.loc[i, q_varname]), path)
        elif df[q_layout].all() in ["table","grid","cat"]:
            add_to_file(header_question.format(df.loc[df.index[0], q_text]), path)
            add_to_file(csv_entry.format(), path)
            add_to_file(csv_delim.format(), path)
            if df[q_layout].all() == "cat":
                add_to_file(csv_columns.format("",df.loc[df.index[0], q_categories]), path)
            else:
                add_to_file(csv_columns.format(",",df.loc[df.index[0], q_categories]), path)
            
            for i in df.index:
                if df.loc[i, q_layout] == "grid":
                    add_to_file(csv_row.format(df.loc[i, q_sub_text]," "), path)
                else:
                    items = df.loc[i, q_categories].count(',') 
                    add_to_file(csv_row.format(df.loc[i, q_sub_text],(button + "|")*(items) + button), path)
        else:
            raise ValueError("Page format in codebook is not correctly defined.")
                                
        if idx == 0:
            next_q = qids[idx+1]
            add_to_file("\n\n:ref:`"+ next_q + "` :raw-html:`&rarr;`", path)

        elif idx == (len(qids)-1):
            previous_q = qids[idx-1]
            add_to_file("\n\n:raw-html:`&larr;` :ref:`" + previous_q +"`", path)
        else:
            previous_q = qids[idx-1]
            next_q = qids[idx+1]
            add_to_file("\n\n:raw-html:`&larr;` :ref:`" + previous_q + "` | :ref:`" + next_q + "` :raw-html:`&rarr;`", path)



def add_to_file(msg, path):
    """ Adds line to file specified in path."""
    with open(path, "a") as f:
        f.write(msg + "\n")
        

def get_rst_names(name_list):
    """ Get list of group .rst-file names. """
    files =[]
    for name in name_list:
        file_name = name
        file_name = "".join(file_name.split())
        files.append(file_name)
        
    return files

        
def insert_question(df, idx, q_type, q_label, q_categories, q_varname, path):
    """ Inserts question based on question type using q_label as question title."""
    
    if df.loc[idx, q_type] == "Categorical":
        add_to_file(csv_header.format(df.loc[idx, q_label], df.loc[idx, q_varname]), path)
        add_to_file(csv_entry.format(), path)
        add_to_file(csv_columns.format(df.loc[idx, q_categories]), path)
        
        items = df.loc[idx, q_categories].count(',') 
        add_to_file(csv_row.format((button + ",")*(items) + button), path)

    elif df.loc[idx, q_type] == "bool":
        add_to_file(bool_entry.format(df.loc[idx, q_label], df.loc[idx, q_varname]), path)

    elif df.loc[idx, q_type] in ("int", "float", "str"):
        add_to_file(open_question.format(df.loc[idx, q_label], df.loc[idx, q_varname]),path)

    else:
        raise ValueError("Question type (q_type) must be in ['Categorical','bool', 'int', 'float', 'str']")
        
def create_topic_folders(codebook, q_topics, target_dir):
    
    topics_list = list(codebook[q_topics].unique())

    for topic in topics_list:
        path = target_dir + topic
        os.mkdir(path)
        
        
def create_group_file(codebook, q_topics, q_groups, q_type, q_label, q_categories, q_varname, target_dir, sort_topic=False):
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
        file_name = "".join(file_name.split())
        
        if sort_topic==True:
            path = target_dir + topic + "/" + file_name +".rst"
        else:
            path = target_dir + file_name +".rst"
            
        # Write header with anchor, group name and add role to use raw-html.                                             
        add_to_file(".. _"+ file_name +":", path) 
        add_to_file("\n \n .. role:: raw-html(raw) \n        :format: html \n", path)
        add_to_file(group + "\n"+ "="*len(group), path)
        
        # Insert questions.
        for i in df.index:
            insert_question(
                            df=df,
                            idx=i, 
                            q_type=q_type,
                            q_label=q_label,
                            q_categories=q_categories,
                            q_varname=q_varname, 
                            path=path
                           )

        # Insert link to previous and next group at the bottom of the page.
        if idx == 0:
            next_group = group_list[idx+1]
            next_group = "".join(next_group.split())
            add_to_file("\n\n:ref:`"+ next_group + "` :raw-html:`&rarr;`", path)

        elif idx == (len(group_list)-1):
            previous_group = group_list[idx-1]
            previous_group = "".join(previous_group.split())
            add_to_file("\n\n:raw-html:`&larr;` :ref:`" + previous_group +"`", path)
        else:
            previous_group = group_list[idx-1]
            previous_group = "".join(previous_group.split())

            next_group = group_list[idx+1]
            next_group = "".join(next_group.split())
            add_to_file("\n\n:raw-html:`&larr;` :ref:`" + previous_group +"` | :ref:`"+ next_group + "` :raw-html:`&rarr;`", path)
