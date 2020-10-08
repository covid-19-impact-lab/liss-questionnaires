How to add a new wave to the documentation
-------------------------------------------

The source files for the documentation can be found in the `docs/` folder. It consists of restructuredtext-files and ist hosed using https://readthedocs.org/. The documentation consists of a collection of files that serve different purposes. The python scrips in this folder mainly serve to create the .rst-files for each question in the documentation and to create variable overview tables. Creating the documentation involves a series of manual and (partially) automated tasks.

1. Add necessary folders, this part is completely manual:

- `python/wave-x`
- `docs/source/wave-x`
- `docs/source/wave-x/_screenshots`
- `docs/source/wave-x/<language>`

2. Create a codebook with all the questions and add it to the folder. This part is completely manual.

This is the most laborious part of adding a new wave, as it requires to create a new .csv file containing all questions and some additional information. There are some redundancies between this table and the renaming table though, so if the workflow is organized nicely you can save some time.

Usually both english and dutch versions of the questions are added to the same codebook. Look at the codebooks from previous waves and corresponding documentation to see how the codebook translates into the website.

3. Setup the notebook `create-documentation.ipynb` to create .rst-files for each question group. The notebook contains information on all the required steps. You need to select the appropriate column names and language. Once everything is configured, you can run the notebook to create the files.

4. Take screenshots of all the questions using test links to the questionnaires. Add them to `docs/source/wave-x/_screenshots`. They need to be named in a specfifc way so the .rst files import them correctly (i.e. they contain a wave identifier and a question identifier). This part is completely manual.

5. Setup the notebook `create-variable-overview.ipynb` to create the variable overview. For this, you need to manually add the renaming table to the repo. It is not committed since it is often updated for new waves and we do not want to save old versions here. The steps to create the variable overview tables are described in the notebook.

6. Create index files that are not created automatically in the previous steps. This includes:

- `docs/source/wave-x/index.rst`
- `docs/source/wave-x/wavex_questions_<language>_ordered`

7. Make sure all files and paths are specified correctly so everything gets imported. I recommend building the documentation locally for to test everything out and check for errors using `make html` when you are in the docs folder ([more info](https://www.sphinx-doc.org/en/master/usage/quickstart.html)).

8. Add information about the wave to the main [README.md](https://github.com/covid-19-impact-lab/liss-questionnaires/blob/master/README.md) of the repository.
