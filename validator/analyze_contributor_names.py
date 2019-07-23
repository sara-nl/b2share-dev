# generate fake DOIs for records without DOIS
import json
from argparse import ArgumentParser
from pprint import pprint
import psycopg2
from psycopg2.extras import Json


def pid_has_doi(pid):
    for rec in pid:
        if rec['type'] == 'DOI':
            return True
    return False


def get_b2rec_value(pid):
    pid_dict = {r['type']: r['value']
                for r in pid}
    if 'b2rec' in pid_dict:
        return pid_dict['b2rec']
    else:
        return None


descr = 'Add fake DOIs to data set.'
parser = ArgumentParser(description=descr)
parser.add_argument('--dbname', type=str, help='dbname', default="b2share")
parser.add_argument('--user', type=str, help='dbuser', default="b2share")
parser.add_argument('--password', type=str, help='dbpassword', default="b2share")
parser.add_argument('--host', type=str, help='dbpassword', default="127.0.0.1")
parser.add_argument('--dryrun', action="store_true")
args = parser.parse_args()
conn = psycopg2.connect(dbname=args.dbname,
                        user=args.user,
                        password=args.password,
                        host=args.host)

SELECT_SQL = "SELECT created, updated, id, json, version_id from records_metadata"
UPDATE_SQL = "UPDATE records_metadata SET json = %s WHERE id = %s AND version_id = %s"

with conn.cursor() as cur:
    with conn.cursor() as cur2:
        cur.execute(SELECT_SQL)
        for rec in cur:
            md = rec[3]
            if md is not None:
                contributors = [item['creator_name']
                                for item in md.get('creators', [])]
                contributors += [item['contributor_name']
                                 for item in md.get('contributors', [])]
                pprint(contributors)
                # b2rec_value = get_b2rec_value(md['_pid'])
                # if not pid_has_doi(md['_pid']) and b2rec_value:
                #    doi_value = {
                #        'type': 'DOI',
                #        'value': '10.23728/b2share.{0}'.format(b2rec_value)}
                #    md['_pid'].append(doi_value)
                #    pprint(doi_value)
                #    pprint(md)
                #    if not args.dryrun:
                #        cur2.execute(UPDATE_SQL, 
                #                     (Json(md), rec[2], rec[4]))
# if not args.dryrun:                        
#    conn.commit()
