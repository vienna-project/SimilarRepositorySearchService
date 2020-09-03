## Similar Repository Search Service

Annoy Index Serving Server For Searching Similar github repository


**Installation**

````bash
pip install -r requirements.txt
````

**Launch Server**

It takes about 1 minute to launch. Choose between two web servers, `inbuilt` and `gunicorn`.

* inbuilt webserver

    ````bash
    sanic service.server.app --host=0.0.0.0 --port=8000
    ````

* with `gunicorn`

    ````bash
    gunicorn service.server:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
    ````

**Client-side**

Currently, only Similar Search for a single repository are possible.

* **python scripts**
    
    ````python
    import requests
    
    res = requests.get("http://localhost:8000/repository",
                       params={"repo_id":7960131, 
                               'nums':5, 
                               'include_scores':True})
    
    print(res.json())
    # {'repos': ['153086880', '15994976', '36145699', '7960131', '31845198'], 
    #  'scores': [5.4246134757995605, 5.268659591674805, 5.265341758728027, 5.189166069030762, 5.081940174102783]}
    ````
    
* **curl**

    ````bash
    curl http://localhost:8000/repository\?repo_id\=7960131
    ````
    
    
**API Specification**

* `Search Repository`
    
    * URL
    
    | method | URL | response  |
    | ----   |  ----   | ----     |
    | GET    | /repository | json | 
    
    * Parameter
    
    | parameter | type | is_required | default |
    | ---- | --- | ---- | ---- |
    | repo_id | int | Y | - |
    | nums | int | N | 10 |
    | include_scores | bool | N | False |    