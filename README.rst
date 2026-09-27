PureSkill.gg CS:GO Data Science Development Kit
===============================================

|PyPI| |GitHub Actions|

.. |PyPI| image:: https://img.shields.io/pypi/v/pureskillgg-csgo-dsdk.svg
   :target: https://pypi.python.org/pypi/pureskillgg-csgo-dsdk
   :alt: PyPI
.. |GitHub Actions| image:: https://github.com/pureskillgg/csgo-dsdk/workflows/main/badge.svg
   :target: https://github.com/pureskillgg/csgo-dsdk/actions
   :alt: GitHub Actions

Counter-Strike helpers for CSDS match data (a manifest plus one pandas
DataFrame per channel). ``scrub_csds_pii`` anonymizes a match before it leaves
the platform, and ``pop_overtime`` removes overtime rounds from a channel. It
works on data you have already loaded, usually with pureskillgg-dsdk_.

.. _pureskillgg-dsdk: https://pypi.python.org/pypi/pureskillgg-dsdk

Installation
------------

Requires Python 3.11 or later.

::

    $ uv add pureskillgg-csgo-dsdk

It does not install pureskillgg-dsdk. The example below loads the match with
it, so add it too::

    $ uv add pureskillgg-dsdk

Usage
-----

Scrub a match, then pop overtime:

.. code-block:: python

    from pureskillgg_dsdk import DsReaderS3, GameDsLoader
    from pureskillgg_csgo_dsdk import (
        csds_pii_channel_instructions,
        pop_overtime,
        scrub_csds_pii,
    )

    loader = GameDsLoader(
        reader=DsReaderS3(bucket="my-csds-bucket", manifest_key="path/to/match/csds")
    )

    # Load only the PII channels this CSDS has, then scrub them.
    data = loader.get_channels(csds_pii_channel_instructions(loader.manifest))
    manifest = scrub_csds_pii(loader.manifest, data)  # data is scrubbed in place

    # CS2 regulation is 24 rounds (MR12). The default, 30, is CS:GO MR15.
    deaths = loader.get_channel({"channel": "player_death"})
    overtime = pop_overtime(deaths, max_rounds_csgo=24)  # deaths keeps rounds 1-24

``scrub_csds_pii`` returns the new manifest. It replaces the job id with the
anonymous id, redacts names, clan tags, chat, share codes and demo ids, maps
each Steam id to a letter, zeroes pings, caps inflated win and commend counts,
and marks every changed column in the manifest. `docs/scrub-csds-pii.md
<docs/scrub-csds-pii.md>`_ lists every field.

``pop_overtime`` returns the removed rows with their original index labels.
Rows with a missing ``round`` stay. A channel without a ``round`` column raises
``MissingColumns``.

Exports
-------

.. list-table::
   :header-rows: 1

   * - Export
     - Used by
   * - ``scrub_csds_pii``, ``SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS``
     - csgo-ppp's scrubber
   * - ``csds_pii_channel_instructions``
     - no consumer yet; prefer it to the constant, which names channels an
       older CSDS may not have
   * - ``pop_overtime``
     - csgo-coach's economy course
   * - ``MissingColumns``, ``UnsupportedChannelStructure``
     - raised when a DataFrame lacks a required column

Development
-----------

You need Python 3, uv_ and `Git LFS`_ (the test fixtures are in LFS).

::

    $ git clone https://github.com/pureskillgg/csgo-dsdk.git
    $ cd csgo-dsdk
    $ git lfs install
    $ git lfs pull
    $ uv sync

The tasks are in the ``Makefile``: ``make lint``, ``make test``, ``make watch``
(tests on every change) and ``make format``.

.. _uv: https://docs.astral.sh/uv/
.. _Git LFS: https://git-lfs.com/

Publishing
~~~~~~~~~~

Set the new version with ``uv version <version>`` (or ``uv version --bump
patch``), then run ``make version``. It commits
``pyproject.toml`` and ``uv.lock`` and pushes a signed ``v*`` tag, which
triggers the publish workflow. Or run the `version workflow`_ by hand with a
version number or a bump (``patch``, ``minor``, ``major``); it does both steps.

Publishing needs the ``PYPI_API_TOKEN`` repository secret. The version and
format workflows also need ``GH_USER``, ``GH_TOKEN``, ``GIT_USER_NAME``,
``GIT_USER_EMAIL``, ``GPG_PRIVATE_KEY`` and ``GPG_PASSPHRASE``.

.. _version workflow: https://github.com/pureskillgg/csgo-dsdk/actions/workflows/version.yml

License
-------

MIT. See ``LICENSE.txt``.
