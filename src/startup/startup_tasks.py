from endless_core.auto_updates.update_manager import UpdateManager
from endless_core.auto_updates.force_install import ForceInstall
from eos_settings.delete_settings_run_file import DeleteSettingsRunFile
from eos_log import log


class StartupTasks(object):
    DEFAULT_TASKS = [ ForceInstall, UpdateManager, DeleteSettingsRunFile ]
    def __init__(self, tasks = DEFAULT_TASKS):
        self._all_tasks = tasks 
    
    def perform_tasks(self):
        for task in self._all_tasks:
            try:
                task().execute()
            except Exception as e:
                log.error("An error ocurred while executing " + task.__name__, e)

