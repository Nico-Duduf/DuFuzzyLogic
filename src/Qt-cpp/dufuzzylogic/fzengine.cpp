#include "fzengine.h"

#include "fzveracity.h"
#include "fzvalue.h"
#include "fzset.h"

FzEngine *FzEngine::_globalEngine = nullptr;

FzEngine *FzEngine::globalEngine()
{
    if (!_globalEngine) _globalEngine = new FzEngine();
    return _globalEngine;
}

FzEngine::FzEngine():
    _v(new FzVeracity(false))
{}

FzEngine::FzEngine(Algorithm algorithm):
    _a(algorithm),
    _v(new FzVeracity(false))
{}

FzEngine::~FzEngine()
{
    delete _v;
}

void FzEngine::setVeracity(const FzVeracity &v)
{
    _v = new FzVeracity(v);
}

FzVeracity FzEngine::veracity() {
    return *_v;
}

FzVeracity FzEngine::fif(const FzVeracity &v)
{
    setVeracity(v);
    return v;
}

void FzEngine::then(FzValue *v, const FzSet &s)
{
    v->set(s, *_v);
}

FzVeracity FzEngine::fif(const FzVeracity &v, std::function<void (FzVeracity)> then) {
    setVeracity(v);
    then(v);
    return v;
}
