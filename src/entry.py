from workers import WorkerEntrypoint, Response
from hello import hello

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response(hello("world"))
