#!/usr/bin/env python3
import importlib
import sys
from pathlib import Path

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

try:
    from ...core import SafeOpenError, safe_open_package
except ImportError:
    # Fallback for repository layout where core is a top-level sibling package.
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    core_module = importlib.import_module("core")
    SafeOpenError = core_module.SafeOpenError
    safe_open_package = core_module.safe_open_package


def _format_summary(result) -> str:
    primary_media_path = result.primary_media_path if result.primary_media_path is not None else "None"
    lines = [
        f"package_type: {result.package_type}",
        f"manifest bytes length: {len(result.manifest_bytes)}",
        f"primary_media_path: {primary_media_path}",
        f"file_paths count: {len(result.file_paths)}",
    ]
    return "\n".join(lines)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AIFX Player (v0) — Read-only Viewer")
        self.resize(980, 640)

        self._media_bytes_qba: QByteArray | None = None
        self._media_buffer: QBuffer | None = None

        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.errorOccurred.connect(self._on_playback_error)

        self.summary_view = QtWidgets.QPlainTextEdit()
        self.summary_view.setReadOnly(True)
        self.summary_view.setPlainText("Use File -> Open... to inspect an AIFX package.")

        self.play_button = QtWidgets.QPushButton("Play")
        self.pause_button = QtWidgets.QPushButton("Pause")
        self.stop_button = QtWidgets.QPushButton("Stop")

        self.play_button.clicked.connect(self.player.play)
        self.pause_button.clicked.connect(self.player.pause)
        self.stop_button.clicked.connect(self.player.stop)
        self._set_controls_enabled(False)

        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addStretch(1)

        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.addWidget(self.summary_view)
        layout.addLayout(controls_layout)
        self.setCentralWidget(container)

        file_menu = self.menuBar().addMenu("&File")
        open_action = file_menu.addAction("Open...")
        open_action.triggered.connect(self.on_open)

    def _set_controls_enabled(self, enabled: bool) -> None:
        self.play_button.setEnabled(enabled)
        self.pause_button.setEnabled(enabled)
        self.stop_button.setEnabled(enabled)

    def _clear_media_source(self) -> None:
        self.player.stop()
        self.player.setSource(QUrl())

        if self._media_buffer is not None and self._media_buffer.isOpen():
            self._media_buffer.close()

        self._media_buffer = None
        self._media_bytes_qba = None

    def _load_media_from_bytes(self, media_bytes: bytes, media_path: str | None) -> None:
        self._clear_media_source()

        self._media_bytes_qba = QByteArray(media_bytes)
        self._media_buffer = QBuffer(self)
        self._media_buffer.setData(self._media_bytes_qba)
        if not self._media_buffer.open(QIODevice.ReadOnly):
            raise RuntimeError("Failed to open in-memory audio buffer")

        # Give Qt a suffix hint for codec inference (no disk IO happens).
        hint_name = media_path or "audio.wav"
        source_url = QUrl.fromLocalFile(hint_name)

        self.player.setSourceDevice(self._media_buffer, source_url)

    def _on_playback_error(self, _error: QMediaPlayer.Error) -> None:
        QtWidgets.QMessageBox.critical(self, "Playback Error", self.player.errorString())

    @QtCore.Slot()
    def on_open(self) -> None:
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open AIFX Package",
            "",
            "AIFX Packages (*.aifm *.aifv *.aifi *.aifp)",
        )
        if not file_path:
            return

        try:
            result = safe_open_package(file_path)
        except SafeOpenError as exc:
            QtWidgets.QMessageBox.critical(self, "Open Error", str(exc))
            return
        except Exception:
            QtWidgets.QMessageBox.critical(
                self,
                "Open Error",
                "An unexpected error occurred while opening the package.",
            )
            return

        self.summary_view.setPlainText(_format_summary(result))

        if result.package_type == "aifm" and result.primary_media_bytes is not None:
            self._load_media_from_bytes(result.primary_media_bytes, result.primary_media_path)
            self._set_controls_enabled(True)
        else:
            self._clear_media_source()
            self._set_controls_enabled(False)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("AIFX Player")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
