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

python-toolbox2 builds like your typical autotools-based project::

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

Web Engine was created at SmartJog by :

* Anthony Mavic <anthony.mavic@smartjog.com>
* Bastien Abadie <bastien.abadie@smartjog.com>
* Benoit Mauduit <benoit.mauduit@smartjog.com>
* Bryann Lamour <bryann.lamour@smartjog.com>
* Clément Bœsch <clement.boesch@smartjog.com>
* Gilles Dartiguelongue <gilles.dartiguelongue@smartjog.com>
* Guillaume Camera <guillaume.camera@smartjog.com>
* Mathieu Dupuy <mathieu.dupuy@smartjog.com>
* Matthieu Bouron <matthieu.bouron@smartjog.com>
* Maxime Mouial <maxime.mouial@smartjog.com>
* Nicolas Noirbent <nicolas.noirbent@smartjog.com>
* Philippe Bridant <philippe.bridant@smartjog.com>
* Rémi Cardona <remi.cardona@smartjog.com>
* Stéphane Kanschine <stephane.kanschine@smartjog.com>
* Thomas Meson <thomas.meson@smartjog.com>
* Thomas Souvignet <thomas.souvignet@smartjog.com>
* Victor Goya <victor.goya@smartjog.com>

