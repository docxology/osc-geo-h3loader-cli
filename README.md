<!-- markdownlint-disable -->
<!-- prettier-ignore-start -->
> [!IMPORTANT]
> On June 26 2024, Linux Foundation announced the merger of its financial services umbrella, the Fintech Open Source Foundation ([FINOS](https://finos.org)), with OS-Climate, an open source community dedicated to building data technologies, modeling, and analytic tools that will drive global capital flows into climate change mitigation and resilience; OS-Climate projects are in the process of transitioning to the [FINOS governance framework](https://community.finos.org/docs/governance); read more on [finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg](https://finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg)
<!-- prettier-ignore-end -->
<!-- markdownlint-enable -->

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
