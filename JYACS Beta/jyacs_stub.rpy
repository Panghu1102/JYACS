# jyacs_stub.rpy – Compatibility stubs for running JYACS sub-mod inside Just Yuri without Monika-After-Story dependencies.
# This file MUST be loaded very early so we use a highly negative init priority.

init -2000 python:
    """Provide dummy implementations of MAS/JYACS helper utilities that
    header.rpy still references.  When the real implementations are not
    present (e.g. in Just Yuri) these stubs prevent NameErrors so the rest
    of the game can finish loading normally.
    """
    import types, logging, store

    # ------------------------------------------------------------------
    # Generic no-op helpers ------------------------------------------------
    # ------------------------------------------------------------------
    def _noop(*_args, **_kwargs):
        """A do-nothing placeholder function."""
        return None

    def _decorator_noop(*_dargs, **_dkwargs):
        """Return a decorator that leaves the wrapped function untouched."""
        def _wrap(fn):
            return fn
        return _wrap

    # ------------------------------------------------------------------
    # Stub for jyacs_submod_utils ----------------------------------------
    # ------------------------------------------------------------------
    if not hasattr(store, "jyacs_submod_utils"):
        store.jyacs_submod_utils = types.SimpleNamespace()
        store.jyacs_submod_utils.Submod = _noop
        store.jyacs_submod_utils.getAndRunFunctions = _noop
        store.jyacs_submod_utils.functionplugin = _decorator_noop
        store.jyacs_submod_utils.submod_log = types.SimpleNamespace()
        store.jyacs_submod_utils.submod_log.level = logging.INFO

    # ------------------------------------------------------------------
    # Alias MAS symbols to the same stub so any residual MAS references
    # won't break the build. ------------------------------------------------
    # ------------------------------------------------------------------
    if not hasattr(store, "mas_submod_utils"):
        store.mas_submod_utils = store.jyacs_submod_utils

    # Provide dummy objects occasionally accessed by legacy MAS code
    if not hasattr(store, "mas_ptod"):
        store.mas_ptod = types.SimpleNamespace()
        store.mas_ptod.font = None

    if not hasattr(store, "mas_ui"):
        store.mas_ui = types.SimpleNamespace()
        store.mas_ui.MONO_FONT = "DejaVuSansMono.ttf"

    # ------------------------------------------------------------------
    # Ensure the original game title is preserved ------------------------
    # ------------------------------------------------------------------
    # Many Ren'Py projects (including Just Yuri) set the displayed title
    # in options.rpy via config.name or gui.window_title.  If an error
    # earlier in initialization prevents options.rpy from being executed,
    # the window falls back to the generic "A Ren'Py Game" string.
    # Setting a safe default here guarantees the title remains correct
    # even if other script errors occur afterwards.
    #
    # We only set the name when it has not already been defined to avoid
    # clobbering the real value when it *is* present.
    if not getattr(config, "name", None):
        config.name = "Just Yuri"

    if not hasattr(store, "getAPIKey"):
        store.getAPIKey = lambda *_args, **_kwargs: ""

    # Common MAS helper symbols occasionally referenced -------------------
    mas_helpers = {
        "_mas_getAffection": (lambda *_a, **_k: 0),
        "mas_getAffection": (lambda *_a, **_k: 0),
        "mas_getEV": (lambda *_a, **_k: None),
        "mas_inEVL": (lambda *_a, **_k: False),
    }
    
    # Add each helper to store if it doesn't exist
    for _name, _default in mas_helpers.items():
        if not hasattr(store, _name):
            setattr(store, _name, _default)

    if not hasattr(store, "mas_rev_unseen"):
        store.mas_rev_unseen = []
        
    if not hasattr(store, "player"):
        store.player = "Player"
        
    def getEV(name):
        """Placeholder for event access function"""
        return None
        
    if not hasattr(store, "getEV"):
        store.getEV = getEV
        
    if not hasattr(store, "jyacs_chat_history"):
        store.jyacs_chat_history = []
        
    if not hasattr(store, "jyacs_log"):
        def jyacs_log(message, level="INFO"):
            """Simple logging function"""
            print("[JYACS-{}] {}".format(level, message))
        store.jyacs_log = jyacs_log 