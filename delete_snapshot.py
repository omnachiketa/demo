#!/usr/bin/python3

import boto3
import argparse
import datetime
import sys
'''
To run this scripet you need to pass these arguments in this oder
 script_name.py <retention_days> <cluster/db-identifier> <access_key> <access_secret> <aws-region>
''' 

parser = argparse.ArgumentParser(description='This will delete the DB/Cluster\'s snapshots identified by the identifier, olded than given days.\
 Please pass the AWS key/ID and no_of_days for retention and region with the DB/Cluster identifier. If want to dryrun, pass --dryrun')
parser.add_argument('-id', '--aws_id', metavar='', required=True, help="aws access key id from IAM with RDS full access")
parser.add_argument('-key', '--aws_key', metavar='', required=True, help="aws access key secret from IAM with RDS full access")
parser.add_argument('-r', '--region', metavar='', required=True, help="AWS region name")
parser.add_argument('-n', '--number', metavar='', required=True, help="The number of days the snapshot will be retained")
parser.add_argument('-d', '--dryrun', metavar='', help="To only list the DB/Cluster snapshot to be deleted")
parser.add_argument('-i', '--identifier', metavar='', required=True, help="DB/Cluster identifier")
args = parser.parse_args()

today = datetime.datetime.now()
delta_days = datetime.timedelta(days = int(args.number))
retention_days = (today - delta_days).date()

client = boto3.client('rds', aws_access_key_id=args.aws_id, aws_secret_access_key=args.aws_key, region_name=args.region)

def find_snapshot():
    res = client.describe_db_snapshots(DBInstanceIdentifier=str(args.identifier))
    res1 = client.describe_db_cluster_snapshots(DBClusterIdentifier = str(args.identifier))
    #print(res)
    #print(res1)
    if len(res['DBSnapshots']) > 0:
        for snapshot in res['DBSnapshots']:
            if (snapshot['DBInstanceIdentifier'] == str(args.identifier)):
                if ((snapshot['SnapshotCreateTime'].date()) < retention_days):
                    print(snapshot['DBSnapshotIdentifier'], snapshot['SnapshotType'])
                    delete_snapshot(snapshot['DBSnapshotIdentifier'])
                else:
                    pass
                    #print("couldn't find DB snapshot", args.identifier)
    else:
        print("you have passed a DBClusterIdentifier or an Invalid entry")
    if len(res1['DBClusterSnapshots']) > 0:
        for snapshot in res1['DBClusterSnapshots']:
            if (snapshot['DBClusterIdentifier'] == str(args.identifier)):
                if ((snapshot['SnapshotCreateTime'].date()) < retention_days):
                    print(snapshot['DBClusterSnapshotIdentifier'], snapshot['SnapshotType'])
                    delete_snapshot(snapshot['DBClusterSnapshotIdentifier'])
                else:
                    pass
                    #print("couldn't find DB cluster snapshot", args.identifier)
    else:
        print("you have passed a DBInstanceIdentifier or an Invalid entry")


def delete_snapshot(snapshot_id):
    print("deleteing snapshot:", snapshot_id)
    if args.dryrun == "dryrun":
        return
    else:
        print("deleting", snapshot_id)
        #response = client.delete_db_snapshot(DBSnapshotIdentifier = snapshot_id)

def main():
    try:
        find_snapshot()
    except Exceprion as e:
        print("An error occurred while deleting the snapshot see the full logs")
        print(e)

if __name__ == "__main__":
    main()
