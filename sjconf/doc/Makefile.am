man8_MANS = sjconf-webengine.man
DISTCLEANFILES = sjconf-webengine.man
EXTRA_DIST = sjconf-webengine.t2t

SUFFIXES = .t2t

.t2t.man:
	txt2tags -o $@ $<

