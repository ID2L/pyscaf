# CHANGELOG


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
