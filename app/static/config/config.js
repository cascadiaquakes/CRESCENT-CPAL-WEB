// Cesium access token
const local_config = window.SKIP_CESIUM;
if (!local_config.skip) {
    Cesium.Ion.defaultAccessToken = "your_access_token";
    Cesium.ArcGisMapService.defaultAccessToken = "your_api_key"
}

// Proxy names
const PROXIES = ["coastal", "terrestrial", "marine", "tsunami"];

columnDefinitions = { "Contact Name": " stratigraphic contact or event identified in paleoseismic studies that may be equivalent to evidence for megathrust earthquakes. Other possible mechanisms are noted in the fields Inferred most likely evidence source and Other possible evidence source interpretations below" }

// GeoJSON Configuration Arrays
// Coastal_Deformation_Data_Compilation_TLDR.geojson
const GEOJSON_URLS = {
    "coastal": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/geojson/Coastal_Deformation_Data_Compilation_TLDR.geojson',
    "marine": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/geojson/Marine_Shaking_Data_Compilation_TLDR.geojson',
    "terrestrial": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/geojson/Terrestrial_Shaking_Data_Compilation_TLDR.geojson',
    "tsunami": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/geojson/Tsunami_Data_Compilation_TLDR.geojson',
};

const COLUMNS_DESCRIPTION = {
    "coastal": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/json/Coastal_Deformation_Data_Compilation_cell_descriptions.json',
    "marine": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/json/Marine_Shaking_Data_Compilation_cell_descriptions.json',
    "terrestrial": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/json/Terrestrial_Shaking_Data_Compilation_cell_descriptions.json',
    "tsunami": 'https://raw.githubusercontent.com/cascadiaquakes/CRESCENT-CPAL/refs/heads/main/data/json/Tsunami_Data_Compilation_cell_descriptions.json',
};
//const GEOJSON_URLS = {
//    "coastal": '/static/geojson/Coastal_Deformation_Data_Compilation.geojson',
//    "terrestrial": '/static/geojson/Terrestrial_Shaking_Data_Compilation.geojson',
//    "marine": '/static/geojson/Marine_Shaking_Data_Compilation.geojson',
//    "tsunami": '/static/geojson/Tsunami_Data_Compilation.geojson'
//};

// GeoJSON Configuration Arrays
const GEOJSON_NAMES = {
    "coastal": 'Coastal Deformation Datasets',
    "terrestrial": 'Terrestrial Shaking Datasets',
    "marine": 'Marine Shaking Datasets',
    "tsunami": 'Tsunami Datasets'
};
// Proxy types for GeoJSON data
const PROXY_TYPES = {
    "coastal": { 'coastal': 'Land-level Change' },
    "terrestrial": {
        'Inlets and Lakes': 'Lake/Inlet',
        'Liquefaction': 'Liquefaction',
        'Subaerial Landslides': 'Landslide',
        'Fragile Geologic Features': 'Fragile feature'
    },
    "marine": { 'marine': 'Turbidite' },
    "tsunami": { 'tsunami': 'Tsunami' }
};

// Shapes for proxy types
const SHAPES = {
    'Land-level Change': 'square',
    "Land-level change": 'square',
    'Lake/Inlet': 'semicircle',
    'Inlets and Lakes': 'semicircle',
    'Liquefaction': 'triangle',
    'Landslide': 'triangle-side',
    'Subaerial Landslides': 'triangle-side',
    'Fragile feature': 'triangle-side',
    'Fragile Geologic Features': 'triangle-side',
    "Marine Turbidite": 'pentagon',
    "Turbidite": 'pentagon',
    "Tsunami": 'circle',
    'Tsunami inundation': 'circle'
};

// Colors for proxy types
const COLORS = {
    "Land-level Change": 'magenta',
    "Land-level change": 'magenta',
    'Lake/Inlet': 'purple',
    'Inlets and Lakes': 'purple',
    'Liquefaction': 'yellow',
    'Landslide': 'orange',
    'Subaerial Landslides': 'orange',
    'Fragile feature': 'blue',
    'Fragile Geologic Features': 'blue',
    "Marine Turbidite": 'green',
    "Turbidite": 'green',
    "Tsunami": 'cyan',
    'Tsunami inundation': 'cyan'
};

// Labels for proxy types
const LABELS = {
    "Land-level Change": 'Land-level Change',
    "Land-level change": 'Land-level Change',
    'Lake/Inlet': 'Lake/Inlet',
    'Inlets and Lakes': 'Lake/Inlet',
    'Liquefaction': 'Liquefaction',
    'Landslide': 'Landslide',
    'Subaerial Landslides': 'Landslide',
    'Fragile feature': 'Fragile feature',
    'Fragile Geologic Features': 'Fragile feature',
    "Marine Turbidite": 'Turbidite',
    "Turbidite": 'Turbidite',
    "Tsunami": 'Tsunami',
    'Tsunami inundation': 'Tsunami'
};

// Scale factors for GeoJSON entities
const SCALE_FACTORS = {
    "coastal": [5],
    "terrestrial": [5, 5, 5, 5],
    "marine": [5],
    "tsunami": [5]
};

// Map bounds for study area
const MAP_BOUNDS = {
    west: -130,
    south: 39,
    east: -116,
    north: 52
};
// Marker size and visibility controls.
const baseMarkerSize = 9;

// Eye offset ranges for small, medium, and large markers, applying different scaling methods to each category
const eyeOffsetFactor = [10000, 700, 50]; // Larger factor to make smaller markers appear closer
const disableDepthTestDistance = 1000000  // Ensures visibility at all distances

// Set initial transparency to 20% (0.8 on a scale from 0 to 1)
const initialTransparency = 0.2;
let gridOpacity = 0.1; // Initial grid transparency value

const zoomOutFactor = 1.3; // Increased zoom out factor for better visibility

// Check if Cesium.Ion.defaultAccessToken is not set or is using the placeholder token.
// using a synchronous XHR request, ensuring that the Cesium token is fetched and 
// set before any further processing. This will block the browser until the token 
// is fetched, but it guarantees that the token is available before proceeding.
// Synchronous XHR is deprecated and will block page rendering, so this method 
// should only be used as a last resort.However, it guarantees that the token 
// is set before any dependent scripts run. Our fetch is quick and is OK to use.
if (!local_config.skip) {
    if (!Cesium.Ion.defaultAccessToken || Cesium.Ion.defaultAccessToken === "your_access_token" || !Cesium.ArcGisMapService.defaultAccessToken || Cesium.ArcGisMapService.defaultAccessToken == "your_api_key") {
        console.log("Cesium access token not set or is using the placeholder token. Retrieving from server...");// + Cesium.Ion.defaultAccessToken);

        try {
            // Create a synchronous XHR request to fetch the token
            const xhr = new XMLHttpRequest();
            xhr.open('GET', '/get-token', false);  // `false` makes the request synchronous
            xhr.send();

            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                Cesium.Ion.defaultAccessToken = data.token;
                console.log("Cesium access token set successfully.");// + Cesium.Ion.defaultAccessToken);
                Cesium.ArcGisMapService.defaultAccessToken = data.apikey;
                console.log("Cesium ArcGisMapService ApiKey set successfully.");// + Cesium.ArcGisMapService.defaultAccessToken);
            } else {
                throw new Error("Failed to fetch Cesium access token/ArcGisMapService ApiKey from server.");
            }
        } catch (error) {
            console.error("Error fetching Cesium access token and ArcGisMapService ApiKey:", error);
        }
    } else {
        console.log("Cesium access token and ArcGisMapService ApiKey are already set and valid.");
    }
}
