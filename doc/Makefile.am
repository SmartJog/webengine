man1_MANS = \
	we_acluser.man \
	we_manageuser.man \
	we_adduser.man \
	we_deluser.man \
	we_listuser.man \
	we_chpasswd.man

SUFFIXES = .t2t

.t2t.man:
	$(TXT2TAGS) -o $@ $<

CLEANFILES = $(man1_MANS)
EXTRA_DIST = $(man1_MANS:.man=.t2t)
