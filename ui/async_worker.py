"""
Helpers de threading Qt : execute une fonction bloquante (OCR, IMAP, etc.)
dans un QThread tout en affichant un QProgressDialog.

Usage :
    from ui.async_worker import run_with_progress

    result = run_with_progress(
        parent=self,
        title="Connexion IMAP",
        message="Recuperation des emails ...",
        target=fetch_invoice_pdfs,
        args=(server, port, email_addr, password),
    )
    if result.success:
        do_something(result.value)
    else:
        show_error(result.error)
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple

from PySide6.QtCore import QObject, QThread, Signal, Qt
from PySide6.QtWidgets import QProgressDialog, QApplication


@dataclass
class WorkerResult:
    success: bool
    value: Any = None
    error: Optional[BaseException] = None


class _Worker(QObject):
    finished = Signal(object)  # WorkerResult

    def __init__(self, target: Callable, args: Tuple, kwargs: dict):
        super().__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            value = self._target(*self._args, **self._kwargs)
            self.finished.emit(WorkerResult(success=True, value=value))
        except BaseException as e:
            self.finished.emit(WorkerResult(success=False, error=e))


def run_with_progress(parent, title: str, message: str,
                      target: Callable, args: tuple = (), kwargs: dict = None,
                      cancellable: bool = False) -> WorkerResult:
    """
    Execute `target(*args, **kwargs)` dans un QThread.
    Bloque l UI utilisateur via un QProgressDialog modal indeterminate,
    mais ne bloque pas la boucle d evenements Qt (pas de freeze).

    Retourne un WorkerResult une fois le travail termine.
    Si cancellable=True, le bouton Annuler est actif (mais le travail
    en cours ne peut pas etre interrompu cote Python : on n attend
    simplement plus le resultat).
    """
    kwargs = kwargs or {}

    progress = QProgressDialog(message, "Annuler" if cancellable else None,
                               0, 0, parent)
    progress.setWindowTitle(title)
    progress.setWindowModality(Qt.WindowModal)
    progress.setMinimumDuration(0)
    progress.setAutoClose(False)
    progress.setAutoReset(False)
    if not cancellable:
        progress.setCancelButton(None)

    thread = QThread()
    worker = _Worker(target, args, kwargs)
    worker.moveToThread(thread)

    holder: dict = {}

    def _on_finished(res: WorkerResult):
        holder["result"] = res
        thread.quit()

    worker.finished.connect(_on_finished)
    thread.started.connect(worker.run)
    thread.finished.connect(worker.deleteLater)

    thread.start()
    progress.show()

    while thread.isRunning():
        QApplication.processEvents()
        if cancellable and progress.wasCanceled():
            holder.setdefault(
                "result",
                WorkerResult(success=False, error=InterruptedError("annule par l utilisateur"))
            )
            break

    progress.close()
    thread.wait(5000)
    thread.deleteLater()

    return holder.get("result", WorkerResult(success=False,
                                             error=RuntimeError("worker termine sans resultat")))
