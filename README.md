# CRESCENT CPAL-WEB

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)

**CPAL-WEB** is a web-based application for visualizing and interacting with site-based data prepared by the Paleoseismology Group of the Cascadia Region Earthquake Science Center ([CRESCENT](https://cascadiaquakes.org/about-crescent/)) and the USGS Powell Center Working Group on [Cascadia Subduction Zone Earthquake Hazards](https://www.usgs.gov/centers/john-wesley-powell-center-for-analysis-and-synthesis/science/margin-wide-geological-and). The goal of this group is to study past earthquake events through geological evidence, enhancing our understanding of seismic hazards in the Cascadia Subduction Zone. This platform allows users to explore mapped sites, evidence types, and attributes collected by the Paleoseismology Group via a dynamic interface powered by [CesiumJS](https://cesium.com/platform/cesiumjs/) maps and the [FastAPI](https://fastapi.tiangolo.com/) web framework.

**Live viewer:** https://cpal.cascadiaquakes.org

---

## Documentation

The [CPAL book](https://cascadiaquakes.github.io/cpal-book/) describes the datasets, their columns, and how to use the viewer.

---

## Features

- Interactive Cesium 3D map for visualizing geologic evidence sites.
- Dropdown selection of sites sorted by latitude, with support for colocated sites distinguished by evidence type.
- Dynamic display of site attributes in a tabular format.
- Filtering and toggling of different site categories (e.g., Fragile Geologic Features).
- Export of filtered events as GeoJSON, JSON, or CSV, and download of the raw dataset files.

---

## Data

The viewer reads site data from **GeoJSON files** with valid `latitude` and `longitude` properties. Each GeoJSON feature includes relevant site attributes such as site name, evidence type, and ranking/classification information.

To prepare data in this format, refer to the companion [CRESCENT-CPAL](https://github.com/cascadiaquakes/CRESCENT-CPAL) repository, which provides the CPAL datasets, Excel parsing tools, and conversion scripts to generate compliant GeoJSON files.

The full compilation files are available from the [USGS ScienceBase data release](https://doi.org/10.5066/P13OJQYW) (see [How to Cite](#how-to-cite)).

---

## Running Locally

You need a [Cesium ion](https://cesium.com/ion/) access token. Put it in a `.env` file in the repository root (it is gitignored):

```bash
CESIUM_KEYS={"cesium_access_token":"<your-cesium-ion-token>"}
```

**With Docker:**

```bash
docker build -t cpal-web .
docker run --env-file .env -p 8000:80 cpal-web
```

**Without Docker** (Python 3.13):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
uvicorn main:app --reload --port 8000 --env-file ../.env
```

The app will be available at <http://localhost:8000>.

---

## Project Structure

```
CPAL-WEB/
├── app/
│   │                               # Application logic (FastAPI app, routers, utilities)
│   ├── static/                     # Static assets such as CSS, JS, icons, and GeoJSON
│   │   ├── config/                 # Site configuration parameters including URLs to the GeoJSON datasets
│   │   └── ...
│   │
│   ├── templates/                  # HTML templates rendered by FastAPI
│   │   ├── cpal_page.html          # Site pages template
│   │   └── ...
│   │
│   ├── main.py                     # FastAPI app entry point
│   └── routes.py                   # FastAPI route handlers
├── infra/                          # Infrastructure-as-Code
├── Dockerfile                      # Docker configuration for containerized deployment
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Deployment

The application is deployed to AWS via a CDK app in `infra/`. The GitHub Actions workflow in `.github/workflows/main.yml` builds and pushes a Docker image to ECR, deploys to [dev.cpal.cascadiaquakes.org](https://dev.cpal.cascadiaquakes.org) automatically on merges to `main`, and gates production deployment behind a GitHub Environment approval.

---

## How to Cite

The paleoseismic data shown in the viewer come from:

> Staisch, L.M., Witter, R.C., Watt, J.T., Grant, A.R., Walton, M.A., Brothers, D., Davis, E., Dura, C., Engelhart, S., Enkin, R., Garrison-Laney, C.E., Goldfinger, C., Hamilton, T., Hawkes, A., Hill, J.C., Hong, I.J., Jaffe, B.E., Kelsey, H., Lahusen, S.R., La Selle, S.M., Nelson, A.R., Nieminski, N.M., Padgett, J.S., Patton, J., Pearl, J.K., Pilarczyk, J., Sherrod, B., and Stanton, K., 2024, Compiled onshore and offshore paleoseismic data along the Cascadia Subduction zone: U.S. Geological Survey data release, https://doi.org/10.5066/P13OJQYW

---

## License

This project is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE).

---

## Contacts

**Software** (questions about the viewer, data access, or downloads):
- **Amanda M. Thomas**, University of California, Davis: [amthom@ucdavis.edu](mailto:amthom@ucdavis.edu)
- **William Marfo**, University of California, Davis: [wmarfo@ucdavis.edu](mailto:wmarfo@ucdavis.edu)
- **Loïc Bachelot**, University of Oregon: [lbachelo@uoregon.edu](mailto:lbachelo@uoregon.edu)

**Data** (questions about the paleoseismic data compilations):
- **Tina Dura**, Virginia Tech: [tinadura@vt.edu](mailto:tinadura@vt.edu)
- **Lydia Staisch**, U.S. Geological Survey: [lstaisch@usgs.gov](mailto:lstaisch@usgs.gov)

You can also use the [Contact Us page](https://cpal.cascadiaquakes.org/request) or [open an issue](https://github.com/cascadiaquakes/CRESCENT-CPAL-WEB/issues).

---

## Acknowledgments

This project is supported by the National Science Foundation through the Cascadia Region Earthquake Science Center (CRESCENT), Cooperative Agreement EAR-2225286, in collaboration with the USGS Powell Center Working Group on Cascadia Subduction Zone Earthquake Hazards.

---

## Disclaimers

**USGS Data Disclaimer**:
Unless otherwise stated, all data, metadata, and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data for other purposes, nor on all computer systems, nor shall the act of distribution constitute any such warranty.

**USGS Nonendorsement Disclaimer**:
Any use of trade, firm, or product names is for descriptive purposes only and does not imply endorsement by the U.S. Government.
