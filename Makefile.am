SUBDIRS = exporter utils etc templates sjconf doc data

dist_webengine_PYTHON = __init__.py urls.py webengine.fcgi
nodist_webengine_PYTHON =  settings.py

edit = $(SED) \
	-e 's|@webenginesysconfdir[@]|$(webenginesysconfdir)|g'

settings.py: settings.py.in Makefile
	$(edit) $< > $@

dist_bin_SCRIPTS = \
	bin/we_acluser \
	bin/we_adduser \
	bin/we_chpasswd \
	bin/we_deluser \
	bin/we_listuser \
	bin/we_manageuser

CLEANFILES = settings.py
EXTRA_DIST = settings.py.in
