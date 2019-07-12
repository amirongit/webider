from requests import get
import domainlib, datalib

def random_surf(conn, proxy):

    """generates random domains using the domainlib,
    checks if it's ok (can you access to the web page or not!),
    and then, inserts it to the database."""

    cursor = conn.cursor()
    while True:
        tmp = domainlib.generate('com', 'ir', 'org', 'info', 'io', 'pro')
        print(tmp)
        try:
            res = get(tmp, proxies=proxy)
            if res.ok == True:
                datalib.write(tmp, cursor)
                conn.commit()
        except:
            pass

def surf_the_data(conn):

    """reads the last 10 domians in the database and
    looks them for new domains!"""

    cursor = conn.cursor()
    tmp = datalib.read(cursor)

    for i in tmp:
        res = get(i)
        urls = domainlib.surf(res.text)
        for j in urls:
            datalib.write(j, cursor)
        conn.commit()


def collect(html_str, conn):

    """inserts the gained domains of a html web page to
    data base!"""

    tmp = domainlib.surf(html_str)
    cursor = conn.cursor()

    for i in tmp: datalib.write(i, cursor)
    conn.commit()