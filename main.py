from website import create_app


"""
Файл с которого запускается сайт
"""


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50100, debug=True)
    