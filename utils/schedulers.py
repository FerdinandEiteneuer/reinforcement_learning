"""
epsilon (exploration rate) schedulers.
"""

import numpy as np
from utils import export


@export
class EpsilonScheduler:

    def __init__(self, eps=0.1, episodes=0, minimum=0):

        assert 0 <= minimum <= 1, f'{eps=} must be between 0 and 1'
        self.minimum = minimum

        self.eps = eps

        self.episodes = episodes

    def _get_eps(self):
        return self._eps

    def _set_eps(self, eps):
        if 0 <= eps <= 1:
            self._eps = max(self.minimum, eps)
        else:
            raise ValueError(f'eps must be between 0 and 1, but is {eps}')

    @property
    def eps(self):
        return self._get_eps()

    @eps.setter
    def eps(self, eps):
        self._set_eps(eps)

    def __call__(self, episodes):
        raise NotImplementedError


@export
class DecayingEpsilonScheduler(EpsilonScheduler):

    def __init__(self, eps, decay_scale=10000, episodes=0, minimum=0):
        """
        After decay_scale episodes, the initial value of eps has dropped to 1/e
        """
        super().__init__(eps=eps, episodes=episodes, minimum=minimum)

        #self.N0 = N0
        self.decay_scale = decay_scale
        self.decay_factor = 1/np.e**(1/decay_scale)
        self.eps_0 = eps

    def __call__(self, episodes=None):
        #self.episodes = episodes
        self.eps = self.eps * self.decay_factor
        return self.eps


@export
class ConstEpsilonScheduler(EpsilonScheduler):

    def __init__(self, eps=0.1):

        super().__init__(eps)

    def __call__(self, episodes=None):
        return self.eps


if __name__ == '__main__':

    cs = ConstEpsilonScheduler(0.1)

    starting_eps = 1
    ds = DecayingEpsilonScheduler(starting_eps, decay_scale=10, minimum=0.1)

    print(starting_eps/np.e)
    for i in range(1, 20):
        print(f'{i=}, {ds()}')
