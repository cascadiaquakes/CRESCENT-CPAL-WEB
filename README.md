# CRESCENT CPAL-WEB

**CPAL-WEB** is a web-based application for visualizing and interacting with site-based data prepared by the Paleoseismology Group of the Cascadia Region Earthquake Science Center ([CRESCENT](https://cascadiaquakes.org/about-crescent/)). The goal of this group is to study past earthquake events through geological evidence, enhancing our understanding of seismic hazards in the Cascadia Subduction Zone. This platform allows users to explore mapped sites, evidence types, and attributes collected by the Paleoseismology Group via a  dynamic interface powered by [CesiumJS](https://cesium.com/platform/cesiumjs/) maps and [FastAPI](https://fastapi.tiangolo.com/) web framework.

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

## Contact

For questions, feedback, or contributions, please visit the [Contact Us page](https://cpal.cascadiaquakes.org/request).
