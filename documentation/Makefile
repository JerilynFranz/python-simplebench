# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
HTML_BUILD_DIR = $(BUILDDIR)/html
HTML_PUBLISH_DIR = ../docs
RM = rm
RSYNC = rsync
MKDIR = mkdir

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean html

html: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(RSYNC) -a --delete --exclude=doctrees/ --exclude=.buildinfo "$(HTML_BUILD_DIR)/" "$(HTML_PUBLISH_DIR)/"

clean:
	# Clean the custom publish directory
	-@$(RM) -rf "$(HTML_PUBLISH_DIR)"
	-@$(MKDIR) -p "$(HTML_PUBLISH_DIR)"
	# Run the standard Sphinx clean for the build directory
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
