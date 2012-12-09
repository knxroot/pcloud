import cgi
import os
import random
import sys
import wsgiref.handlers

import webapp2
from google.appengine.ext import db
import pygments

from pygments import lexers
from pygments import highlight
from pygments.formatters import HtmlFormatter

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class Portapapel(db.Model):
    name = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class Index(webapp2.RequestHandler):

    u = '127.0.0.1:8080'
    r = 'portapapel'

    def help(self, u, r):
        f = 'data:text/html,<form action="%s" method="POST"><textarea name="%s" cols="80" rows="24"></textarea><br><button type="submit">%s</button></form>' % (u, r, r)
        return """
<style> a { text-decoration: none } </style>
<pre>
127.0.0.1:8080(1)                          127.0.0.1:8080                         127.0.0.1:8080(1)

NAME
    portapapel: command line pastebin.

SYNOPSIS
    &lt;command&gt; | curl -F '%s=&lt;-' %s

DESCRIPTION
    add <a href='http://pygments.org/docs/lexers/'>?&lt;lang&gt;</a> to resulting url for line numbers and syntax highlighting
    use <a href='%s'>this form</a> to paste from a browser

EXAMPLES
    ~$ cat bin/ching | curl -F '%s=&lt;-' %s
       %s/VZiY
    ~$ firefox %s/VZiY?py#n-7

SEE ALSO
    http://lacosox.org

</pre>""" % (r, u, f, r, u, u, u)

    def new_id(self):
        nid = ''
        symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        while len(nid) < 4:
            n = random.randint(0,35)
            nid = nid + symbols[n:n+1]
        return nid

    def get(self, got):
        if not got:
            self.response.out.write(self.help(self.u, self.r))
            return

        c = Portapapel.gql('WHERE name = :1', got).get()
        if not c:
            self.response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
            self.response.out.write(got + ' not found')
            return

        syntax = self.request.query_string
        if not syntax:
            self.response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
            self.response.out.write(c.content + '\n')
            return
        try:
            lexer = pygments.lexers.get_lexer_by_name(syntax)
        except:
            lexer = pygments.lexers.TextLexer()
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.out.write(highlight(c.content,
                                          lexer,
                                          HtmlFormatter(full=True,
                                          style='borland',
                                          lineanchors='n',
                                          linenos='inline',
                                          encoding='utf-8')))

    def post(self, got):
        self.response.headers['Content-Type'] = 'text/plain'
        got = self.request.query_string
        if self.request.get(self.r):
            nid = self.new_id()
            while Portapapel.gql('WHERE name = :1', nid).get():
                nid = self.new_id()
            s = Portapapel()
            s.content = self.request.get(self.r)
            s.name = nid

            # delete the oldest sprunge
            old = Portapapel.gql('ORDER BY date ASC LIMIT 1').get()
            if old:
                old.delete()

            s.put()
            self.response.out.write(' ' + self.u + '/' + nid + '\n')

def main():
    app = webapp2.WSGIApplication([(r'/(.*)', Index)],debug=False)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
