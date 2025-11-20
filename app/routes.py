import os
import boto3

from fastapi import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageDraw
from io import BytesIO

from datetime import datetime, timezone
import json
import logging
import httpx


router = APIRouter()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_DIR = os.path.join(BASE_DIR, "static", "json")
NETCDF_DIR = os.path.join(BASE_DIR, "static", "netcdf")
LOGO_FILE = "static/images/Crescent_Logos_horizontal_transparent.png"

# Logo placement in inches below the lower left corner of the plot area
LOGO_INCH_OFFSET_BELOW = 0.5

# Templates
templates = Jinja2Templates(directory="templates")


def utc_now():
    """Return the current UTC time."""
    try:
        _utc = datetime.now(tz=timezone.utc)
        utc = {
            "date_time": _utc.strftime("%Y-%m-%dT%H:%M:%S"),
            "datetime": _utc,
            "epoch": _utc.timestamp(),
        }
        return utc
    except:
        logging.error(f"[ERR] Failed to get the current UTC time")
        raise


def standard_units(unit):
    """Check an input unit and return the corresponding standard unit."""
    unit = unit.strip().lower()
    if unit in ["m", "meter"]:
        return "m"
    elif unit in ["degrees", "degrees_east", "degrees_north"]:
        return "degrees"
    elif unit in ["km", "kilometer"]:
        return "km"
    elif unit in ["g/cc", "g/cm3", "g.cm-3", "grams.centimeter-3"]:
        return "g/cc"
    elif unit in ["kg/m3", "kh.m-3"]:
        return "kg/m3"
    elif unit in ["km/s", "kilometer/second", "km.s-1", "kilometer/s", "km/s"]:
        return "km/s"
    elif unit in ["m/s", "meter/second", "m.s-1", "meter/s", "m/s"]:
        return "m/s"
    elif unit.strip().lower in ["", "none"]:
        return ""


def create_error_image(message: str) -> BytesIO:
    """Generate an image with an error message."""
    # Create an image with white background
    img = Image.new("RGB", (600, 100), color=(255, 255, 255))

    # Initialize the drawing context
    d = ImageDraw.Draw(img)

    # Optionally, add a font (this uses the default PIL font)
    # For custom fonts, use ImageFont.truetype()
    # font = ImageFont.truetype("arial.ttf", 15)

    # Add text to the image
    d.text(
        (10, 10), message, fill=(255, 0, 0)
    )  # Change coordinates and color as needed

    # Save the image to a bytes buffer
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    image_data = (
        img_io.read()
    )  # Read the entire stream content, which is the image data

    return image_data


@router.get("/map3d", response_class=HTMLResponse)
async def map3d(request: Request):
    return templates.TemplateResponse("map_3d.html", {"request": request})


@router.post("/submitForm")
async def submit_form(
    name: str = Form(...),
    institution: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):

    try:
        # Create SES client
        AWS_REGION = "us-east-2"
        SENDER_EMAIL = "manochehr.bahavar@earthscope.org"
        RECIPIENT_EMAIL = "manochehr.bahavar@earthscope.org"
        ses_client = boto3.client("ses", region_name=AWS_REGION)

        # Email content
        subject = "New Request from Form"
        body_text = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        body_html = f"""<html>
        <head></head>
        <body>
        <h1>New Request</h1>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong> {message}</p>
        </body>
        </html>
                    """

        response = ses_client.send_email(
            Destination={
                "ToAddresses": [
                    RECIPIENT_EMAIL,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": "UTF-8",
                        "Data": body_html,
                    },
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": body_text,
                    },
                },
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": subject,
                },
            },
            Source=SENDER_EMAIL,
        )
    except Exception as e:
        # Log the exception if needed
        logging.error(f"[ERR] Error sending email: {e}")
    return HTMLResponse(content="<p>Form submitted successfully!</p>", status_code=200)


@router.get("/get-token")
async def get_cesium_key(request: Request):
    """This must be secured lated to avoid external"""

    # Only internal requests are accepted.
    if os.getenv("CESIUM_KEYS") is None:
        logging.warning(f"[INFO] get-token Failed")
        return {"token": "your_access_token"}
    else:
        CESIUM_KEYS = json.loads(os.getenv("CESIUM_KEYS"))
        access_token = CESIUM_KEYS["cesium_access_token"]
        api_key = CESIUM_KEYS["arcgis_default_access_token"]
        return {"token": access_token, "apikey": api_key}


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/downloads", response_class=HTMLResponse)
async def downloads(request: Request):
    return templates.TemplateResponse("downloads.html", {"request": request})


@router.get("/3d", response_class=HTMLResponse)
async def threed(request: Request):
    return templates.TemplateResponse("view3d.html", {"request": request})


@router.get("/request", response_class=HTMLResponse)
async def request(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@router.get("/news", response_class=HTMLResponse)
async def news(request: Request):
    return templates.TemplateResponse("news.html", {"request": request})


@router.get("/cesium", response_class=HTMLResponse)
async def cesium(request: Request):
    return templates.TemplateResponse("cesium.html", {"request": request})


# Route to create html for model dropdown.
@router.get("/models_drop_down_coverage", response_class=HTMLResponse)
def models_drop_down_coverage():
    json_directory = JSON_DIR
    coords_list = list()
    model_list = list()
    title_list = list()
    for filename in sorted(os.listdir(json_directory)):
        logging.warning(f"[INFO] Reading {filename}")
        # Opening the file and loading the data
        with open(os.path.join(json_directory, filename), "r") as file:
            json_data = json.load(file)
            logging.warning(f"[INFO] {json_data}")
            coords = list()
            coords.append(str(json_data["geospatial_lon_min"]))
            coords.append(str(json_data["geospatial_lon_max"]))
            coords.append(str(json_data["geospatial_lat_min"]))
            coords.append(str(json_data["geospatial_lat_max"]))

            # Cesium takes depth in meters
            if standard_units(json_data["geospatial_vertical_units"]) == "m":
                depth_factor = 1000
            elif standard_units(json_data["geospatial_vertical_units"]) == "km":
                depth_factor = 1
            else:
                depth_factor = 1
                logging.error(
                    f"[ERR] Invalid depth unit of {json_data['geospatial_vertical_units']}"
                )

            coords.append(
                str(float(json_data["geospatial_vertical_min"]) / depth_factor)
            )
            coords.append(
                str(float(json_data["geospatial_vertical_max"]) / depth_factor)
            )

            model_coords = f"({','.join(coords)})"
            if "title" in json_data:
                title_list.append(json_data["title"])
            else:
                title_list.append("-")
            model_name = json_data["model"]
            coords_list.append(model_coords)
            model_list.append(model_name)

    # Prepare the HTML for the dropdown
    dropdown_html = f'<option value="">None</option>'
    for i, filename in enumerate(model_list):
        selected = " selected" if i == 0 else ""
        dropdown_html += (
            f'<option value="{coords_list[i]}"{selected}>{model_list[i]}</option>'
        )
    return dropdown_html


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(router, host="127.0.0.1", port=8080)
