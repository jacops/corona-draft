import pickle
import markdown
from jinja2 import Template
from pyppeteer import launch
from google_auth_oauthlib.flow import InstalledAppFlow


POSITIONS_ORDER = [
    ["LW", "LF", "FW", "ST", "CF", "RF", "RW"],
    ["LM", "MF", "AM", "CM", "RM"],
    ["LWB", "DM", "RWB"],
    ["LB", "CBL", "CB", "SW", "CBR", "RB"],
    ["GK"]
]


def generate_token_pickle(credentials_path: str, token_pickle_path: str) -> None:
    print(credentials_path)
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, ['https://www.googleapis.com/auth/spreadsheets.readonly'])
    credentials = flow.run_local_server(port=0)
    with open(token_pickle_path, 'wb') as token:
        pickle.dump(credentials, token)


def get_list_value(list, index, default = None):
    return list[index] if index < len(list) else default


def get_line_by_position(position: str) -> int:
    for line_number, line in enumerate(POSITIONS_ORDER):
        for line_position in line:
            if line_position == position:
                return line_number
    raise Exception("Unknown position: {}".format(position))


async def generate_png(source_path: str, output_path: str, clip: dict = None) -> None:
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto("file://" + source_path)
    await page.screenshot({'path': output_path, "fullPage": True, 'clip': clip})
    await browser.close()


def generate_html_from_markdown(content: str, output_path: str) -> None:
    md = markdown.Markdown()
    with open('templates/rules.html') as f:
        with  open(output_path, "wt") as html_file:
            template = Template(f.read())
            html_file.write(template.render(rules=md.convert(content)))
