man1_MANS = \
	we_acluser.man \
	we_manageuser.man

SUFFIXES = .t2t

.t2t.man:
	txt2tags -o $@ $<

CLEANFILES = $(man1_MANS)
EXTRA_DIST = $(man1_MANS:.man=.t2t)
