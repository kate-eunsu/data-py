#%%
import requests
# https://apick.app/rest/

# https://apick.app/rest/iros/1
CL_AUTH_KEY = "419ddf2dc433fc49fd7d27c77191dff0"

headers = {
  "CL_AUTH_KEY": CL_AUTH_KEY,
}

# FormData
files = {
  "address": (None, "서울특별시 종로구 종로63다길 5"),
}

response = requests.post("https://apick.app/rest/iros/1", headers=headers, files=files)
print(response.json())
# %%
# {'data': {'ic_id': 3042146, 'success': 1}, 'api': {'success': True, 'cost': 900, 'ms': 15056, 'pl_id': 10975604}}
ic_id = response.json()["data"]["ic_id"]
files = {
  "ic_id": (None, str(ic_id)),
}

response2 = requests.post("https://apick.app/rest/iros_download/1", headers=headers, files=files)
print(response2.json())
# %%
with open("downloaded_file.pdf", "wb") as f:
    f.write(response2.content)
# %%
