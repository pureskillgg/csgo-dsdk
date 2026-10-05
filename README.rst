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
the platform, ``pop_overtime`` removes overtime rounds from a channel, and
``add_player_vector_derived_columns`` computes ``player_vector``'s velocities
and movement angles. It works on data you have already loaded, usually with
pureskillgg-dsdk_.

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

Derived player_vector columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ten ``player_vector`` columns are computed from the columns read from the
demo: ``second``, ``x_vel``, ``y_vel``, ``z_vel``, ``speed_2d``,
``movement_angle``, ``movement_angle_diff``, ``phi_vel``, ``theta_vel`` and
``ang_vel``. Compute them after loading:

.. code-block:: python

    from pureskillgg_csgo_dsdk import (
        add_player_vector_derived_columns,
        player_vector_source_columns,
    )

    # Everything, on a whole player_vector.
    player_vector = loader.get_channel({"channel": "player_vector"})
    add_player_vector_derived_columns(player_vector)  # added in place

    # Or load only what two of them need.
    wanted = ["speed_2d", "z_vel"]
    player_vector = loader.get_channel(
        {"channel": "player_vector", "columns": player_vector_source_columns(wanted)}
    )
    add_player_vector_derived_columns(player_vector, columns=wanted)

The values are the ones csgo-ppp writes:

- Velocities are differenced per player per round, so each player's first
  sample in a round reads 0. A sample where any axis moved faster than 3,500
  units a second (the engine's cap) is a teleport and reads 0 too.
- ``movement_angle`` is the direction of movement, 0 to 360.
  ``movement_angle_diff`` is where the player looks minus where they move,
  -180 to 180. Both are missing when the player stands still.
- ``second`` is ``tick`` over the tick rate: 64 in CS2. Pass ``tick_rate``
  for a CS:GO match; it is in the match's header.

A derived column the frame already has is replaced, never read, so a file that
stores them comes out the same as one that doesn't. Rows must be in tick order
within each player and round, as csgo-ppp writes them. For a frame holding
more than one match, such as a tome, pass
``group_by=["match_key", "player_id", "round"]``. A frame that lacks a column
they are computed from raises ``MissingColumns``.

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
   * - ``add_player_vector_derived_columns``, ``player_vector_source_columns``,
       ``PLAYER_VECTOR_DERIVED_COLUMNS``
     - readers of ``player_vector`` that need its velocities, movement angles
       or ``second``
   * - ``pureskillgg_csgo_dsdk.player_vector``'s ``calc_*`` functions
     - csgo-ppp's converter, which computes the same columns step by step
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
