<!-- markdownlint-disable -->
<!-- prettier-ignore-start -->
> [!IMPORTANT]
> On June 26 2024, Linux Foundation announced the merger of its financial services umbrella, the Fintech Open Source Foundation ([FINOS](https://finos.org)), with OS-Climate, an open source community dedicated to building data technologies, modeling, and analytic tools that will drive global capital flows into climate change mitigation and resilience; OS-Climate projects are in the process of transitioning to the [FINOS governance framework](https://community.finos.org/docs/governance); read more on [finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg](https://finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg)
<!-- prettier-ignore-end -->
<!-- markdownlint-enable -->

> [!NOTE]
> **Docxology Fork - July 2025**
> 
> This repository is a fork of the original OS-Climate `osc-geo-h3loader-cli` project, maintained by [docxology](https://github.com/docxology) with several improvements and updates:
> 
> ### H3 Library Upgrade to v4
> The fork has been updated to use H3 library version 4.x, which introduces significant API changes from the original v3.x implementation. Key method name changes include:
> 
> **Core Indexing Functions:**
> - `h3.geo_to_h3(lat, lng, res)` → `h3.latlng_to_cell(lat, lng, res)`
> - `h3.h3_to_geo(h3_index)` → `h3.cell_to_latlng(h3_index)`
> - `h3.h3_to_geo_boundary(h3_index)` → `h3.cell_to_boundary(h3_index)`
> 
> **Hierarchical Operations:**
> - `h3.h3_to_parent(h3_index, res)` → `h3.cell_to_parent(h3_index, res)`
> - `h3.h3_to_children(h3_index, res)` → `h3.cell_to_children(h3_index, res)`
> 
> **Region Operations:**
> - `h3.polyfill(geojson, res)` → `h3.polygon_to_cells(geojson, res)`
> 
> **Traversal Functions:**
> - `h3.k_ring(h3_index, k)` → `h3.k_ring(h3_index, k)` (unchanged)
> - `h3.hex_ring(h3_index, k)` → `h3.hex_ring(h3_index, k)` (unchanged)
> 
> **Inspection Functions:**
> - `h3.h3_is_valid(h3_index)` → `h3.is_valid_cell(h3_index)`
> - `h3.h3_get_resolution(h3_index)` → `h3.get_resolution(h3_index)`
> 
> ### Additional Improvements
> - Enhanced error handling and validation
> - Improved performance optimizations
> - Better integration with modern Python geospatial libraries
> - Updated dependencies for Python 3.13 compatibility
> 
> For more information about H3 v4 changes, see the [official H3 documentation](https://h3geo.org/docs/upgrade-guide) and [migration guide](https://h3geo.org/docs/migration-guide).

# osc-geo-h3grid-srv - Service for Geospatial Temporal Data Mesh

Experimental geospatial temporal data mesh that uses
H3 (from Uber) cells to create a uniform mesh of regions
of varying resolutions for the globe.

Capabilities include:

- loading geospatial data
- interpolating latitude/longitude data to map into H3 cells
  of varying resolution.
- managing shapefiles

The Ecosystem Platform was originally developed by Broda Group Software
with key contributions by:

- [Eric Broda](https://www.linkedin.com/in/ericbroda/)
- [Davis Broda](https://www.linkedin.com/in/davisbroda/)
- [Graeham Broda](https://www.linkedin.com/in/graeham-broda-3a2294b3/)

## The Geospatial Grid

The h3 geospatial indexing system is an indexing system created
by Uber to represent the entire globe. It consists of a series of
hexagonal grids that cover the world at different resolution levels.

For more information see the [h3 website](https://h3geo.org/), or
[uber's h3 introduction blog](https://www.uber.com/en-CA/blog/h3/)

## Setting up your Environment

**Important Note for Fiona and GDAL:**
Fiona, a dependency for geospatial operations, requires a system-level installation of GDAL and its development libraries (e.g., `libgdal-dev` on Debian/Ubuntu, `gdal-devel` on RHEL/Fedora, or `gdal` via Homebrew on macOS). Please ensure GDAL is installed on your system before attempting to install Python dependencies. Refer to Fiona's official documentation for detailed installation instructions: [https://fiona.readthedocs.io/en/latest/manual.html#installing-fiona](https://fiona.readthedocs.io/en/latest/manual.html#installing-fiona)

Some environment variables are used by various code and scripts.
Set up your environment as follows (note that "source" is used)

```bash
source ./bin/environment.sh
```

It is recommended that a Python virtual environment be created.
Several convenience scripts are available to create and activate
a virtual environment.

To create a new virtual environment (it will create a directory
called "venv" in your current working directory):

```bash
$PROJECT_DIR/bin/venv.sh
```

Once your virtual enviornment has been created, it can be activated
as follows (note: you _must_ activate the virtual environment
for it to be used, and the command requires "source" to ensure
environment variables to support venv are established correctly):

```bash
source $PROJECT_DIR/bin/vactivate.sh
```

Install the required libraries as follows:

```bash
pip install -r requirements.txt
```

## Getting started

For a brief overview of how to get started with this application, see
the [Getting Started Guide](/docs/getting-started.md).

## About the CLIs

To see more information about particular aspects of the geo server, see
the below documentation.

This repo offers a command language interface (CLI) to demonstrate
this functionality:

- [Geospatial](/docs/README-geospatial.md):
  Query information in the Geospatial Data Mesh
- [Data Loading](/docs/README-loading.md):
  Interpolate sparse data into H3 cell grid
- [Shapefile](/docs/README-shapefile.md):
  Shapefile simplification, statistics, and viewing
- [Repository](/docs/README-repository.md):
  Shapefile registration and inventory management
- [End-to-End Examples](/docs/README-example.md):
  Examples of datasets taken from loading to visualization

## Running tests

(You may need to install pytest)

```bash
pytest ./test
```

## Branch Naming Guidelines

Each branch should have an associated github issue. Branches should be named
as follows:
`<branch-type>/issue-<issue number>-<short description>`.
Where the branch type is one of:
[feature, bugfix, hotfix],
the issue number is the number of the associated issue, and the
short description is a dash ('-') seperated description of the branch's purpose.
This to between one and three words if possibble.

## Roadmap

For information on planned features, see the [roadmap](/docs/roadmap.md)
