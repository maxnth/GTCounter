import src.utils as utils

from pathlib import Path


import xml.etree.ElementTree as ET


class Counter:
    def __init__(self, path: Path, index: int):
        self.path = path
        self.index = index
        self.stats = dict()

        self.count_ground_truth()

    def collect_files(self):
        return self.path.rglob("*.xml")

    def count_ground_truth(self):
        for file in sorted(self.collect_files()):
            try:
                xml = ET.parse(str(file)).getroot()
            except ET.ParseError:
                utils.cprint(f"Warning: File {str(file)} couldn't get parsed. Skipping!", fg='r', style='bx')
                continue
            ns = utils.get_namespace(xml)

            gt_count = len(xml.findall(f".//page:TextEquiv[@index='{self.index}']", namespaces=ns))
            try:
                self.stats[str(file.parent)] += gt_count
            except KeyError:
                self.stats[str(file.parent)] = gt_count

    def get_count(self):
        return sum(self.stats.values())

    def export_stats(self, directory: Path):
        utils.export_stats(self.stats, directory)
