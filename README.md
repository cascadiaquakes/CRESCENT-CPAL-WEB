# CRESCENT CPAL-WEB

**CPAL-WEB** is a web-based application for visualizing and interacting with site-based data prepared the Paleoseismology Group of the Cascadia Region Earthquake Science Center ([CRESCENT](https://cascadiaquakes.org/about-crescent/)) and the USGS Powell Center Working Group on [Cascadia Subduction Zone Earthquake Hazards](https://www.usgs.gov/centers/john-wesley-powell-center-for-analysis-and-synthesis/science/margin-wide-geological-and). The goal of this group is to study past earthquake events through geological evidence, enhancing our understanding of seismic hazards in the Cascadia Subduction Zone. This platform allows users to explore mapped sites, evidence types, and attributes collected by the Paleoseismology Group via a dynamic interface powered by [CesiumJS](https://cesium.com/platform/cesiumjs/) maps and [FastAPI](https://fastapi.tiangolo.com/) web framework. The full compilation files are available from the [USGS ScienceBase data release](https://doi.org/10.5066/P13OJQYW).


## Features

- Interactive Cesium 3D map for visualizing geologic evidence sites.
- Dropdown selection of sites sorted by latitude, with support for colocated sites distinguished by evidence type.
- Dynamic display of site attributes in a tabular format.
- Filtering and toggling of different site categories (e.g., Fragile Geologic Features).
- Integration with GeoJSON datasets.

## Directory Structure

```
CPAL-WEB/
├── app
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
├── Dockerfile                      # Docker configuration for containerized deployment
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Data Format Requirements

The web viewer expects site data in the form of **GeoJSON files** with valid `latitude` and `longitude` properties. Each GeoJSON feature should include relevant site attributes such as site name, evidence type, and ranking/classification information.

To prepare data in this format, refer to the companion **CRESCENT-CPAL** repository:

🔗 [CRESCENT-CPAL](https://github.com/cascadiaquakes/CRESCENT-CPAL)  
This repository provides CPAL datasets, Excel parsing tools, and conversion scripts to generate compliant GeoJSON files.

Raw data are available from Staisch, L.M., Witter, R.C., Watt, J.T., Grant, A.R., Walton, M.A., Brothers, D., Davis, E., Dura, C., Engelhart, S., Enkin, R., Garrison-Laney, C.E, Goldfinger, C., Hamilton, T., Hawkes, A., Hill, J.C., Hong, I.J., Jaffe, B.E., Kelsey, H., Lahusen, S.R, La Selle, S.M, Nelson, A.R, Nieminski, N.M, Padgett, J.S, Patton, J., Pearl, J.K, Pilarczyk, J., Sherrod, B., and Stanton, K., 2024, Compiled onshore and offshore paleoseismic data along the Cascadia Subduction zone: U.S. Geological Survey data release, [https://doi.org/10.5066/P13OJQYW](https://doi.org/10.5066/P13OJQYW).

## Contact

For questions, feedback, or contributions, please visit the [Contact Us page](https://cpal.cascadiaquakes.org/request).

## Disclaimers

**USGS Data Disclaimer**:  
Unless otherwise stated, all data, metadata, and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data for other purposes, nor on all computer systems, nor shall the act of distribution constitute any such warranty.

**USGS Nonendorsement Disclaimer**:  
Any use of trade, firm, or product names is for descriptive purposes only and does not imply endorsement by the U.S. Government.