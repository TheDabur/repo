from os import path
from xbmc import translatePath
from control import log
from contextlib import contextmanager
import sqlite3

DB_DIR = translatePath("special://profile/Database")
DB_FILE = path.join(DB_DIR, 'Addons27.db')


@contextmanager
def open_db(file=DB_FILE):
    if not path.exists(file):
        open(file, 'w').close()
    for i in range(10):
        try:
            CONN = sqlite3.connect(file)
            break
        except:
            log('Failed to open DB')
            time.sleep(1)
    if not CONN:
        raise Exception('DB is locked')
    CONN.row_factory = sqlite3.Row
    DB = CONN.cursor()
    yield DB
    CONN.commit()
    DB.close()
    CONN.close()


def set_enabled(addons, value=True):
    with open_db() as db:
        log("{0} {1} addons {2}".format('Enabling' if value else 'Disabling', len(addons), str(addons)))
        cur = db.executemany('UPDATE installed SET enabled={0} WHERE addonID=(?)'.format(int(value)),
                             ((id,) for id in addons))
        log("updated {0} rows".format(cur.rowcount))


def remove_addons(addons):
    with open_db() as db:
        log("Removing {0} addons {1}".format(len(addons), str(addons)))
        cur = db.executemany('DELETE FROM installed WHERE addonID=(?)', ((id,) for id in addons))
        log("removed {0} rows".format(cur.rowcount))
