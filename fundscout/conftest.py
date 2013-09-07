from gocept.pytestlayer import fixture


globals().update(fixture.create(
    'fundscout.testing.SQLLayer',
    'fundscout.testing.IntegrationLayer',
))
