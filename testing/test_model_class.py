from transitgen._Modelgen import PyModel


def test_id():
    m = PyModel()
    m.id = 10
    assert m.id == 10


def test_submodel_id():
    m = PyModel()
    m.submodel_id = 10
    assert m.submodel_id == 10


def test_period():
    m = PyModel()
    m.period = 10.2
    assert m.period == 10.2


def test_epoch():
    m = PyModel()
    m.epoch = 10.2
    assert m.epoch == 10.2


def test_a():
    m = PyModel()
    m.a = 10.2
    assert m.a == 10.2


def test_rs():
    m = PyModel()
    m.rs = 10.2
    assert m.rs == 10.2


def test_i():
    m = PyModel()
    m.i = 10.2
    assert m.i == 10.2


def test_rp():
    m = PyModel()
    m.rp = 10.2
    assert m.rp == 10.2


def test_mstar():
    m = PyModel()
    m.mstar = 10.2
    assert m.mstar == 10.2


def test_c1():
    m = PyModel()
    m.c1 = 10.2
    assert m.c1 == 10.2


def test_c2():
    m = PyModel()
    m.c2 = 10.2
    assert m.c2 == 10.2


def test_c3():
    m = PyModel()
    m.c3 = 10.2
    assert m.c3 == 10.2


def test_c4():
    m = PyModel()
    m.c4 = 10.2
    assert m.c4 == 10.2


def test_teff():
    m = PyModel()
    m.teff = 10.2
    assert m.teff == 10.2
