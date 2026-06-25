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

``pureskillgg-csgo-dsdk`` is a small, CS:GO/CS2-specific data-science library,
layered on top of the generic `pureskillgg-dsdk`_ package, that provides utility
functions to clean up and anonymize **CSDS** ("Counter-Strike Data Standard")
match data before analysis or publication.

It is an importable toolkit, not a running service: there are no lambdas, no
``serverless.yml``, no Step Functions, no Terraform, and no CLI commands. It
ships zero deployed AWS infrastructure. The package is consumed by downstream
data-science and analytics repos that read parsed match data and need to strip
personally identifiable information (PII) or remove overtime rounds first.

.. _pureskillgg-dsdk: https://pypi.python.org/pypi/pureskillgg-dsdk

What it does
~~~~~~~~~~~~

The package (``pureskillgg_csgo_dsdk``) exposes exactly four public symbols from
its top-level ``__init__``:

- ``scrub_csds_pii`` - anonymize a CSDS match (manifest + per-channel
  DataFrames) in place.
- ``pop_overtime`` - remove rows for rounds past regular time from a channel
  DataFrame.
- ``SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS`` - a constant list of the CSDS channels
  a caller should load before scrubbing.
- ``MissingColumns`` / ``UnsupportedChannelStructure`` - exceptions raised when a
  DataFrame lacks a required column.

The **scrubber** (``scrubber/scrub_pii.py``) rewrites a CSDS match in place. In
the manifest it replaces ``jobId`` with the anonymous ``id`` everywhere (via a
``rapidjson`` dump / string-replace / load round-trip), redacts ``sharecode``,
``demoId`` and ``metadata.bucket``, and lowers ``matchDate`` precision to
minutes. In the channel DataFrames it redacts identifying columns (``sharecode``
and ``demo_id`` in ``header``; ``name_new`` / ``name_old`` in ``player_name``;
``name`` / ``clan_tag`` in ``player_personal``), maps each unique ``steam_id`` to
a letter (``A``, ``B``, ``C`` ...), zeroes ``ping`` in ``player_status``, and
caps inflated ``player_info`` stats (``wins`` over 2500 to 2501; each of
``commends_friendly`` / ``commends_leader`` / ``commends_teacher`` over 100 to
101). Every mutation also tags the corresponding manifest column ``origin`` with
``-redacted`` or ``-capped`` and flips that channel's ``redacted`` flag.

The **overtime filter** (``overtime/pop_overtime.py``) drops rows whose
``round`` exceeds ``max_rounds_csgo`` (default ``30``) from any channel DataFrame
that has a ``round`` column, mutating the input in place and returning the
removed overtime rows. It raises ``MissingColumns`` if there is no ``round``
column. There is no automatic short-match detection; a caller may pass
``max_rounds_csgo=16`` manually for short matches.

For a field-by-field breakdown of the scrubber's redact-vs-cap rules and its
manifest bookkeeping, see the deep dive linked under `Documentation`_.

Pipeline role
~~~~~~~~~~~~~

This is a downstream-consumed helper library, not a stage in the match
pipeline. It operates on CSDS channel data - the per-match DataFrames plus
manifest produced upstream by the demo replay / CSDS parsing stage
(``csgo-rushb`` / csds).

Data-science and analytics code imports it to anonymize match data before it
leaves the platform and to strip overtime rounds before modeling. Consumers
include ``csgo-datascience``, the coach / PPP / match-conversion pipeline
(``csgo-ppp``, ``csgo-coach``, ``csgo-progression``), and dataset-export /
Data-Exchange tooling. Any actual AWS I/O (reading the parsed match DataFrames
from S3) is performed by those consuming repos through ``pureskillgg-dsdk``
readers/loaders, not here.

Public API
~~~~~~~~~~

These are the confirmed exported symbols. They are the library's only "jobs";
this package owns no AWS resources, queues, tables, or log groups.

- ``scrub_csds_pii(manifest, data)`` - anonymize a CSDS match in place. Replaces
  ``jobId`` with the anonymous ``id`` throughout the manifest, redacts
  ``sharecode`` / ``demoId`` / ``metadata.bucket``, lowers ``matchDate`` to
  minute precision, redacts the identifying name/clan/sharecode/demo columns,
  maps ``steam_id`` values to letters, zeroes pings, caps inflated wins/commends,
  and flags every affected manifest channel/column as redacted or capped.
  Returns the (rewritten) manifest; the ``data`` dict is mutated in place.
- ``pop_overtime(df, *, max_rounds_csgo=30)`` - remove rows for rounds past
  regular time from a channel DataFrame (in place) and return the removed
  overtime rows. Raises ``MissingColumns`` if there is no ``round`` column.
- ``SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS`` - list of channel descriptors
  (``player_name``, ``header``, ``player_personal``, ``player_info``,
  ``player_status``) telling callers which CSDS channels to load before running
  ``scrub_csds_pii``.
- ``MissingColumns`` / ``UnsupportedChannelStructure`` - error types signaling a
  DataFrame lacks a required column. ``MissingColumns`` subclasses
  ``UnsupportedChannelStructure`` and carries the offending column names on its
  ``columns`` attribute.

Logs and observability
~~~~~~~~~~~~~~~~~~~~~~~

This is a pure Python library and owns **no** cloud resources, so there is
nothing to find in CloudWatch. It has no AWS-SDK calls, no DynamoDB / SQS / SNS /
S3 / Lambda / Step Functions usage, no DLQs, no Sentry integration, and no
``LOG_LEVEL`` handling. (The only ``bucket`` token in the code overwrites the
manifest's ``metadata.bucket`` field with the literal string ``redacted`` during
scrubbing - it is not a real S3 bucket reference.)

- **Runtime behavior:** failures surface only as raised Python exceptions
  (``MissingColumns`` / ``UnsupportedChannelStructure`` from this library, plus a
  ``RuntimeError`` if a manifest channel or column referenced during scrubbing is
  missing) propagated to whatever process imports the library. To find the logs
  for a real match run, look at the **consuming service** (for example
  ``csgo-datascience`` or the PPP/coach pipeline), not at this repo.
- **CI/CD:** the only observable surface owned by this repo is GitHub Actions
  (``main`` test, ``format``, ``publish`` to PyPI, ``version`` git-tag trigger).
  Failures show up as red GitHub Actions runs, not CloudWatch.

Documentation
~~~~~~~~~~~~~

- `docs/scrub-csds-pii.md <docs/scrub-csds-pii.md>`_ - deep dive on
  ``scrub_csds_pii``: the exact fields redacted vs. capped, the
  ``steam_id`` -> letter mapping, the ``jobId`` -> ``id`` manifest round-trip,
  and the manifest channel/column bookkeeping. This is the privacy-critical path
  for any data leaving the platform (for example Data Exchange / academic
  datasets), so the precise rules are worth knowing before relying on it.

Installation
------------

This package is registered on the `Python Package Index (PyPI)`_
as pureskillgg-csgo-dsdk_.

Install it with

::

    $ uv add pureskillgg-csgo-dsdk

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
    $ uv sync

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

You will need `Python 3`_ and uv_.

Install the development dependencies with

::

    $ uv sync

.. _uv: https://docs.astral.sh/uv/
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

Use the `uv version`_ command to release a new version.
Then run `make version` to commit and push a new git tag
which will trigger a GitHub action.

Publishing may be triggered using on the web
using a `workflow_dispatch on GitHub Actions`_.

.. _uv version: https://docs.astral.sh/uv/reference/cli/#uv-version
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
