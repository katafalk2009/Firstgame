import pytest
from Firstgame.first import *


@pytest.fixture
def test_player():
    return Player(100, 100, r'D:\Pycharm Projects\Firstgame\h.png')



@pytest.fixture
def monster():
    return Monster(200, 200, 'monster.png')


@pytest.fixture
def spike_platform():
    return SpikesPlatform(300, 300, 'platform_s.png')


@pytest.fixture
def rum():
    return RUM(500, 500, r'D:\Pycharm Projects\Firstgame\rum.png')



