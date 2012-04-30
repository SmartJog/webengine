man8_MANS = sjconf-webengine.man
DISTCLEANFILES = sjconf-webengine.man
EXTRA_DIST = sjconf-webengine.t2t

SUFFIXES = .t2t

.t2t.man:
	$(AM_V_GEN)$(TXT2TAGS) --quiet -o $@ $<

