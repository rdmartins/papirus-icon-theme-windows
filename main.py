import os
import subprocess
from pathlib import Path
from tqdm import tqdm
from typing import Dict, List

class IconTemplate:
    def __init__(self, name: str, category: str, svgs: List[str] = list()):
        self.name = name
        self.category = category
        self.svgs = svgs

    def add_svg(self, filepath: str):
        self.svgs.append(filepath)


def create_template_list(theme: str) -> Dict[str, IconTemplate]:
    icon_templates = dict[str, IconTemplate]()

    for dirpath, _, filenames, in os.walk(theme):
        for filename in filenames:
            name, extension = os.path.splitext(filename)

            if extension != '.svg':
                continue

            filepath = os.path.join(dirpath, filename)
            category = filepath.split("/")[2]

            if name in icon_templates:
                icon_templates[name].add_svg(filepath)
            else:
                icon_templates[name] = IconTemplate(name, category, [filepath])

    return icon_templates


def create_icons(theme, icon_templates: Dict[str, IconTemplate]) -> None:
    for _, icon_template in tqdm(
        icon_templates.items(),
        desc=theme,
        unit='icon'
    ):
        outdir = Path(os.path.join(
            'dist',
            theme,
            icon_template.category
        ))
        Path(outdir).mkdir(parents=True, exist_ok=True)

        subprocess.run([
            'convert',
            '-density', '300',
            '-define', 'icon',
            '-background', 'none',
        ]+ icon_template.svgs + [
            os.path.join(outdir, icon_template.name + '.ico')
        ])


def main():
    for theme in ['ePapirus', 'ePapirus-Dark', 'Papirus', 'Papirus-Dark', 'Papirus-Light']:
        icon_templates = create_template_list(theme)
        create_icons(theme, icon_templates)

if __name__ == "__main__":
    main()
