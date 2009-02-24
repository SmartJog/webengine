dist_webenginesysconf_DATA = webengine.conf

webengine.conf: $(top_srcdir)/etc/webengine.conf.in Makefile
	sed "s|@sysconfdir[@]|${sysconfdir}|;s|@webenginesysconfdir[@]|${webenginesysconfdir}|" $< > $@
