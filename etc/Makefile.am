dist_webenginesysconf_DATA = webengine.conf webengine-conf.conf
EXTRA_DIST = webengine.conf.in

webengine.conf: $(top_srcdir)/etc/webengine.conf.in Makefile
	$(SED) \
		-e 's|@webenginedir[@]|$(pkgdatadir)/app/webengine|' \
		-e 's|@webengineappdir[@]|$(pkgdatadir)/app|' \
		-e 's|@webenginemediasdir[@]|$(pkgdatadir)/medias|' \
		$< > $@

DISTCLEANFILES = webengine.conf
