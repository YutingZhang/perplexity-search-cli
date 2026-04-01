from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

_MSG = """
=======================================================
  perplexity-search-cli installed!

  To register as a Claude Code MCP server, run:

    perplexity-install-claude-mcp

=======================================================
"""


class PostInstall(install):
    def run(self):
        super().run()
        print(_MSG)


class PostDevelop(develop):
    def run(self):
        super().run()
        print(_MSG)


setup(
    cmdclass={
        "install": PostInstall,
        "develop": PostDevelop,
    }
)
