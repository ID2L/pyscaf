# License Action

This action allows you to add a LICENSE file to your project during scaffolding.

## Features
- Proposes a list of standard open source licenses (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, Mozilla, Unlicense)
- Copies the corresponding license template into the project root as LICENSE
- Dynamically fills in the year and author if provided in the context

## Usage
When running the scaffolder, you will be prompted to choose a license for your project. The selected license will be added as a LICENSE file in your project root.

## Supported Licenses
- MIT
- Apache-2.0
- GPL-3.0
- BSD-3-Clause
- Mozilla (MPL-2.0)
- Unlicense

You can customize the author name by providing the --author option (if available in your context). 