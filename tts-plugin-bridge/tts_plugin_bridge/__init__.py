from .protocol import TTSRequest, TTSResponse, TTSConnector
from .factory import ConnectorFactory

__all__ = ["TTSRequest", "TTSResponse", "TTSConnector", "ConnectorFactory", "TTSSkill"]
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def __getattr__(name):
    args = [name]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x___getattr____mutmut_orig, x___getattr____mutmut_mutants, args, kwargs, None)


def x___getattr____mutmut_orig(name):
    if name == "TTSSkill":
        import vox4ai_skill_lib  # noqa: F811

        return vox4ai_skill_lib.TTSSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def x___getattr____mutmut_1(name):
    if name != "TTSSkill":
        import vox4ai_skill_lib  # noqa: F811

        return vox4ai_skill_lib.TTSSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def x___getattr____mutmut_2(name):
    if name == "XXTTSSkillXX":
        import vox4ai_skill_lib  # noqa: F811

        return vox4ai_skill_lib.TTSSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def x___getattr____mutmut_3(name):
    if name == "ttsskill":
        import vox4ai_skill_lib  # noqa: F811

        return vox4ai_skill_lib.TTSSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def x___getattr____mutmut_4(name):
    if name == "TTSSKILL":
        import vox4ai_skill_lib  # noqa: F811

        return vox4ai_skill_lib.TTSSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def x___getattr____mutmut_5(name):
    if name == "TTSSkill":
        import vox4ai_skill_lib  # noqa: F811

        return vox4ai_skill_lib.TTSSkill
    raise AttributeError(None)

x___getattr____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x___getattr____mutmut_1': x___getattr____mutmut_1, 
    'x___getattr____mutmut_2': x___getattr____mutmut_2, 
    'x___getattr____mutmut_3': x___getattr____mutmut_3, 
    'x___getattr____mutmut_4': x___getattr____mutmut_4, 
    'x___getattr____mutmut_5': x___getattr____mutmut_5
}
x___getattr____mutmut_orig.__name__ = 'x___getattr__'
