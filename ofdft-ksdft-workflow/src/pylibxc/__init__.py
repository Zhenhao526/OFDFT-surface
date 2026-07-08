"""Small pylibxc compatibility layer for DFTpy.

The real pylibxc package is not available from this environment's Python
indexes, while Homebrew provides libxc itself. DFTpy only needs
``pylibxc.functional.LibXCFunctional`` for the current LDA/GGA workflows, so
the project ships that narrow API backed by the system libxc shared library.
"""

