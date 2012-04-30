man1_MANS = \
	we_acluser.man \
	we_manageuser.man

SUFFIXES = .t2t

.t2t.man:
	$(AM_V_GEN)$(TXT2TAGS) --quiet -o $@ $<

CLEANFILES = $(man1_MANS)
EXTRA_DIST = $(man1_MANS:.man=.t2t)
