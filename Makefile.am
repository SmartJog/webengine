ACLOCAL_AMFLAGS = -I /usr/share/sjconf/autotools

SUBDIRS = exporter utils etc templates sjconf doc
dist_webengine_PYTHON = __init__.py urls.py
nodist_webengine_PYTHON =  settings.py

edit = sed \
	-e 's|@webenginesysconfdir[@]|$(webenginesysconfdir)|g'

settings.py: settings.py.in Makefile
	$(edit) $< > $@

dist_bin_SCRIPTS = bin/we_acluser bin/we_adduser bin/we_deluser bin/we_listuser bin/we_manageuser

CLEANFILES = settings.py
EXTRA_DIST = settings.py.in
