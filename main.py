import ast
from typing import List
import requests
import os
import argparse
from google.cloud import storage


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
CRED_PATH = os.path.join(ABS_PATH, "credentials/google_cloud_key.json")
CURRENT_FILE_NAME = os.path.join(os.getcwd(), 'data.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CRED_PATH

storage_client = storage.Client()


# Create new bucket
bucket_name = "js_data_buckets"  # this bucket name used for download file
# bucket = storage_client.bucket(bucket_name)
# bucket.location = "US"
# storage_client.create_bucket(bucket)
blob_name = "data.json"


def bucket_access(buc_name):
    # access to bucket
    my_bucket = storage_client.get_bucket(bucket_name)
    return my_bucket


def download_file_from_bucket(bl_name, file_path, buc_name):
    try:
        bucket_acc = bucket_access(bucket_name)
        blob = bucket_acc.blob(bl_name)
        with open(file_path, "wb") as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except Exception as e:
        print(e)
        return False


def get_ancestors_list(resurs_id, data):
    res_one = None
    folder = resurs_id.split("/")[-1]
    for resurs in data:
        if resurs_id in resurs["name"]:
            res_one = resurs
    ancestor = None
    for anc in res_one["ancestors"]:
        if folder == anc.split("/")[-1]:
            ancestor = anc
    result = ancestor.split('/')[::-1]
    return result


def get_resources_list(un_id, data):
    res_list = []
    for resurs in data:
        results = {
            "ancestors": []
        }
        for members in resurs["iam_policy"]["bindings"]:
            for member in members["members"]:
                if un_id == member.split(":")[-1]:

                    results.update({
                        "role": members["role"],
                        "asset_type": resurs["asset_type"],
                        "name": resurs["name"]

                    })
                    for ancestor in resurs["ancestors"]:
                        results["ancestors"].append(ancestor.split("/")[::-1])
                        res_list.append(results)
    return res_list


def get_members(un_id, data):
    result = []
    for resurs in data:
        if un_id == resurs["name"]:
            for members in resurs["iam_policy"]["bindings"]:
                for member in members["members"]:
                    result.append({
                        "name": resurs["name"],
                        "role": members["role"],
                        "members": member
                    })
    return result




def main():
    download_file_from_bucket(blob_name, CURRENT_FILE_NAME, bucket_name)
    string_data = []
    with open(CURRENT_FILE_NAME, 'r') as f:
        string_data = f.read().splitlines()
    list_data = [ast.literal_eval(data) for data in string_data]
    if args.ancestors:
        list_ancestors = get_ancestors_list(args.ancestors, list_data)
        print(list_ancestors)
    elif args.members:
        list_resources = get_resources_list(args.members, list_data)
        print(list_resources)
    elif args.resources:
        list_members = get_members(args.resources, list_data)
        print(list_members)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--ancestors", dest="ancestors", help="write resource id", type=str)
    parser.add_argument("-m", "--members", dest="members", help="write resource id", type=str)
    parser.add_argument("-r", "--resources", dest="resources", help="write member id", type=str)
    args = parser.parse_args()
    main()
