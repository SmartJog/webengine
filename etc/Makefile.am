dist_webenginesysconf_DATA = webengine.conf
EXTRA_DIST = webengine.conf.in

webengine.conf: $(top_srcdir)/etc/webengine.conf.in Makefile
	sed "s|@webenginedir[@]|${pkgdatadir}|;s|@datadir[@]|${prefix}/share|" $< > $@
