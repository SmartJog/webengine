dnl Process this file with autoconf to produce a configure script.
AC_INIT(webengine, 0.1~dev)

dnl 2.52 is quite realistic
AC_PREREQ(2.52)

AM_INIT_AUTOMAKE([foreign])
AM_PATH_PYTHON

AC_PROG_SJCONF

AC_SUBST([webenginesysconfdir], [\$\(sysconfdir\)/webengine])

AC_SUBST([webenginedir], [\$\(pkgdatadir\)])
AC_SUBST([automationsdir], [\$\(webenginedir\)/automations])
AC_SUBST([exporterdir], [\$\(webenginedir\)/exporter])
AC_SUBST([importerdir], [\$\(webenginedir\)/importer])
AC_SUBST([rxtxdir], [\$\(webenginedir\)/rxtx])
AC_SUBST([telecommandedir], [\$\(webenginedir\)/telecommande])
AC_SUBST([utilsdir], [\$\(webenginedir\)/utils])
AC_SUBST([utilstagsdir], [\$\(utilsdir\)/templatetags])

AC_CONFIG_FILES([Makefile \
                 automations/Makefile \
                 automations/templates/Makefile \
                 exporter/Makefile \
                 importer/Makefile \
                 etc/Makefile \
                 rxtx/Makefile \
                 rxtx/templates/Makefile \
                 telecommande/Makefile \
                 telecommande/templates/Makefile \
                 utils/Makefile \
                 utils/templatetags/Makefile \
		 ])
AC_OUTPUT
