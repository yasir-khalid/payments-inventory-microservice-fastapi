# Experimenting-with-FastAPI
Building CRUD operations using FastAPI, establishing links to NoSQL and SQL databases and providing authorized endpoints for end users

---
### Setup Environment
First we need to create a virtual environment for the code to operate in successfully with the 
right dependencies and python version. Got to your command line and run the following commands
```commandline
python3.10 -m venv venv
```
Now it's time to activate the virtual environment to so we can install libs inside of it

- For linux users:
```commandline
source venv/Scripts/activate
```
- For windows users (command line or powershell)
```
.\venv\Scripts\activate.bat
```

---

### Code Guide
> FastAPI runs through the code top to bottom and prioritses API logic based
on the function that appears first

`PATH PARAMETER` If the params is part of the endpoint, and it's passed into the function:


If the params is not part of the endpoint, and it's passed into the function:
- Is it a primtive type i.e. str, int, bool etc: `QUERY PARAMETER`
- Is it of type Pydantic BaseModel: `REQUEST BODY`

> Ideally any `required` params should be path params

Behind the scenes, APIs often need to manipulate data as part of their operation. 
Typically, these data operations—called CRUD for short—run against backend databases

| CRUD   | HTTP Methods |
|--------|--------------|
| Create | POST         |
| Read   | GET          |
| Update | PUT          |
| Delete | DELETE       |

---

## Usage guides
To launch the server, use this command and will automatically reload when you make changes to 
the code
```commandline
uvicorn api.main:app --reload
```