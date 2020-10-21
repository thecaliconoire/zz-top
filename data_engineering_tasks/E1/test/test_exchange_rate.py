def test_postgres_connection(setup):
    """test if table exists"""
    cursor = setup
    cursor.execute('SELECT * FROM currency')
    records = cursor.fetchall()
    record = len(list(records))
    assert record== 3

def test_get_project_costs(setup):
    """can select a value"""
    cursor = setup
    cursor.execute('SELECT currency, rate FROM currency WHERE rate = 1')
    eur = cursor.fetchall()
    assert eur == [('EUR', 1.0)]