#!/usr/bin/python

import sqlite3, pyqrcode, urllib, sys, os

def readDB(dbfile):
    try:
        db = sqlite3.connect(dbfile)
        cursor = db.cursor()
        cursor.execute('SELECT email, secret, issuer, original_name FROM accounts')
        rows = cursor.fetchall()
        return rows
    
    except Exception as err:
        print('There was an error reading the database: {}'.format(err))

    finally:
        db.close()


def main(args):
    if len(args) == 1:
        print('Usage: {} <database_file>'.format(args[0]))
        sys.exit(1)
    db = args[1]
    if not os.path.isfile(db):
        print('Error. File "{}" does not exist'.format(db))
        sys.exit(1)
    accts = readDB(db)
    url = 'otpauth://totp/{}?secret={}&issuer={}'
    try:
        if accts:
            print('Generating otpauth urls and QRcodes...\n')
            for r in accts: # 0: email, 1: secret, 2: issuer, 3: original_name
                email = urllib.quote(r[0]) if r[0] else 'Unknown'
                secret = urllib.quote(r[1]) if r[1] else 'Unknown'
                issuer = urllib.quote(r[2]) if r[2] else 'Unknown'
                otpauth = url.format(email, secret, issuer)
                print('otpauth url: {}'.format(otpauth))
                qr = pyqrcode.create(otpauth, error='L')
                print(qr.terminal(quiet_zone=1))
                raw_input('Press ENTER to continue...\n\n')
        else:
            print('No data found in database file "{}"'.format(db))
    except Exception as err:
        print('There was an error generating the QR codes: {}'.format(err))


if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print "\nBye!"
        sys.exit()