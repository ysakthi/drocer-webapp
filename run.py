# run development server
if __name__ == '__main__':
    from app import wsgi_app # defined in app/__init__.py
    # >>> int('cle'.encode('hex'), 16)
    # 6515813
    wsgi_app.run(debug=True, host='127.65.158.13', port=3000)
