dnl Process this file with autoconf to produce a configure script.
AC_INIT(webengine, 0.2.0)

dnl 2.52 is quite realistic
AC_PREREQ(2.52)

AM_INIT_AUTOMAKE([foreign])
AM_PATH_PYTHON

AC_SUBST([webenginesysconfdir], [\$\(sysconfdir\)/webengine])

AC_SUBST([webenginedir], [\$\(pkgdatadir\)/app/webengine])
AC_SUBST([exporterdir], [\$\(webenginedir\)/exporter])
AC_SUBST([utilsdir], [\$\(webenginedir\)/utils])
AC_SUBST([utilstagsdir], [\$\(utilsdir\)/templatetags])
AC_SUBST([templatesdir], [\$\(pkgdatadir\)/templates])

AC_CONFIG_FILES([Makefile \
                 exporter/Makefile \
                 etc/Makefile \
                 utils/Makefile \
                 utils/templatetags/Makefile \
                 templates/Makefile
                 ])
AC_OUTPUT
