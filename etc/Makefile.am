webenginesysconf_DATA = webengine.conf
dist_webenginesysconf_DATA = webengine-conf.conf
EXTRA_DIST = webengine.conf.in

webengine.conf: $(top_srcdir)/etc/webengine.conf.in Makefile
	$(AM_V_GEN)$(SED) \
		-e 's|@webengineappdir[@]|$(webengineappdir)|g' \
		-e 's|@webenginemediasdir[@]|$(pkgdatadir)/medias|g' \
		$< > $@

DISTCLEANFILES = webengine.conf
