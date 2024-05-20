#include "fzveracity.h"

FzEngine::Algorithm FzVeracity::algorithm() const {
    if (_a == FzEngine::Default)
        return FzEngine::globalEngine()->algorithm();
    return _a;
}
