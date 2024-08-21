## Usage guides

There are 2 types of backend applications here, one for storing inventory and the other one that handles orders. Both of them support the CRUD operations

To start a **products** service on localhost, use the following Make target that launches the API server on *port 8000* via the target command `@uvicorn api.products:app --reload --port 8000`
```bash
make products
```


To start a **orders** service on localhost, use the following Make target that launches the API server on *port 9000* via the target command `@uvicorn api.orders:app --reload --port 9000`
```bash
make products
```
---

In case you stop these services, but the ports 8000 and 9000 are still blocked, you can use the following to free up the ports:
```bash
make kill
```