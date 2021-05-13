# -*- coding: utf-8 -*-
"""
Created on Tue May 02 22:16:19 2017
@author: vic
"""

from imgurpython import ImgurClient


def upload_photo(image_path):
    client_id = 'cbb37018d97bb2e'
    client_secret = 'e294e00c4ee0e2fcd5f8a545baf2113516188c28'
    access_token = 'f90853c389e52aff4a02a39216cd72f8ed5a20e4'
    refresh_token = '0080a377bdd2e45e6ed6050bdfd476931068672e'
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    album = None # You can also enter an album ID here
    config = {
        'album': album,
    }

    print("Uploading image... ")
    image = client.upload_from_path(image_path, config=config, anon=False)
    print("Done")    
    return image['link']

def deleteImage(image_id):
    client_id = 'cbb37018d97bb2e'
    client_secret = 'e294e00c4ee0e2fcd5f8a545baf2113516188c28'
    access_token = 'f90853c389e52aff4a02a39216cd72f8ed5a20e4'
    refresh_token = '0080a377bdd2e45e6ed6050bdfd476931068672e'
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    album = None # You can also enter an album ID here
    config = {
        'album': album,
    }

    print("deleting image... ")
    image = client.delete_image(image_id)
    print("Done")