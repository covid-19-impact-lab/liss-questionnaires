# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

clean:
	rm -f covid-19impactlabquestionnaire.pdf

build:
	clean;
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

save_all_content_to_pdf:
	@$(SPHINXBUILD) -M latexpdf -interaction=nonstopmode . _build

capture_pdf:
	make serve & ( sleep 5 && make save_all_content_to_pdf ; echo "Captured PDF"; )

update_zenodo_deposit:
	build;
	capture_pdf;
	python3 $(shell pwd)/zenodo_release.py;


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	#@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	update_zenodo_deposit
