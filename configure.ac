dnl -*- Mode: autoconf -*-
dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.53)
AC_INIT([eos-app-store], [1.0.99], [http://www.endlessm.com])
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])
AC_CONFIG_SRCDIR(eos-app-store.in)
AC_CONFIG_HEADERS([config.h])
AM_INIT_AUTOMAKE([1.9 no-dist-gzip dist-xz foreign])

AM_PATH_PYTHON_VERSION(2.7, 2.7.0, 2.6, 2.6.0, 2.5, 2.5.0, 2.4, 2.4.0)

GOBJECT_INTROSPECTION_REQUIRE([0.9.6])

PKG_CHECK_MODULES(EOS_APP_STORE,
                  gio-2.0
                  gtk+-3.0
                  gobject-introspection-1.0)

AC_CONFIG_FILES([
        Makefile
        images/Makefile
        EosAppStore/Makefile
        EosAppStore/add_shortcuts_module/Makefile
        EosAppStore/application_store/Makefile
        EosAppStore/desktop/Makefile
        EosAppStore/desktop_files/Makefile
        EosAppStore/eos_log/Makefile
        EosAppStore/eos_util/Makefile
        EosAppStore/eos_widgets/Makefile
        EosAppStore/folder/Makefile
        EosAppStore/osapps/Makefile
        EosAppStore/removal_module/Makefile
        EosAppStore/shortcut/Makefile
        EosAppStore/util/Makefile
        ])

AC_OUTPUT
echo "
        eos-app-store $VERSION
        ===================

        prefix: ${prefix}

        Now type 'make' to build $PACKAGE
"