import requests
# print("@@@@@ Document Mode @@@@@")
# filename = "recipt.jpg"
# files = {"file":('recipt.jpg', open("recipt.jpg", 'rb'))}
# print(files)
# # response = requests.post(
# # 	'http://127.0.0.1:8000/document_mode/images',
# # 	files = files,
# # 	)

# # print(response.json())
session = requests.session()
print("#########")
print("@@@@@ Simple  Mode @@@@@")

filename = "recipt.jpg"    

files = {"file":('recipt.jpg', open("recipt.jpg", 'rb'))}
print(files)
headers = {}
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
user = {
        "email":"onanugaoreoluwa@outlook.com",
        "password":"oreoluwa"
}
# response = requests.post(
#         'http://127.0.0.1:8000/abstract_mode/images/',
#         files = files, auth = basic
#         )
response = session.post(
         'http://127.0.0.1:8000/signup/', headers=headers, json=user
        )
response_dict = response.json()
print(response.json())
access_token = response_dict['access_token']
print(access_token)
print("#########")
print("@@@@@ Currency  @@@@@")

filename = "recipt-10.jpg"
files = {"file":('recipt-10.jpg', open("recipt-10.jpg", 'rb'))}
print(files)
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers['Authorization']= f"Bearer {access_token}"
response = session.post(
        'http://127.0.0.1:8000/currency/images/',headers=headers,files = files
        )

print(response.json())

# print("#########")
# print("@@@@@  FaceReco  @@@@@")

# filename = "recipt-ananth_detect.jpg"
# files = {"file":('recipt-ananth_detect.jpg', open("recipt-ananth_detect.jpg", 'rb'))}
# print(files)


# response = requests.post(
#         'http://127.0.0.1:8000/facereco/images/',
#         files = files,
#         )

# print(response.json())

# print("#########")
# print("@@@@@  Focus_mode  @@@@@")

# filename = "everydayobject_test11.mp4"
# files = {"file":('everydayobject_test11.mp4', open("everydayobject_test11.mp4", 'rb'))}
# print(files)


# response = requests.post(
#         'http://127.0.0.1:8000/focus/video/',
#         files = files,
#         )
# for i in response:
#         print(i)
        
