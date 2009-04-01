dnl Process this file with autoconf to produce a configure script.
AC_INIT(webengine, 0.1.1~dev)

dnl 2.52 is quite realistic
AC_PREREQ(2.52)

AM_INIT_AUTOMAKE([foreign])
AM_PATH_PYTHON

#AC_PROG_SJCONF

AC_SUBST([webenginesysconfdir], [\$\(sysconfdir\)/webengine])

AC_SUBST([webenginedir], [\$\(pkgdatadir\)/app/webengine])
AC_SUBST([exporterdir], [\$\(webenginedir\)/exporter])
AC_SUBST([importerdir], [\$\(webenginedir\)/importer])
AC_SUBST([utilsdir], [\$\(webenginedir\)/utils])
AC_SUBST([utilstagsdir], [\$\(utilsdir\)/templatetags])

AC_CONFIG_FILES([Makefile \
                 exporter/Makefile \
                 importer/Makefile \
                 etc/Makefile \
                 utils/Makefile \
                 utils/templatetags/Makefile \
		 ])
AC_OUTPUT
