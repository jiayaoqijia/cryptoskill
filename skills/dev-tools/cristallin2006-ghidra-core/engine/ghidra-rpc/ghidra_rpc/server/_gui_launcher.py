"""GUI launcher for ghidra-rpc, adapted from pyghidra-mcp's GuiPyGhidraMcpLauncher."""

from __future__ import annotations

import contextlib
import ctypes
import sys
import threading
import time
from pathlib import Path

from pyghidra.launcher import PyGhidraLauncher, _PyGhidraStdOut


class GuiRpcLauncher(PyGhidraLauncher):
    """PyGhidra GUI launcher adapted for ghidra-rpc lifecycle control."""

    def __init__(self, project_gpr_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_vmargs("-DUSER_AGREEMENT=ACCEPT")
        self.project_gpr_path = project_gpr_path
        self.args = []
        self._is_exiting = threading.Event()
        self._shutdown_requested = False

    def _launch(self) -> None:
        """Start the Ghidra GUI without blocking the caller.

        The project path is passed directly to GhidraRun so Ghidra opens the
        requested project immediately on startup, bypassing the
        "restore last-used project" behaviour.  This avoids races with
        Ghidra's own project-restore sequence and eliminates the need for any
        post-startup project-switching logic.
        """
        from ghidra import Ghidra
        from java.lang import Runtime, Thread  # type: ignore

        if sys.platform == "win32":
            appid = ctypes.c_wchar_p(self.app_info.name)
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

        Runtime.getRuntime().addShutdownHook(Thread(self._is_exiting.set))

        # Pass the .gpr path as the first argument so GhidraRun opens the right
        # project from the start instead of auto-restoring the last-used one.
        args = ["ghidra.GhidraRun", str(self.project_gpr_path), *self.args]

        stdout = _PyGhidraStdOut(sys.stdout)
        stderr = _PyGhidraStdOut(sys.stderr)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            Thread(lambda: Ghidra.main(args)).start()

    def run_gui_event_loop(self) -> None:
        """Block until the GUI is shutting down."""
        if sys.platform == "darwin":
            from pyghidra.launcher import _run_mac_app
            _run_mac_app()
        self._is_exiting.wait()

    def request_shutdown(self) -> None:
        """Ask the running Ghidra GUI to close itself cleanly."""
        if self._shutdown_requested or self._is_exiting.is_set():
            return
        self._shutdown_requested = True

        from ghidra.framework.main import AppInfo
        from ghidra.util import Swing

        def do_close():
            front_end_tool = AppInfo.getFrontEndTool()
            if front_end_tool is not None:
                front_end_tool.close()

        Swing.runLater(do_close)

    def wait_for_shutdown(self, timeout: float = 5.0) -> bool:
        """Wait for a clean GUI shutdown."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self._is_exiting.wait(timeout=0.1):
                return True
        return self._is_exiting.is_set()
