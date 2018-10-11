import GenerateApk


def main():
    print(response())
    GenerateApk.RunGenerateAPK().run()
    

def response():
    html = 'Content-type:text/html\r\n\r\n'
    html += '<html>'
    html += '<head><title>APK Creator</title></head>'
    html += '<body>'
    html += '<span>Creating The Apk</span>'
    html += '</body>'
    html += '</html>'
    return html

main()
