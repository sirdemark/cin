import requests
import random
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from cin.web.api.search.feed import FEED_ITEMS

router = APIRouter()


token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCbTFFOC1rekJaTU9iSExjcVlCX2s5cDNVT05ZTDZzaEZ0ZlB2MjlVNXBnIn0.eyJleHAiOjE3MjY3MzcyMjksImlhdCI6MTcyNDE0NTIyOSwianRpIjoiNjg0MGVlMzYtZjRlNS00ZDUzLWE2NjgtOGYwYmUwYzY2MGQ5IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5kZXYtaW50ZXJuYWwucHJlZGljdG8tdGVjaC5ydS9hdXRoL3JlYWxtcy9uYXYtYXBpIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6Ijg2YWFhYWRkLTk3YWYtNDFiNi04NjI4LTUyZTY4ZTUzMDMwZSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImFwaSIsInNlc3Npb25fc3RhdGUiOiJiNTFkYThiZS05MDE1LTQxNWYtYjMyZi1hMzNjMGQ0MDVjMjciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImRlZmF1bHQtcm9sZXMtbmF2LWFwaSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIHNjZW5hcmlvIiwic2lkIjoiYjUxZGE4YmUtOTAxNS00MTVmLWIzMmYtYTMzYzBkNDA1YzI3IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJTZXJnZXkgUGV0dW5pbiIsInByZWZlcnJlZF91c2VybmFtZSI6ImNpbmVtYS1zZWFyY2gtcHJvZCIsImdpdmVuX25hbWUiOiJTZXJnZXkiLCJmYW1pbHlfbmFtZSI6IlBldHVuaW4iLCJlbWFpbCI6InMucGV0dW5pbkBwcmVkaWN0by5ydSJ9.rjpJJ1EMESVPYhwF2QnpqLVwlnbhsNGtXSqxVWJlTbzJ7CwB9CrwLVCRb1YnuXdHE5pfXaER1P1wH1yvcjGlCcu-vzOqXwFdaaaG8dGk_PTTeb8_v4MXLGqeMIB_mFVC7hjC7gSz2i-jINnQJmbcKlYad27L5EAVWpzs8K9LSri9Ynggbeeo_-gYyG3CMJlPZcyVAwxEkueByNBn0hGwuSmNn7mNPBE1mzweqrOr9u5GcIBwTY1wcEz89FntrmgORzFbra07R48EcacIRQt-ih8WFmpLG_8DA4loxH0-gSA2X0fjAiejoYAwd0Klj-1sFbWu8ovKseRq_XsDeqh9xA'
search_url = 'https://search-api-http-prod.rutube.predicto-tech.ru/api/v2/search/'
rutube_url =  'https://rutube.ru/api/video/list/public/'


class SearchQuery(BaseModel):
    query: str


@router.post("/search")
async def search(
    request: Request,
    query: SearchQuery,
) -> JSONResponse:
    host = print(request.headers['host'])
    print(f"Запрос {query.query}")
    try:
        search_response = requests.post(
            url = search_url,
            headers={
                'Authorization': f'Bearer {token}',
            },
            json={

                    "query": query.query,
                    "limit": 5,
                    "scenario": "search.rutube.cinema.online.video.fulltext",
            },
            timeout=5,
        )
    except requests.ReadTimeout:
        print("Таймаут поиска")
        raise HTTPException(status_code=521, detail="search down")

    rutube_uuids = []
    if search_response.status_code == 200:
        payload = search_response.json()['payload']
        for item in payload:
            rutube_uuids.append(item['content_id'])
    

    try:
        rutube_response = requests.get(
            url=rutube_url,
            params={
                'id_list': ','.join(rutube_uuids),
            },
            headers={
                "Content-Type": "application/json"
            }
        )
    except requests.ReadTimeout:
        print("Таймаут обогащения")
        raise HTTPException(status_code=521, detail="data down")
    
    headers = {
        'Access-Control-Allow-Origin': host
    }
    return JSONResponse(headers=headers,content=jsonable_encoder(rutube_response.json()))


@router.get("/feed")
async def search(
    request: Request,
) -> JSONResponse:
    host = print(request.headers['host'])
    number_of_items = 5
    if len(FEED_ITEMS) < number_of_items:
        number_of_items = len(FEED_ITEMS)

    list_of_random_items = random.sample(FEED_ITEMS, number_of_items)
    headers = {
        'Access-Control-Allow-Origin': host
    }
    return JSONResponse(headers=headers, content=jsonable_encoder(list_of_random_items))
