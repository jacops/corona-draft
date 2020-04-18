import asyncio
from jinja2 import Template
from pyppeteer import launch
from .models import Team


async def _generate_png(source_path: str, output_path: str) -> None:
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


def generate_lineup(team: Team, output_path: str) -> str:
    html_file_path = output_path + "/lineup.html"
    with open('templates/team_grid.html') as f:
        html_file = open(html_file_path, "wt")
        template = Template(f.read())

    html_file.write(template.render(grid=team.get_grid().values()))
    html_file.close()

    asyncio.get_event_loop().run_until_complete(
        _generate_png(html_file_path, output_path + "/lineup.png")
    )

    return output_path + "/lineup.png"
