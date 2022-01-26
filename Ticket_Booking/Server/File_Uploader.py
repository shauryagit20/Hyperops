import os
import cloudinary
import cloudinary.uploader

upload_file_list = [r"Sample_Ticket.png"]
cloudinary.config(
  cloud_name = "dr0ppt3js",
  api_key = "375687298325763",
  api_secret = "fYEeiW9x5PRGFZtr5MV26yqUra0"
)
def upload_files(file_name,uid):
    file_name_2 =  "_".join(file_name.split(" "))
    cloudinary.uploader.upload(file_name,public_id = f"{str(uid)}_{file_name_2}")
