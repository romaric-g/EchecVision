from cefpython3 import cefpython as cef
import platform
import sys
import os


def main():
    # Configure Cefpython
    sys.excepthook = cef.ExceptHook
    settings = {
        "context_menu": {"enabled": True},
        "remote_debugging_port": 0,
        "browser_subprocess_path": "%s/%s" % (cef.__file__, "../subprocess")
    }
    cef.Initialize(settings)
    # Load React application
    html_path = os.path.abspath(
        "c:\\Users\\Romaric\\DataScience\\EchecsVision\\echec_vision\\chess-vision-web\\dist\\index.html")
    url = "file://%s" % html_path
    browser = cef.CreateBrowserSync(url="url", window_title="React App", settings={
                                    "file_access_from_file_urls_allowed": True,
                                    'universal_access_from_file_urls_allowed': True,
                                    'web_security_disabled': True
                                    })

    # Run Cefpython message loop
    cef.MessageLoop()

    # Shutdown Cefpython
    cef.Shutdown()


if __name__ == '__main__':
    main()
