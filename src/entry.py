from workers import WorkerEntrypoint, Response
from hello import hello

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # name = (await request.json()).name
        if request.method != "POST":
            return Response("Method not allowed", status=405)
        if request.headers.get("Content-Type") != "application/json":
            return Response("Content-Type must be application/json", status=400)
        body=await request.json()
        name=body.get("name")
        if not name:
            return Response("Missing 'name' in JSON body", status=400)
        name2=self.env.API_HOST
        if not name2:
            return Response("Missing 'name2' in variable", status=400)
        name =name + name2
        return Response(hello(name))
