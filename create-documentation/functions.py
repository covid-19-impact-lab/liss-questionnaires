""" Functions used in create-documentation notebook"""


button = ":raw-html:`&#10063;`"
csv_header="\n*{}*\n"
csv_entry = "\n.. csv-table:: \n"
csv_columns = "\n       {}"
csv_row ="\n            {}"  
bool_entry=":raw-html:`&#10063;` Yes :raw-html:`&#10063;` No – *{}*\n"
open_question="\n*{}*  .............. \n"


def add_to_file(msg, path):
    with open(path, "a") as f:
        f.write(msg + "\n")
        

def get_rst_names(name_list):
    """ Get list of group .rst-file names. """
    files =[]
    for group in name_list:
        file_name=group
        file_name = ''.join(file_name.split())
        files.append(file_name)
        
    return files

        
def insert_question(df, idx, q_type, q_label, q_categories, path):
    """ Inserts question based on question type using q_label als question title."""
    
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
        
        
        
def create_group_file(codebook, q_groups, q_type, q_label, q_categories, target_dir):
    
    group_list = list(codebook[q_groups].unique())
    
    data = codebook.copy()
    data = data.set_index([codebook.index, q_groups])
    
    for idx, group in enumerate(group_list):
        
        df = data[data.index.get_level_values(q_groups) == group]
        
        # Create rst-file.
        file_name = group
        file_name = ''.join(file_name.split())
        
        path = target_dir + file_name +".rst"
        
        # Write header with anchor, group name and some other utilities.                                             
        add_to_file(".. _"+ file_name +":", path) 
        add_to_file("\n \n .. role:: raw-html(raw) \n        :format: html \n", path)
        add_to_file(group + "\n"+ "="*len(group), path)
        
        # Insert questions.
        for i in df.index:
            insert_question(df=df,idx=i, q_type=q_type,q_label=q_label,q_categories=q_categories, path=path)

        # Insert link to previous and next group in documentation.
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

            
### NEEDS TO BE UPDATED ---------------------------------------------------------------------------------------
def create_topic_file(codebook, q_topics, q_groups, q_type):
    
    topic_list = list(codebook[q_topics].unique())
    
    data = codebook.copy()
    data = data.set_index([codebook.index, q_topics, q_groups])
    
    for idx, topic in enumerate(topic_list):
        
        topic_df = data[data.index.get_level_values(q_topics) == topic]
        
        # Create rst-file.
        file_name = topic
        file_name = ''.join(file_name.split())
        f= open(target_dir + file_name +".rst", "w+")
        
        # Write header with anchor, group name and some other utilities.
        f.write(".. _"+ file_name +":")
        f.write("\n \n .. role:: raw-html(raw) \n        :format: html \n \n")
        f.write(topic + "\n"+ "="*len(topic)+"\n\n")
        
        group_list = list(topic_df.index.get_level_values(q_groups).unique())
        for group in group_list:
            
            # Take slice of dataframe for each group.
            df = topic_df[topic_df.index.get_level_values(q_groups) == group]
            f.write("\n" + group + "\n"+ "-"*len(group) +"\n\n")
            # Insert questions.
            for i in df.index:
                insert_question(df=df,idx=i, q_type=q_type,q_label=q_label, path=path)

        # Insert link to previous and next topic in documentation.
        if idx == 0:
            next_topic = topic_list[idx+1]
            next_topic = ''.join(next_topic.split())
            f.write("\n :ref:`"+ next_topic + "` :raw-html:`&rarr;`")

        elif idx == (len(topic_list)-1):
            previous_topic = topic_list[idx-1]
            previous_topic = ''.join(previous_topic.split())
            f.write("\n :raw-html:`&larr;` :ref:`" + previous_topic +"`")
        else:
            previous_topic = topic_list[idx-1]
            previous_topic = ''.join(previous_topic.split())

            next_topic = topic_list[idx+1]
            next_topic = ''.join(next_topic.split())
            f.write("\n\n :raw-html:`&larr;` :ref:`" + previous_topic +"` | :ref:`"+ next_topic + "` :raw-html:`&rarr;`")
        
        f.close()