How to create the documentation
--------------------------------

Creating the documentation involves a series of manual and (partially) automated tasks:

1. Add necessary folders:

- python/wave-x
- docs/source/wave-x
- docs/source/wave-x/_screenshots
- docs/source/wave-x/<language>


2. Create a codebook with all the questions and add it to the folder.

This is the most laborious part of adding a new wave, as it requires to create a new .csv file containing all questions and some additional information. There are some redunancies between this table and the renaming table though, so if the workflow is organized correctly you can save some time.

I usually add both english and dutch versions of the questions to the same codebook. I would suggest just looking at the old codebooks an corresponding documentation to see how the codebook translates into the website.

3. Setup the notebook `create-documentation.ipynb` to create .rst files for each question group. The notebook contains information on all the required steps. You need to select the appropriate column names and language in the files. Once everything is configured, you can run the notebook to create the files.

4. Take screenshots of all the questions using test links to the questionnaires. Add them to docs/source/wave-x/_screenshots. They need to be named in a specfifc way so the .rst files import them correctly (i.e. they contain a wave identifier and a question identifier).

5. Setup the notebook `create-variable-overview.ipynb` to create the variable overview. For this, you need to manually add the renaming table to the repo. It is not committed since it is continually updated for new waves and we don't want to save old versions here. The steps to create the variable overview tables are described in the notebook.

6. Create index files that are not created automatically in the previous steps. This includes:

- docs/source/wave-x/index.rst
- docs/source/wave-x/wavex_questions_<language>_ordered
