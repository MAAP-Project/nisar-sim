import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing.cli_test import CliTestCase

from stactools.nisar_sim.commands import create_nisarsim_command


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_nisarsim_command]

    def test_create_collection(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-collection command and validate

            # Example:
            destination = os.path.join(tmp_dir, "collection.json")

            result = self.run_command(f"nisarsim create-collection {destination}")

            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            collection = pystac.read_file(destination)
            assert collection.id == "nisar-sim"
            # assert collection.other_attr...

            collection.validate()

    def test_create_item(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-item command and validate

            # Example:
            inpath = "tests/data-files/winnip_31604_12061_004_120717_L090_CX_07"
            destination = os.path.join(tmp_dir, "item.json")
            dither = "X"
            nmode = "129"
            result = self.run_command(
                f"nisarsim create-item {inpath} {destination} --dither {dither} --nmode {nmode}"
            )
            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            item = pystac.read_file(destination)
            assert item.id == "winnip_31604_12061_004_120717_L090_CX_07"
            # assert item.other_attr...

            item.validate()
