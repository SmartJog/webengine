===============
webengine
===============

The first goal of the Web Engine is to gather the several differents websites
that are in use for SmartJog and TV-Radio.

It aims to be able to run both SJ and TVR “applications” using the same code
base, changing display based on profiles and configuration.

The webengine is composed of 2 main parts:

    * A base, as tiny as possible, just a base to develop plugins on.
    * Plugins, where the biggest part is.

Web Engine is based on Django (a python framework for web development).

License
======

Web Engine is released under the `GNU LGPL 2.1 <http://www.gnu.org/licenses/lgpl-2.1.html>`_.


Build and installation
=======================

Bootstrapping
-------------

Web Engine uses the autotools for its build system.

If you checked out code from the git repository, you will need
autoconf and automake to generate the configure script and Makefiles.

To generate them, simply run::

    $ autoreconf -fvi

Building
--------

Web Engine builds like your typical autotools-based project::

    $ ./configure && make && make install


Development
===========

We use `semantic versioning <http://semver.org/>`_ for
versioning. When working on a development release, we append ``~dev``
to the current version to distinguish released versions from
development ones. This has the advantage of working well with Debian's
version scheme, where ``~`` is considered smaller than everything (so
version 1.10.0 is more up to date than 1.10.0~dev).


Authors
======

Web Engine was created at SmartJog by:

* Anthony Mavic
* Bastien Abadie
* Benoit Mauduit
* Bryann Lamour
* Clément Bœsch
* Gilles Dartiguelongue
* Guillaume Camera
* Mathieu Dupuy
* Matthieu Bouron
* Maxime Mouial
* Nicolas Delvaux <nicolas.delvaux@cji.paris>
* Nicolas Noirbent
* Philippe Bridant
* Rémi Cardona
* Stéphane Kanschine
* Thomas Meson
* Thomas Souvignet
* Victor Goya


