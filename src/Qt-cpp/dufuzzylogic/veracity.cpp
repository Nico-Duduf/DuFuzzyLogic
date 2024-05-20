#include "veracity.h"

FzL::Engine::Algorithm FzL::Veracity::algorithm() const {
    if (_a == Engine::Default)
        return Engine::globalEngine()->algorithm();
    return _a;
}
