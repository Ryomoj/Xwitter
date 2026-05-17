from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI(title="API Gateway")

SERVICES = {
    "Tweets": "http://localhost:8001",
    "Timelines": "http://localhost:8002",
    "Follows": "http://localhost:8003",
    "Media": "http://localhost:8004"
}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(service: str, path: str, request: Request):
    if service not in SERVICES:
        return Response(status_code=404, content="Service not found")

    target_url = f"{SERVICES[service]}/{path}"

    body = await request.body()
    params = dict(request.query_params)
    headers = {k: v for k, v in request.headers.items()
               if k.lower() not in ("host", "content-length")}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                headers=headers,
                params=params,
                timeout=30.0
            )
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=dict(resp.headers)
            )
        except httpx.TimeoutException:
            return Response(status_code=504, content="Gateway Timeout")