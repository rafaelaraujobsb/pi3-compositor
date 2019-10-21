import sys

from compositor import criar_app


app = criar_app()
app.run(host='0.0.0.0', port=sys.argv[1], debug=eval(sys.argv[2]))
