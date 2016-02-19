webenginesysconf_DATA = webengine.conf webengine.ini
dist_webenginesysconf_DATA = webengine-conf.conf
EXTRA_DIST = webengine.conf.in webengine.ini.in

webengine.conf: $(top_srcdir)/etc/webengine.conf.in Makefile
	$(AM_V_GEN)$(SED) \
		-e 's|@webenginemediasdir[@]|$(pkgdatadir)/medias|g' \
		$< > $@

webengine.ini: $(top_srcdir)/etc/webengine.ini.in Makefile
	$(AM_V_GEN)$(SED) \
		-e 's|@webengineappdir[@]|$(webengineappdir)|g' \
		$< > $@

DISTCLEANFILES = webengine.conf webengine.ini
