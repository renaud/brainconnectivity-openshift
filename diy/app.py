'''
REST endpoint for BR connectivity
for new database format (3 extractors)
'''
from datetime import date
from tornado import ioloop, web, autoreload
import simplejson as json
import pymysql
from pymysql import escape_string
import math, os, codecs
from counter import Counter
from collections import defaultdict
import ABA


# load brainer vocab into dict
vocab_file = 'data/20140522_brainer_entities_idx_2.tsv'
brainer_brs = dict((idx, br.rstrip()) for (idx, br) in enumerate(open(vocab_file).readlines()))
assert len(brainer_brs) > 2000
assert 'hippocampus' in brainer_brs.values()
print 'BraiNER loaded with %s regions' % len(brainer_brs)

dbhost = 'booh'
dbport = '17'


def getMySQLConnection():
    return pymysql.connect(host=dbhost, port=int(dbport), user="nweoinewoincew", passwd="noiwneoicnew", db="20140226_coocs", charset='utf8');


def get_name(id, id_type):
    if id_type == 'aba':
        return ABA.name(id)
    elif id_type == 'brainer':
        return brainer_brs[id]
    else:
        raise Exception("no id_type '%s' " % id_type)

def to_query(rids, id_type):
    return '\'' + '\',\''.join([id_type+':'+rid for rid in rids]) + '\''

''' serves index.html'''
class MainHandler(web.RequestHandler):
    def get(self):
        self.render('static/index.html')


class DetailsHandler(web.RequestHandler):
    QUERY = '''SELECT dt.pubmed_id, dt.snippet, dt.id,
        dt.extr_topdown, dt.extr_kernel, dt.extr_rules, fb.feedback,
        (0.28 * dt.extr_topdown + 0.29 * dt.extr_kernel + 0.43 * dt.extr_rules) AS score
        FROM {0}_data AS dt LEFT JOIN {1}_feedback AS fb ON dt.id = fb.data_id
        WHERE ((e1_entity IN ({2}) AND e2_entity IN ({3})) OR (e1_entity IN ({4}) AND e2_entity IN ({5}) ))
        ORDER BY score DESC'''

    def get(self, db, br1, br2):
        id_type = db.split('_')[1] # aba or brainer
        r1ids, r2ids = br1.split(','), br2.split(',')
        q1, q2 = to_query(r1ids, id_type), to_query(r2ids, id_type)
        br1_names = [get_name(int(rid), id_type) for rid in r1ids]
        br2_names = [get_name(int(rid), id_type) for rid in r2ids]

        conn = getMySQLConnection()
        cur = conn.cursor(pymysql.cursors.DictCursor) # in dictionary mode
        cur.execute(DetailsHandler.QUERY.format(escape_string(db), escape_string(db), q1 , q2, q2, q1))
        coocs = cur.fetchall()

        self.write(json.dumps({"coocs": coocs,
            'br1_names': br1_names, 'br2_names': br2_names}, use_decimal=True))


class FeedbackHandler(web.RequestHandler):
    QUERY = '''INSERT INTO {0}_feedback (data_id, feedback, user, id)
               VALUES (%s, %s, %s, NULL)'''

    def post(self, db, data_id, feedback, user=''):
        conn = getMySQLConnection()
        conn.cursor().execute(FeedbackHandler.QUERY.format(escape_string(db)),\
            (data_id, feedback, user))
        conn.commit()


