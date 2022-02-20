## Sensor Device: Architectural Abstract
<p>When hundreds of thousands of hardware devices are concurrently uploading sensors data, performance, availability, 
and scalability are questions that needed to be answered while designing the infrastructure to sustain the system.</p>
<p>In this scenario, I suggest to deploy the system on cloud service where scalability, and high availability can be provided within minutes.  
The following graphic describes an integration infrastructure design where the application will be deployed</p>
<div style="margin: 0px auto;">
<img src="https://storage.googleapis.com/josue-kula-static/design_abstract/josue-kula-Aws-design.svg" width="400" height="400"/>
</div>

## Installing packages
Before running , we need to install required packages on top of which application components have been built.
``` bash
# Clone the repository
$ git clone https://github.com/nn-naga/

# create a virtual environment
$ cd canary-device && python3 -m venv virtualenv

# install packages
source ./virtualenv/bin/activate && ./virtualenv/bin/python -m pip install -r requirements.txt
```

## Database

In the architectural blueprint, we suggest that persistent data should be redundant with 2 or more database per availability zone.
However, for demo purpose, I'm using db.sqlite in order to easily run and test the app.
```python
# ../sensorsdev/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
### Make migrations before running the application
``` bash
(virualenv)youser@hostname:~$ cd sensorsdev && ./virtualenv/bin/python manage.py makemigrations

$ ./virtualenv/bin/python manage.py migrate
```
We have to make sure there's a newly created file named db.sqlite at the current directory

## Running the app locally

```bash
(virualenv)youser@hostname:~$ cd sensorsdev && ./virtualenv/bin/python manage.py runserver
```
## Application Configuration
As you can see at the file requirements .txt, we used django and django-rest-framework to create sensors device app.
In order to ubiquitously have the correct Datetime across end-user at different geographical location, we need to configure both
the server and django project to use UTC TIMEZONE.
However, for testing purpose, we have decided to set the time to New York timezone

```python
 # ../sensorsdev/settings.py
  TIME_ZONE = 'America/New_York'
  USE_TZ = True
``` 
Attention should also be paid at SECRET_KEY and DEBUG config setting that are exposed by default.
In real production ready application, we have to hide our SECRET_KEY and dynamically switch DEBUG
value in dev - production environment.

### Dealing with secret_key and debug
```python
SECRET_KEY = 'ik!81-q8usbm-oqwui*!oty+^3y$+8q8m#als$$_j)y%667y&5'
``` 

Since the Rest API resources do not require authentication and the service functionality requires resources to
handle many request but not too many, we configured the projects to only accept 60 request per minutes (GET, POST, PUT, DELETE)

```python
REST_FRAMEWORK = {
 #....

 'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute'
    },
}
```
### Dealing with timestamp format
At the requirement level, the payload appears to have sensor_reading_time to be on unix timestamp format.
We did not choose that format to facilitate datetime conversion at different geographical location from the end-user 
perspective. we are using datetime format with timezone.

```python
  REST_FRAMEWORK = {
  'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S",
 #...  
}
# Note: this format not applied while querying datetime range in django
```
#### JWT Authentication
![Screenshot (26)](https://user-images.githubusercontent.com/53946839/154868700-bd39c33e-c022-49b4-9c96-b57e036c0e54.png)

## API Resource and utilization
### API Resource
For sensors application, we have two resources to handle writing and reading from the database.
``` bash
 The first resource http://localhost:8000/sensors/devices/ handles creating new record, getting all sensors data
 and getting a single record using uuid as url parameter
 # use GET (with uuid), POST, DELETE, and PUT
```
[Devices: http://localhost:8000/sensors/devices/](http://localhost:8000/sensors/devices/)
``` bash
 The second resource http://localhost:8000/sensors/devices/ handles data retrieval using
 star_time and date_time
 # use GET (datetime range ), PUT, and DELETE
