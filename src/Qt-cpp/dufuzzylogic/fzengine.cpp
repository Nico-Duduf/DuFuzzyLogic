#include "engine.h"

#include "veracity.h"
#include "value.h"
#include "set.h"

FzL::Engine *FzL::Engine::_globalEngine = nullptr;

FzL::Veracity FzL::fif(const Veracity &v) {
    return Engine::globalEngine()->fif(v);
}

template<typename Then>
FzL::Veracity FzL::fif(const Veracity &v, Then &&then)
{
    return Engine::globalEngine()->fif(v, then);
}

void FzL::then(Value *v, const Set &s)
{
    Engine::globalEngine()->then(v, s);
}

FzL::Engine *FzL::Engine::globalEngine()
{
    if (!_globalEngine) _globalEngine = new Engine();
    return _globalEngine;
}

FzL::Engine::Engine():
    _v(new Veracity(false))
{}

FzL::Engine::Engine(Algorithm algorithm):
    _a(algorithm),
    _v(new Veracity(false))
{}

FzL::Engine::~Engine()
{
    delete _v;
}

void FzL::Engine::setVeracity(const Veracity &v)
{
    _v = new Veracity(v);
}

FzL::Veracity FzL::Engine::veracity() {
    return *_v;
}

FzL::Veracity FzL::Engine::fif(const Veracity &v)
{
    setVeracity(v);
    return v;
}

void FzL::Engine::then(Value *v, const Set &s)
{
    v->set(s, *_v);
}

template<typename Then>
FzL::Veracity FzL::Engine::fif(const Veracity &v, Then &&then)
{
    setVeracity(v);
    then(v);
    return v;
}

FzL::Veracity FzL::currentVeracity()
{
    return Engine::globalEngine()->veracity();
}