class MatrixHandler(web.RequestHandler):
    QUERY = 'SELECT count(*) AS cnt, e1_entity AS e1, e2_entity AS e2 FROM {0}_data GROUP BY e1, e2'

    def get(self, db):
        id_type = db.split('_')[1] # aba or brainer
        size = int(self.get_argument('size', 30))
        conn = getMySQLConnection()
        cur = conn.cursor(pymysql.cursors.DictCursor) #in dictionary mode
        cur.execute(MatrixHandler.QUERY.format(escape_string(db)))

        # count all co-occurences
        counter = Counter() # to count mentions of a br
        coocs = defaultdict(lambda : defaultdict(int))
        for c in cur.fetchall():
            cnt = c['cnt']
            frm = int(c['e1'].split(':')[1]) # comes as 'aba:123', 'brainer:123'
            to =  int(c['e2'].split(':')[1])
            counter[frm] +=cnt
            counter[to] +=cnt
            if frm > to: # symetrize
                frm, to = to, frm
            if frm != to:
                coocs[frm][to] += cnt

        # a tuple of top br (aba_id, name)
        top_brs = [(i[0], get_name(i[0], id_type), counter[i[0]]) for i in counter.most_common(size)]

        self.write(json.dumps({"coocs": coocs, "top_brs": top_brs}))


class SearchHandler(web.RequestHandler): # FIXME toooo hardcoded!

    def get(self, query_st):
        query_st = query_st.lower()
        hits = [] #(aba|brainer, db, name, id)
        for id, br in ABA._name.items():
            if query_st in br.lower():
                hits.append(('ABA','20140226_aba', br, id))
        for id, br in brainer_brs.items():
            if query_st in unicode(br, errors='ignore'):
                hits.append(('braiNER','20140522_brainer', br, id))

        # sort by
        self.write(json.dumps(sorted(hits, key=lambda x: len(x[2]))))


class RegionHandler(web.RequestHandler):
    QUERY = '''SELECT count(*) AS cnt, e1_entity AS e1, e2_entity AS e2
        FROM {0}_data WHERE ( e1_entity IN ({1}) OR e2_entity IN ({2}) ) GROUP BY e1, e2'''

    def get(self, db, region_ids_str):
        id_type = db.split('_')[1] # aba or brainer
        rids = region_ids_str.split(',')
        size = int(self.get_argument('size', 30))
        conn = getMySQLConnection()
        cur = conn.cursor(pymysql.cursors.DictCursor) #in dictionary mode
        cur.execute(RegionHandler.QUERY.format(escape_string(db), to_query(rids, id_type), to_query(rids, id_type)))
        # count all co-occurences
        counter = Counter() # to count mentions of a br
        for c in cur.fetchall():
            cnt = c['cnt']
            frm = int(c['e1'].split(':')[1]) # comes as 'aba:123', 'brainer:123'
            to =  int(c['e2'].split(':')[1])
            if frm != to:
                other_region = to if frm in rids else frm
                counter[other_region] += cnt
        for rid in rids:
            del counter[int(rid)]
        # a tuple of top br (aba_id, name)
        top_brs = [(i[0], get_name(i[0], id_type), counter[i[0]]) for i in counter.most_common()]
        br_names = [get_name(int(rid), id_type) for rid in rids]
        self.write(json.dumps({"top_brs": top_brs, 'br': br_names}))


application = web.Application([
    (r'/', MainHandler),
    (r"/(.+)/br/details/([0-9,]+)/([0-9,]+)", DetailsHandler),
    (r"/(.+)/br/feedback/([0-9]+)/([0-9]+)/(.*)", FeedbackHandler),
    (r"/(.+)/br/region/([0-9,]+)", RegionHandler),
    (r"/(.+)/br/matrix/?", MatrixHandler),
    (r"/search/(.+)", SearchHandler),
    (r'/static/(.*)', web.StaticFileHandler, {'path': 'static/'})
],gzip=True)


def main(address, _dbhost, _dbport):
    global dbhost # there must be a better way...
    dbhost = _dbhost
    global dbport
    dbport = _dbport

    application.listen(8080, address)
    #autoreload.start() #TODO remove in prod
    #for dir, _, files in os.walk('static'):
    #    [autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
    print 'server (re)started'#, go visit http://%s:%s' % port
    ioloop.IOLoop.instance().start()


# local debug
if __name__ == "__main__":
    address = "127.0.0.1"
    main(address, 'localhost', '3306')