```
[Retrive: http://localhost:8000/sensors/retrieve/](http://localhost:8000/sensors/retrieve/)
#### Note: make sure the project is running before you check the url

### API Utilization
As soon as you run the application, there's no data insert at migration level. so the device table should be empty
To confirm, try to get all sensors data using a simple curl command.
```bash
 curl -X GET http://localhost:8000/sensors/devices/
 # returns [] empty list
```
Great, Now let create a new record
```bash
  curl -X POST -H "Content-Type: application/json" -d \
 '{"sensor_value": 5.0, "sensor_type": "temperature"}' http://localhost:8000/sensors/devices/
```
Notice we have just created a new record using two fields: 
* sensor_value which is required, and;
* sensor_type which is optional with default value temperature

#### Simulating concurrent HTTP requests
To simulate concurrent requests with constraint on data upload, we create a http client script 
using a python coroutine module for http client and service called aiohttp.
To see how it works, we need first to generate 10 sensor value(s) with random sensor_type 

##### Open a new terminal window to keep the application running ...

``` bash
# at the project root (sensorsdev), type the following command
(virualenv)youser@hostname:~$ ./virtualenv/bin/python http_client.py -n 10 --url http://localhost:8000/sensors/devices/
```
The preceding command generates random temperature and creates 10 records on database.
Now, let check to make sure we now have records in the database

```bash
  # the following returns a json non pretty array of objects
  curl -X GET http://localhost:8000/sensors/devices/
```

We can also check directly from django shell 
##### Open a new terminal to check number of the records 
```bash
(virualenv)youser@hostname:~$ ./virtualenv/bin/python manage.py shell
>>> from sensors.model import Device
>>> check_length = Device.objects.all()
>>> len(check_length)
>>> 11
```

### Checking Data Constraint on field sensor_value
the application functionality restricts sensor_value between 0.0 to 100.0.
Let check it out and see what's happened
```bash
 curl -X POST -H "Content-Type: application/json" -d  \
 '{"sensor_value": 100.0, "sensor_type": "temperature"}' http://localhost:8000/sensors/devices/
```
Great, we can create new record with sensor_value equals to 100.0. what about 100.1 ?

```bash
  curl -X POST -H "Content-Type: application/json" -d \
  '{"sensor_value": 100.1, "sensor_type": "temperature"}' http://localhost:8000/sensors/devices/
```
 Nope ! As you can see if you are using the browser, the server result is as follows:
 ```json
{
    "non_field_errors": [
        "Sensor value cannot be grater than 100.0"
    ]
}
```
### Checking constraint about too many concurrent requests
In the previous example on concurrent requests, we demonstrated how the application can handle concurrent
requests. In this example, we use the same curl request by increasing the number of random records per minute.

```bash
 $  ./virtualenv/bin/python http_client.py -n 62 --url http://localhost:8000/sensors/devices/
```
the preceding command returns a request throttle message after 60 successful requests per minute:

```bash
# As soon as we reache 60 requests per minute, the resource got throttled

{'detail': 'Request was throttled. Expected available in 17 seconds.'}
{'detail': 'Request was throttled. Expected available in 16 seconds.'}
```

### Retrieve sensor data using start_time and end_time
To retrieve data with GET using the starting and ending sensor_reading_time, open the following link on your browser.

[Retrive: http://localhost:8000/sensors/retrieve/](http://localhost:8000/sensors/retrieve/)

Click on Filter button and the following modal will open:
<img src="https://storage.googleapis.com/josue-kula-static/design_abstract/Filter_data.png" />

Type the sensor type, start_time (datetime), end_time (datetime). Use the correct format for datetime as
describe below.

```
 sensor type: temperature
 start_time: 2019-09-11 11:20:02
 end_time: 2019-09-11 11:23:01
```

## App Testing
For this project, I only tested the server side application. I tested urls resolver, Views/
ModelViewSet and data models (entity). To see the test files, find the path below

```bash
  youser@hostname:~$ cd sensorsdev/sensors/tests && ls -lrt
```
## Run test
```bash
   (virualenv)youser@hostname:~$ ./virtualenv/bin/python manage.py test
```
```bash
  ...
  ----------------------------------------------------------------------
  Ran 5 tests in 0.033s
  OK

```
















