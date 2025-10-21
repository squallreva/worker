from workers import WorkerEntrypoint, Response
from hello import hello

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # name = (await request.json()).name
        if request.method != "POST":
            return Response("Method not allowed", status=405)
        if request.headers.get("Content-Type") != "application/json":
            return Response("Content-Type must be application/json", status=400)
        body=request.json()
        name=body.get("name")
        return Response(hello(name))
