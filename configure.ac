AC_PREREQ([2.67])
AC_INIT([webengine],[0.15.5],[opensource@arkena.com])

AM_INIT_AUTOMAKE([foreign -Wall 1.11])
AM_SILENT_RULES([yes])

AM_PATH_PYTHON([2.5])

AC_PROG_SED
SJ_PROG_SJCONF
AC_PATH_PROG([TXT2TAGS], [txt2tags])
AS_IF([test "$TXT2TAGS" = ""], [AC_MSG_ERROR([Please install txt2tags.])])

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
