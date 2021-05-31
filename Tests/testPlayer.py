import pytest
from Firstgame.first import *


@pytest.fixture
def create_player():
    player = Player(100, 100, 'h.png')


@pytest.fixture
def create_monster():
    mon = Monster(200, 200, 'monster.png')


@pytest.fixture
def create_spike_platform():
    spf = SpikesPlatform(300, 300, 'platform_s.png')


@pytest.fixture
def create_rum():
    r = RUM(500, 500, 'rum.png')


def test_rum_heals():
    pass

def spike_platform_hurts():
    pass
