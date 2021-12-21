#!/usr/bin/python3

import boto3
import argparse
import datetime
import sys
'''
To run this scripet you need to pass these arguments in this oder
 script_name.py <retention_days> <cluster/db-identifier> <access_key> <access_secret> <aws-region>
''' 

input_info = sys.argv
data = {
    "account_info": {
        "no_of_days": input_info[1], 
        "ID": input_info[3],
        "Secret": input_info[4],
        "region_name": input_info[5]
        }
}
today = datetime.datetime.now()
delta_days = datetime.timedelta(days = int(sys.argv[1]))
retention_days = (today - delta_days).date()
describe_db_cluster_snapshots = sys.argv[2]

client = boto3.client('rds', aws_access_key_id=data['account_info']['ID'], aws_secret_access_key=data['account_info']['Secret'], region_name=data['account_info']['region_name'])

def find_snapshot():
    res = client.describe_db_snapshots()
    res1 = client.describe_db_cluster_snapshots()
    #print(res)
    #print(res1)
    for snapshot in res['DBSnapshots']:
        if (snapshot['DBInstanceIdentifier'] == sys.argv[2]):
            if ((snapshot['SnapshotCreateTime'].date()) < retention_days):
                print(snapshot['DBSnapshotIdentifier'], snapshot['SnapshotType'])
                delete_snapshot(snapshot['DBSnapshotIdentifier'])
                return
            else:
                pass
                #print("couldn't find DB snapshot", sys.argv[2])
    print("---------------------------------------")
    for snapshot in res1['DBClusterSnapshots']:
        if (snapshot['DBClusterIdentifier'] == str(sys.argv[2])):
            if ((snapshot['SnapshotCreateTime'].date()) < retention_days):
                print(snapshot['DBClusterSnapshotIdentifier'], snapshot['SnapshotType'])
                delete_snapshot(snapshot['DBClusterSnapshotIdentifier'])
            else:
                pass
                #print("couldn't find DB cluster snapshot", sys.argv[2])
                

def delete_snapshot(snapshot_id):
    print("deleteing snapshot:", snapshot_id)
    #response = client.delete_db_snapshot(DBSnapshotIdentifier = snapshot_id)

def main():
    try:
        find_snapshot()
    except:
        print("An error occurred while deleting the snapshot see the full logs")
    
if __name__ == "__main__":
    main()
