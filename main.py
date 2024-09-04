from flask import Flask, request, abort

from api import search, get_resolutions, retrieve_games, GetAppInfo

app = Flask(__name__)

@app.route("/search/")
def _search():

    query = request.args.get("q")
    if not query: abort(422)
    results = search(query)

    body = {}

    if results.results:
        body["results"] = results.results
    if results.current_page:
        body["current_page"] = results.current_page
    if results.next_page:
        body["next_page"] = results.next_page
    if results.last_page:
        body["last_page"] = results.last_page

    return body

@app.route("/retrieve_games/")
def _retrieve_games():
    
    link = request.args.get("link")
    if not link: abort(422)
    results = retrieve_games(link)

    return {
        "results": results.results,
        "current_page": results.current_page,
        "next_page": results.next_page,
        "last_page": results.last_page
    }

@app.route("/get_app_info/")
def _get_app_info():

    link = request.args.get("link")
    if not link: abort(422)
    
    info = GetAppInfo(link)

    return {
        "splash": info.splash,
        "screenshots": info.screenshots,
        "title": info.title,
        "date": info.date,
        "counter": info.counter,
        "vendor": info.vendor,
        "description": info.description,
        "download_links": info.download_links
    }

@app.route("/get_resolutions/")
def _get_resolutions():

    link = request.args.get("link")
    if not link: abort(422)

    resolutions = get_resolutions(link)

    return resolutions

if __name__ == "__main__":
    app.run(debug=True, port=7080)