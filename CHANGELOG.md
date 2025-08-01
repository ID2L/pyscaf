# CHANGELOG


## v1.2.1 (2025-07-31)

### Bug Fixes

- **dependencies**: Add PyYAML 6.0.2 to project dev dependencies
  ([`a7f3178`](https://github.com/ID2L/pyscaf/commit/a7f3178332133b8790aac2eaf41ea770fea093cd))

### Chores

- **ci/cd**: Test workflow
  ([`027f33e`](https://github.com/ID2L/pyscaf/commit/027f33ee93f0bf300d06e31be979d3cde1abcdb9))

- **ci/cd**: Workflow passes locally
  ([`2320b24`](https://github.com/ID2L/pyscaf/commit/2320b2496df379826826a5b4503eb60e5b7b9143))


## v1.2.0 (2025-07-31)

### Bug Fixes

- **cli**: Handle boolean options with True default value
  ([`6aba861`](https://github.com/ID2L/pyscaf/commit/6aba8610782648e153094d47f39018c77d9ee802))

- **cli**: Proper handling of interactive/non-interactive mod with choices cli options
  ([`3728004`](https://github.com/ID2L/pyscaf/commit/372800423a1b1035ae5b45ae0bd9719893e34e4d))

- **cli**: Uniformize handle boolean options for consitency
  ([`86164ec`](https://github.com/ID2L/pyscaf/commit/86164ec6069a707d23db264a4294494c8c88467f))

### Features

- **test**: Pytest compatible way of declaring dynamic testing
  ([`1c67389`](https://github.com/ID2L/pyscaf/commit/1c67389502bbffcaa660454c6706b4e03f5a2b85))

### Testing

- **actions**: Basic tests for actions
  ([`99ef790`](https://github.com/ID2L/pyscaf/commit/99ef790c8506e9178cfdb4969689d152a7ca814d))

- **actions**: Dynamics integration tests for actions
  ([`de8e0d5`](https://github.com/ID2L/pyscaf/commit/de8e0d5a7c2c7dc0306a91695880530aaffc3764))

- **actions**: Handle boolean value
  ([`6e20981`](https://github.com/ID2L/pyscaf/commit/6e2098173d71476964d1c62ad22c700d5e0a69be))

- **actions**: Updated dynamic testing and a bunch of tests
  ([`505d224`](https://github.com/ID2L/pyscaf/commit/505d224b70c1254f86c32a429f214cd815d5a499))


## v1.1.2 (2025-07-29)

### Bug Fixes

- **cli**: Gracefully handle default value in non-interactive mod
  ([`01aa9c0`](https://github.com/ID2L/pyscaf/commit/01aa9c04266868130f78b92536c7d4be6c66e31f))


## v1.1.1 (2025-07-29)

### Bug Fixes

- First draw for the better choices cli options
  ([`40b56f0`](https://github.com/ID2L/pyscaf/commit/40b56f09bcbb7ba419a3fba669460c6c49a82c47))

Doesn't display well the default value for action documentation

- **cliOption**: Properly handle default option display
  ([`b86c59d`](https://github.com/ID2L/pyscaf/commit/b86c59dc8ad716a150460001e3ad80b0670a6195))


## v1.1.0 (2025-07-28)

### Features

- **documentation**: Added readme
  ([`166616b`](https://github.com/ID2L/pyscaf/commit/166616b255d1a66d8b60ac626164fe0cd6e9af9e))


## v1.0.0 (2025-07-28)

### Bug Fixes

- Deploy release
  ([`9ce4f25`](https://github.com/ID2L/pyscaf/commit/9ce4f251fea18e731ba35177fdccca0a71e6b52f))

BREAKING CHANGE: scaffolded scripts pathes has change

- **readme**: Removed deprecated info
  ([`a9aed8c`](https://github.com/ID2L/pyscaf/commit/a9aed8c9f823c0f50eb133820a3941cce61236e3))


## v0.11.0 (2025-07-21)

### Features

- Jupyter-tool action for jupyter ease of use
  ([`6a87020`](https://github.com/ID2L/pyscaf/commit/6a870203bb6e196f568cae22be0965c1a90db0b2))


## v0.10.4 (2025-06-06)

### Bug Fixes

- Use the new preference_chain in the cli
  ([`16218d8`](https://github.com/ID2L/pyscaf/commit/16218d8f003f8e276ba517d8d28c6045d6917fe2))


## v0.10.3 (2025-06-02)

### Bug Fixes

- Ci/cd for release on Pypitest
  ([`d829b38`](https://github.com/ID2L/pyscaf/commit/d829b3868c59f109b6a62d731f7b1b9a341640a6))

### Chores

- Change name to publish on pypi
  ([`ece0f02`](https://github.com/ID2L/pyscaf/commit/ece0f02324aa697e0ed953eb16a3dd89201ca1d8))


## v0.10.2 (2025-06-02)


## v0.10.1 (2025-06-02)

### Bug Fixes

- Manual deployment to pypi
  ([`87c7337`](https://github.com/ID2L/pyscaf/commit/87c7337fdfc4edcf4f16ffb474ddeed811389ae0))

- Old release job
  ([`89ee1ab`](https://github.com/ID2L/pyscaf/commit/89ee1ab187207db5a75ce9739469cb4d4e90038e))

### Chores

- Implements a Github flow
  ([`a12f5a7`](https://github.com/ID2L/pyscaf/commit/a12f5a77e07627a203f335d9775adf610da0b6bb))

Développement : Feature branches → PR → main Test automatique : Push main → v1.2.3 sur PyPI Test
  Production manuelle : Action "Deploy v1.2.3 to Production"


## v0.10.1-rc.1 (2025-06-02)

### Bug Fixes

- Add permissions for deployment workflows
  ([`23ddbf9`](https://github.com/ID2L/pyscaf/commit/23ddbf978936fb96a5ffa9e2766535833037d4bc))

This commit enhances the `deploy-production.yml` and `deploy-test.yml` workflow files by adding
  necessary permissions for the deployment jobs. The changes include:

- Introduction of `permissions` settings to allow write access for `contents` and `id-token`, which
  are essential for the deployment processes. - Ensuring that the workflows can effectively manage
  the required resources during deployment to both Production and Test PyPI.

These modifications aim to improve the functionality and security of the deployment workflows,
  facilitating smoother operations within the GitHub Actions environment.

- Add permissions for deployment workflows ([#4](https://github.com/ID2L/pyscaf/pull/4),
  [`e2c006e`](https://github.com/ID2L/pyscaf/commit/e2c006e52ecaa92c68552dbad103aa003aa1b145))

This commit enhances the `deploy-production.yml` and `deploy-test.yml` workflow files by adding
  necessary permissions for the deployment jobs. The changes include:

- Introduction of `permissions` settings to allow write access for `contents` and `id-token`, which
  are essential for the deployment processes. - Ensuring that the workflows can effectively manage
  the required resources during deployment to both Production and Test PyPI.

These modifications aim to improve the functionality and security of the deployment workflows,
  facilitating smoother operations within the GitHub Actions environment.

* 0.10.1-rc.1

Automatically generated by python-semantic-release

- Remove GITHUB_TOKEN from reusable-deploy.yml
  ([`1f88d3f`](https://github.com/ID2L/pyscaf/commit/1f88d3fe0c5a5ae67efaf42f49b0b6fe01c5a804))

This commit updates the `reusable-deploy.yml` workflow file by removing the `GITHUB_TOKEN` secret
  requirement. The change aims to simplify the deployment process by eliminating unnecessary token
  requirements, thereby enhancing security and reducing potential configuration issues.

Key changes include: - Deletion of the `GITHUB_TOKEN` entry from the secrets section, which was
  previously marked as required for the deployment workflow.

These modifications contribute to a more streamlined and secure deployment configuration within the
  GitHub Actions workflows.

- Remove GITHUB_TOKEN from reusable-deploy.yml ([#4](https://github.com/ID2L/pyscaf/pull/4),
  [`e2c006e`](https://github.com/ID2L/pyscaf/commit/e2c006e52ecaa92c68552dbad103aa003aa1b145))

This commit updates the `reusable-deploy.yml` workflow file by removing the `GITHUB_TOKEN` secret
  requirement. The change aims to simplify the deployment process by eliminating unnecessary token
  requirements, thereby enhancing security and reducing potential configuration issues.

Key changes include: - Deletion of the `GITHUB_TOKEN` entry from the secrets section, which was
  previously marked as required for the deployment workflow.

These modifications contribute to a more streamlined and secure deployment configuration within the
  GitHub Actions workflows.

### Chores

- Implements a Github flow ([#4](https://github.com/ID2L/pyscaf/pull/4),
  [`e2c006e`](https://github.com/ID2L/pyscaf/commit/e2c006e52ecaa92c68552dbad103aa003aa1b145))

Développement : Feature branches → PR → main Test automatique : Push main → v1.2.3 sur PyPI Test
  Production manuelle : Action "Deploy v1.2.3 to Production"

---------

Co-authored-by: semantic-release <semantic-release>


## v0.10.0 (2025-06-02)

### Chores

- Remove pytest configuration and add GitHub workflows for deployment
  ([`71818dc`](https://github.com/ID2L/pyscaf/commit/71818dc5a02a4ebe12318e197c58700b09372a62))

This commit removes the `pytest.ini` configuration file, which was previously used for setting up
  pytest testing parameters. In its place, new GitHub workflows have been introduced to automate
  deployment processes to both TestPyPI and Production PyPI. Key changes include:

- Deletion of the `pytest.ini` file, eliminating the previous testing configuration. - Addition of
  `deploy-production.yml` for deploying to Production PyPI upon pushes to the `main` branch. -
  Addition of `deploy-test.yml` for deploying to TestPyPI upon pushes to the `develop` branch. -
  Creation of `README.md` in the workflows directory to document the new workflow structure and
  required secrets for deployment. - Introduction of `reusable-deploy.yml` to encapsulate common
  deployment logic, enhancing maintainability and clarity.

These changes aim to streamline the deployment process and improve the overall project structure by
  leveraging GitHub Actions for automated workflows.

- Update configuration for ruff and pytest
  ([`997a84d`](https://github.com/ID2L/pyscaf/commit/997a84d9750f8198ae1df6d98f2fe5ee4a3214af))

This commit enhances the configuration for the `ruff` linter and `pytest` testing framework in the
  `pyproject.toml` and `.vscode/settings.json` files.

Key changes include: - Exclusion of template files from linting in the `ruff` configuration to avoid
  unnecessary warnings. - Updated `pytest` options to include strict markers and configuration
  checks, as well as enabling colored output for better readability. - Addition of new markers for
  categorizing tests, including `slow`, `integration`, and `unit`.

These adjustments aim to improve the development workflow and maintain code quality standards across
  the project.

### Features

- Integrate pytest testing action and update dependencies
  ([`150be5d`](https://github.com/ID2L/pyscaf/commit/150be5d94f1c09584533625e840bd94ee1ea52ac))

This commit introduces a new `TestAction` class to initialize a project with the pytest testing
  framework, enhancing the testing capabilities of the project. Key changes include:

- Addition of a new `src/pyscaf/actions/test/__init__.py` file containing the `TestAction` class,
  which manages the setup and configuration of pytest. - Creation of a `config.toml` file for pytest
  configuration, specifying test paths, file patterns, and markers. - Inclusion of a `README.md`
  file detailing the pytest integration, features, and best practices for writing tests. - A
  template for test examples is provided in `template_test_example.py`, demonstrating basic test
  structure and usage of fixtures. - Updates to existing `GitAction` and `JupyterAction` classes to
  change their dependencies from `poetry` to `core`, ensuring consistency across actions.

These enhancements aim to streamline the testing process and improve code quality through better
  test organization and documentation.


## v0.9.0 (2025-06-02)

### Code Style

- Minor writting fix
  ([`bd61236`](https://github.com/ID2L/pyscaf/commit/bd61236d83bd83d2c8d97803dc5ae549d9dce738))

### Features

- Renamed PoetryAction to CoreAction & added ruff to it
  ([`0bdb60e`](https://github.com/ID2L/pyscaf/commit/0bdb60ece6ec8aeda8372e5ba8eefecc4e74f263))


## v0.8.0 (2025-05-27)

### Features

- Add ruff as a development dependency
  ([`5c05049`](https://github.com/ID2L/pyscaf/commit/5c0504941ce1723a10701bd2e602c1943f7b1f86))

This commit introduces the `ruff` package (version 0.11.11) as a new development dependency in the
  `pyproject.toml` file. Ruff is an extremely fast Python linter and code formatter, enhancing the
  code quality and consistency of the project. Additionally, the `poetry.lock` file has been updated
  to reflect this new dependency, including all relevant wheel files and their hashes.

Minor formatting adjustments were also made across various files to ensure consistency and
  readability, including the addition of newlines and the reformatting of some code lines.


## v0.7.1 (2025-05-27)

### Bug Fixes

- Correctly handle python >3.10
  ([`9d9da59`](https://github.com/ID2L/pyscaf/commit/9d9da596f64b35ebe1da842049435345af98e995))


## v0.7.0 (2025-05-27)

### Bug Fixes

- Cli click flag support properly handle mixing option with the interactive call
  ([`ea390b6`](https://github.com/ID2L/pyscaf/commit/ea390b63b0506e25585abdbfd07150a199e27935))

### Features

- Added bool suport as CLI click options
  ([`4ea9405`](https://github.com/ID2L/pyscaf/commit/4ea940528a004c79095f4338bec78012668f6f23))


## v0.6.0 (2025-05-27)

### Features

- Added activate hook to modulary handle behaviour while in prompt mode, or during the skeleton and
  install hook
  ([`90ca806`](https://github.com/ID2L/pyscaf/commit/90ca806eaeef352b85d03c222ab1de298968c73f))


## v0.5.1 (2025-05-27)

### Bug Fixes

- Release action set to python 3.12
  ([`f7b2579`](https://github.com/ID2L/pyscaf/commit/f7b257952ea9903defe7c1d45e7aa106790af66c))


## v0.5.0 (2025-05-27)

### Bug Fixes

- **preference_chain**: Enhance dependency loading and tree building with detailed comments
  ([`af0e597`](https://github.com/ID2L/pyscaf/commit/af0e5970670d271a8f1edc3dcffa76e611dbdd9a))

Long description: - Improved the `load_and_complete_dependencies` function to provide clearer
  documentation on its behavior, specifically regarding the auto-completion of the 'after' property
  when only one dependency exists. - Added comprehensive comments throughout the
  `build_dependency_tree` and `DependencyTreeWalker` classes to clarify the purpose and
  functionality of each method and variable. - Enhanced the `print_tree` method to include visual
  cues for fulfilled and external dependencies, improving the usability of the dependency tree
  representation. - These changes aim to increase code readability and maintainability, making it
  easier for future developers to understand the logic behind dependency management and tree
  traversal.

### Code Style

- Added flake8 / blackformatter in local settings.json
  ([`af0e597`](https://github.com/ID2L/pyscaf/commit/af0e5970670d271a8f1edc3dcffa76e611dbdd9a))

### Features

- Make best_execution_order robust to circular dependencies
  ([`af0e597`](https://github.com/ID2L/pyscaf/commit/af0e5970670d271a8f1edc3dcffa76e611dbdd9a))

Long description: - The function now handles cycles or unsatisfiable dependencies gracefully by
  picking the first remaining node in a stable order (sorted by id) instead of raising an exception.
  - A warning is printed listing the nodes for which dependencies could not be satisfied. - This
  ensures a stable and always available execution order, even in the presence of preference cycles.

- **interactive**: Enhance project initialization with conditional questions
  ([`af0e597`](https://github.com/ID2L/pyscaf/commit/af0e5970670d271a8f1edc3dcffa76e611dbdd9a))

Long description: - Removed the interactive mode logic from the `init` function and encapsulated it
  within the `ActionManager` class, specifically in the new `ask_interactive_questions` method. -
  Introduced a `condition_to_ask` method in the `Action` class to determine if a question should be
  asked based on the current context, allowing for more dynamic and context-aware interactions. -
  Added a new CLI option for enabling versioning with Git, enhancing the project's configurability
  during initialization. - The changes aim to streamline the user experience by only prompting for
  necessary information, thus improving the overall interactivity of the project setup process.

- **preference_chain**: Add __main__.py as package entry point
  ([`af0e597`](https://github.com/ID2L/pyscaf/commit/af0e5970670d271a8f1edc3dcffa76e611dbdd9a))

Long description: - Created __main__.py in pyscaf.preference_chain to serve as the executable entry
  point for the package. - Moved the main execution logic (dependency loading and tree printing)
  from __init__.py to __main__.py. - This allows running `python -m pyscaf.preference_chain` as
  recommended by Python packaging best practices. - __init__.py now only handles package
  initialization and imports.

- **preference_chain**: Add recursive optimal dependency resolution order from root
  ([`af0e597`](https://github.com/ID2L/pyscaf/commit/af0e5970670d271a8f1edc3dcffa76e611dbdd9a))

Long description: - Introduces a recursive function to compute the optimal order of dependency
  resolution starting from a given root node. - At each recursion level, direct dependants are
  ordered using best_execution_order, and the process is applied recursively to each dependant. -
  The root id is always included as the first element in the returned order, ensuring the full
  resolution path is explicit and starts from the root. - This approach minimizes context switching
  and follows the 'after' preferences as much as possible, providing a stable and logical
  question/step ordering for complex dependency graphs. - The final optimal order is printed for
  user inspection.

### Refactoring

- Action now declare their dependencies on themselves
  ([`af0e597`](https://github.com/ID2L/pyscaf/commit/af0e5970670d271a8f1edc3dcffa76e611dbdd9a))

* [refactor] actions to be in declarative mod


## v0.4.0 (2025-05-22)

### Features

- Add support for develop branch in semantic release for prerelease and pypi-test publishing
  ([`e680e99`](https://github.com/ID2L/pyscaf/commit/e680e99b0d0fcf0a98ff3b8da791b4664f02579a))

This commit introduces configuration for the 'develop' branch in the semantic release setup. The
  'develop' branch is now recognized as a pre-release branch with a specific token for release
  candidates. Additionally, the GitHub Actions workflow has been updated to trigger releases on
  pushes to the 'develop' branch, enhancing the CI/CD pipeline for development workflows.


## v0.3.1 (2025-05-22)

### Bug Fixes

- Removed empty build path `./scripts`
  ([`d15947b`](https://github.com/ID2L/pyscaf/commit/d15947b416ddfb456f1e877557cee2848afb27b4))


## v0.3.0 (2025-05-22)

### Bug Fixes

- Remove publish script from pyproject.toml
  ([`ada55d5`](https://github.com/ID2L/pyscaf/commit/ada55d564dc2bfa4ef439ee9ba02fd24ec85eef9))

- Trying fixing semantic relaease action
  ([`dbfc241`](https://github.com/ID2L/pyscaf/commit/dbfc241e8ae2c054e58544b86d63b9c9fd56686e))

### Chores

- **release**: 0.0.0
  ([`fd4ad5d`](https://github.com/ID2L/pyscaf/commit/fd4ad5db8a12f334ac02d501122cbc5abe6da41f))

Updated project version to 0.0.0 in pyproject.toml and src/pyscaf/__init__.py. Introduced GitHub
  Actions workflow for automated releases, including steps for semantic versioning and publishing to
  TestPyPI. Removed the publish script as its functionality is now handled by the semantic-release
  tool.


## v0.2.0-rc.7 (2025-05-20)

### Chores

- **release**: 0.2.0-rc.7
  ([`faf4e8b`](https://github.com/ID2L/pyscaf/commit/faf4e8ba017155b090b2727264cba80187ec25bc))


## v0.2.0-rc.6 (2025-05-20)

### Chores

- **release**: 0.2.0-rc.6
  ([`f638e12`](https://github.com/ID2L/pyscaf/commit/f638e129419b057950c3ffd9128c012b893c970e))


## v0.2.0-rc.5 (2025-05-20)

### Chores

- **release**: 0.2.0-rc.5
  ([`5f93fab`](https://github.com/ID2L/pyscaf/commit/5f93fab756e093d23702dfa6e9112bf4c8bfe2a1))

### Features

- Trigger release 3
  ([`badfbc5`](https://github.com/ID2L/pyscaf/commit/badfbc5bd6e013fbc78a03fbbddbfa7ae31990d2))


## v0.2.0-rc.4 (2025-05-20)

### Chores

- **release**: 0.2.0-rc.4
  ([`156c4ac`](https://github.com/ID2L/pyscaf/commit/156c4ac4cbb62265076fb9129f0a3ae5b2680f76))


## v0.2.0-rc.3 (2025-05-20)

### Chores

- **release**: 0.2.0-rc.3
  ([`613679a`](https://github.com/ID2L/pyscaf/commit/613679a6dbd259e14fb0a1b5626866bfeb1a28a6))

### Features

- Trigger release 2
  ([`342eb23`](https://github.com/ID2L/pyscaf/commit/342eb23f3ee767fcd19c30bc999f00a83029c9dc))


## v0.2.0-rc.2 (2025-05-20)

### Chores

- **release**: 0.2.0-rc.2
  ([`d31d6c9`](https://github.com/ID2L/pyscaf/commit/d31d6c902f0fbf3365c228cad75c15da3a41cfd0))

### Features

- Trigger release
  ([`bf6c8d6`](https://github.com/ID2L/pyscaf/commit/bf6c8d60b0c80f8d884fbfac572fa42fe9a17de4))


## v0.2.0-rc.1 (2025-05-20)

### Chores

- **release**: 0.2.0-rc.1
  ([`48078a0`](https://github.com/ID2L/pyscaf/commit/48078a05c6de6736c2aec33edf5a008f5b31dd0e))


## v0.2.0 (2025-05-20)

### Chores

- Test prerelease
  ([`8dcf605`](https://github.com/ID2L/pyscaf/commit/8dcf605a1084890983b7c3f2dbb3ee1ee6cdfe99))

- **release**: 0.2.0
  ([`5098660`](https://github.com/ID2L/pyscaf/commit/5098660ddcd6a834cb483a968c4baf2e43d89f8d))

### Features

- Test prerelease
  ([`1a55988`](https://github.com/ID2L/pyscaf/commit/1a5598832263ab86e0fc48405b637083e895b791))

- Test prerelease
  ([`a18353a`](https://github.com/ID2L/pyscaf/commit/a18353a705c2de1cf086dbf2bac83f49f1fd8c42))


## v0.1.0 (2025-05-19)

### Chores

- A test for release
  ([`5f385c2`](https://github.com/ID2L/pyscaf/commit/5f385c2848cb4f6548264b88b9da14c041f85300))

- Initial release
  ([`3a19a23`](https://github.com/ID2L/pyscaf/commit/3a19a23beaa8712a19922d8736ed906f7eb56b6f))

- **release**: 0.1.0
  ([`3dfee75`](https://github.com/ID2L/pyscaf/commit/3dfee750e785617cfc7fbe25e2896ddddfa05f58))

### Features

- Update dependencies and project structure ([#2](https://github.com/ID2L/pyscaf/pull/2),
  [`462e0e0`](https://github.com/ID2L/pyscaf/commit/462e0e0f1f7a9b1520e4473e08af26ad308ac16f))

This commit enhances the project by updating the `pyproject.toml` and `poetry.lock` files to include
  new development dependencies such as `python-semantic-release` and `python-dotenv`. It also
  introduces a new script for publishing, improving the project's deployment capabilities. The
  `poetry.lock` file has been modified to include additional packages like `certifi`,
  `charset-normalizer`, and `click-option-group`, among others, which are essential for development
  and testing.

Furthermore, the project structure has been refined to include the `scripts` directory, allowing for
  better organization of utility scripts. The `dev` group in the `pyproject.toml` has been expanded
  to support a broader range of development tools, ensuring a more robust development environment.

These changes aim to streamline the development process and enhance the overall functionality of the
  project.
