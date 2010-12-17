dnl Process this file with autoconf to produce a configure script.
AC_INIT(webengine, 0.12.0~dev)

dnl 2.52 is quite realistic
AC_PREREQ(2.52)

AM_INIT_AUTOMAKE([foreign])
AM_PATH_PYTHON

AC_PROG_SED
AC_PROG_SJCONF
AC_PATH_PROG(TXT2TAGS, txt2tags)

AC_SUBST([webenginesysconfdir], [\$\(sysconfdir\)/webengine])

AC_SUBST([webenginedir], [\$\(pkgdatadir\)])
AC_SUBST([webengineappdir], [\$\(pkgdatadir\)/app/webengine])
AC_SUBST([exporterdir], [\$\(webengineappdir\)/exporter])
AC_SUBST([utilsdir], [\$\(webengineappdir\)/utils])
AC_SUBST([utilstagsdir], [\$\(utilsdir\)/templatetags])
AC_SUBST([templatesdir], [\$\(pkgdatadir\)/templates])

AC_CONFIG_FILES([Makefile \
                 exporter/Makefile \
                 data/Makefile \
                 doc/Makefile \
                 etc/Makefile \
                 utils/Makefile \
                 utils/templatetags/Makefile \
                 templates/Makefile \
                 sjconf/Makefile \
                 sjconf/plugins/webengine.py \
                 sjconf/templates/Makefile \
                 sjconf/templates/webengine/Makefile \
                 sjconf/confs/Makefile \
                 sjconf/doc/Makefile
                 ])
AC_OUTPUT
