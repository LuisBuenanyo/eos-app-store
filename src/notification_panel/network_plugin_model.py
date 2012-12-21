from ui.abstract_notifier import AbstractNotifier
from eos_util.custom_decorators import consumes_errors
from network_manager import NetworkManager

class NetworkPluginModel(AbstractNotifier):
    NETWORK_STATE_CHANGED = 'network-state-changed'
    
    def __init__(self, network_manager = NetworkManager.from_dbus()):
        self._network_util = network_manager
        self._register_listeners()
    
    def _network_state_changed(self, *args):
        self._notify(self.NETWORK_STATE_CHANGED)
        self._network_util.register_ap_callback(self._network_strength_changed)
    
    def _network_strength_changed(self, *args):
        self._notify(self.NETWORK_STATE_CHANGED)
    
    @consumes_errors
    def _register_listeners(self):
        self._network_util.register_device_change_listener(self._network_state_changed)
        self._network_util.register_ap_callback(self._network_strength_changed)
         
    
    @consumes_errors
    def get_network_state(self):
        return self._network_util.get_network_state()
