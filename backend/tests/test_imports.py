def test_app_modules_compile():
    from app.main import app
    paths = {route.path for route in app.routes}
    assert "/health" in paths
    assert "/auth/login" in paths
    assert "/patients" in paths
    assert "/doctors" in paths
    assert "/appointments" in paths
