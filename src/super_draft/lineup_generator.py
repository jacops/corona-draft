import asyncio
from jinja2 import Template
from pyppeteer import launch


async def generate_png(source_path: str, output_path: str) -> None:
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto("file://" + source_path)
    await page.screenshot({'path': output_path, 'clip': {
        "x": 0,
        "y": 0,
        "width": 935,
        "height": 720
    }})
    await browser.close()


class LineUpGenerator:
    def __init__(self, team_name: str, players_grid):
        self.team_name = team_name
        self.players_grid = players_grid

    def generate(self, output_path: str) -> None:
        html_file_path = output_path + "/lineup.html"
        with open('templates/team_grid.html') as f:
            html_file = open(html_file_path, "wt")
            template = Template(f.read())

        html_file.write(template.render(grid=self.players_grid.values()))
        html_file.close()

        asyncio.get_event_loop().run_until_complete(
            generate_png(html_file_path, output_path + "/lineup.png")
        )
