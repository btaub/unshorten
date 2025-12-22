#!/usr/bin/env python3

from flask import Flask, request, make_response
import unshorten

application = Flask(__name__)

# The index route.
@application.route('/', methods=['GET', 'HEAD'])
def index():
    try:
        url = request.args.get('link')
        print(f"URL: {url}\n")
        if url:
            res = unshorten.unshorten(url)
        # empty link paramater or value, show usage
        if not url:
            res = 'No url provided. Pass a url in using the link parameter: \n\n'\
                 f'example: {request.url.split("?")[0]}?link=git.io/h'

    except Exception as e:
        print(f"Bad link, exception: {e}")
        res = make_response('bad_link',404)
        res.headers['Content-type'] = 'text/plain'
        return(res)

    res = make_response(res)
    res.headers['Content-type'] = 'text/plain'
    return(res)


# Run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()
