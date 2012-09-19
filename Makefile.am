SUBDIRS = exporter utils etc templates sjconf doc data
dist_webengineapp_PYTHON = __init__.py urls.py manage.py
nodist_webengineapp_PYTHON =  settings.py webengine.wsgi webengine.fcgi
dist_doc_DATA = README.rst

edit = $(SED) \
	-e 's|@webenginedir[@]|$(webenginedir)|g' \
	-e 's|@webengineappdir[@]|$(webengineappdir)|g' \
	-e 's|@webenginesysconfdir[@]|$(webenginesysconfdir)|g'

settings.py: settings.py.in Makefile
	$(AM_V_GEN)$(edit) $< > $@

webengine.fcgi: webengine.fcgi.in Makefile
	$(AM_V_GEN)$(edit) $< > $@

webengine.wsgi: webengine.wsgi.in Makefile
	$(AM_V_GEN)$(edit) $< > $@

dist_bin_SCRIPTS = \
	bin/we_acluser \
	bin/we_manageuser

CLEANFILES = $(nodist_webengineapp_PYTHON)
EXTRA_DIST = $(nodist_webengineapp_PYTHON:=.in)
