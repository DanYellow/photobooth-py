import http.server
import socketserver
import threading
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class WebGallery:
    def generate_gallery(self, photos_list):
        os.chdir(f"{self.root_dir}/_tmp")

        f = open('index.html','w')

        images_tpl = []
        for image in photos_list:
            images_tpl.append(f"""
                <li>
                    <a href="full/{image}">
                        <figure>
                            <img src="./{image}" />
                        </figure>
                    </a>
                </li>
            """)
        
        html_tpl = f"""
            <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Photomaton</title>
                    <link rel="stylesheet" type="text/css" href="reset.css">
                    <style>
                        body {{
                            padding: 0 2%;
                        }}
                        ul {{
                            display: grid;
                            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                            grid-gap: 0.25em;
                            margin: 0 auto;
                        }}

                        @media only screen and (max-width: 600px) {{
                            ul {{
                                display: grid;
                                grid-template-columns: repeat(auto-fill, minmax(33%, 1fr));
                                grid-gap: 0.25em;
                                margin: 0 auto;
                            }}
                        }}

                        img {{
                            display: block;
                            max-width: 100%;
                        }}

                        figure {{
                            height: 150px;
                            overflow: hidden;
                        }}
                    </style>
                </head>
                <body>
                    <ul>{''.join(images_tpl)}</ul>
                </body>
            </html>
        """

        f.write(html_tpl)
        f.close()

        print("---- Gallery server: regenerated")
        
        return 0

    def start_server(self):
        os.chdir(f"{self.root_dir}/_tmp")

        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("---- Gallery server: serving at port", PORT)
            httpd.serve_forever()

        return 0

    def __init__(self, root_dir = ROOT_DIR):
        self.root_dir = root_dir
        threading.Thread(target=self.start_server).start()

        