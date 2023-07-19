import uvicorn

from fastapi import FastAPI

from fastapi.responses import HTMLResponse
from datetime import datetime
from fastapi import FastAPI, Form, Request, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_mqtt import FastMQTT, MQTTConfig



mqtt_config = MQTTConfig(
    host='10.10.1.224',
    port=1883,
    username='rfi_dominator'
)

mqtt = FastMQTT(config=mqtt_config)

app = FastAPI()
mqtt.init_app(app)

app.mount("/static", StaticFiles(directory="src/static", html=True), name="static")
templates = Jinja2Templates(directory='src/htmldirectory')    



@mqtt.on_connect()
def mqtt_connect(client, flags, rc, properties):
    mqtt.client.subscribe("#")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    data = payload.decode("utf-8")
    # some_list.append(f'{topic}, {data}, {time.time()}')
    print("Received message: ", topic, data, qos, properties)
    return 0


@mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    return 0


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)





@app.on_event("startup")
async def startup_event():
    """Start up event for FastAPI application."""
    print("there's a new cowboy in town!!")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})



