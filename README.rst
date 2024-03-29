PureSkill.gg CS:GO Data Science Development Kit
===============================================

|PyPI| |GitHub Actions|

.. |PyPI| image:: https://img.shields.io/pypi/v/pureskillgg-csgo-dsdk.svg
   :target: https://pypi.python.org/pypi/pureskillgg-csgo-dsdk
   :alt: PyPI
.. |GitHub Actions| image:: https://github.com/pureskillgg/csgo-dsdk/workflows/main/badge.svg
   :target: https://github.com/pureskillgg/csgo-dsdk/actions
   :alt: GitHub Actions

Python Data Science Development Kit for CS:GO.

Description
-----------

Do data science with CS:GO.

Installation
------------

This package is registered on the `Python Package Index (PyPI)`_
as pureskillgg-csgo-dsdk_.

Install it with

::

    $ poetry add pureskillgg-csgo-dsdk

.. _pureskillgg-csgo-dsdk: https://pypi.python.org/pypi/pureskillgg-csgo-dsdk
.. _Python Package Index (PyPI): https://pypi.python.org/

Development and Testing
-----------------------

Quickstart
~~~~~~~~~~

::

    $ git clone https://github.com/pureskillgg/csgo-dsdk.git
    $ git lfs install
    $ git lfs pull
    $ cd csgo-dsdk
    $ poetry install

Run each command below in a separate terminal window:

::

    $ make watch

Primary development tasks are defined in the `Makefile`.

Source Code
~~~~~~~~~~~

The `source code`_ is hosted on GitHub.
Clone the project with

::

    $ git clone https://github.com/pureskillgg/csgo-dsdk.git
    $ git lfs install
    $ git lfs pull

.. _source code: https://github.com/pureskillgg/csgo-dsdk

Requirements
~~~~~~~~~~~~

You will need `Python 3`_ and Poetry_.

Install the development dependencies with

::

    $ poetry install

.. _Poetry: https://poetry.eustace.io/
.. _Python 3: https://www.python.org/

Tests
~~~~~

Lint code with

::

    $ make lint


Run tests with

::

    $ make test

Run tests on changes with

::

    $ make watch

Publishing
~~~~~~~~~~

Use the `poetry version`_ command to release a new version.
Then run `make version` to commit and push a new git tag
which will trigger a GitHub action.

Publishing may be triggered using on the web
using a `workflow_dispatch on GitHub Actions`_.

.. _Poetry version: https://python-poetry.org/docs/cli/#version
.. _workflow_dispatch on GitHub Actions: https://github.com/pureskillgg/csgo-dsdk/actions?query=workflow%3Aversion

GitHub Actions
--------------

*GitHub Actions should already be configured: this section is for reference only.*

The following repository secrets must be set on GitHub Actions.

- ``PYPI_API_TOKEN``: API token for publishing on PyPI.

These must be set manually.

Secrets for Optional GitHub Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The version and format GitHub actions
require a user with write access to the repository
including access to read and write packages.
Set these additional secrets to enable the action:

- ``GH_USER``: The GitHub user's username.
- ``GH_TOKEN``: A personal access token for the user.
- ``GIT_USER_NAME``: The name to set for Git commits.
- ``GIT_USER_EMAIL``: The email to set for Git commits.
- ``GPG_PRIVATE_KEY``: The `GPG private key`_.
- ``GPG_PASSPHRASE``: The GPG key passphrase.

.. _GPG private key: https://github.com/marketplace/actions/import-gpg#prerequisites

Contributing
------------

Please submit and comment on bug reports and feature requests.

To submit a patch:

1. Fork it (https://github.com/pureskillgg/csgo-dsdk/fork).
2. Create your feature branch (`git checkout -b my-new-feature`).
3. Make changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin my-new-feature`).
6. Create a new Pull Request.

License
-------

This Python package is licensed under the MIT license.

Warranty
--------

This software is provided by the copyright holders and contributors "as is" and
any express or implied warranties, including, but not limited to, the implied
warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall the copyright holder or contributors be liable for
any direct, indirect, incidental, special, exemplary, or consequential damages
(including, but not limited to, procurement of substitute goods or services;
loss of use, data, or profits; or business interruption) however caused and on
any theory of liability, whether in contract, strict liability, or tort
(including negligence or otherwise) arising in any way out of the use of this
software, even if advised of the possibility of such damage.
