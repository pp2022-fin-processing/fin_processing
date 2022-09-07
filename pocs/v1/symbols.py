from data.symbol import Symbol

indices = {
    'S&P 500': Symbol('^GSPC'),
    'NASDAQ': Symbol('^IXIC')
}

index_components = {
    'Apple Inc.': Symbol('AAPL'),
    'Microsoft Corporation': Symbol('MSFT'),
    'Amazon.com Inc.': Symbol('AMZN'),
    'Tesla Inc.': Symbol('TSLA'),
    'NVIDIA Corporation': Symbol('NVDA'),
    'BorgWagner Inc.': Symbol('BWA'),
    'Invesco Ltd.': Symbol('IVZ'),
    'Under Armour Inc. Class A': Symbol('UA'),
}

non_index_components = {
    'KGHM Polska Miedz S.A.': Symbol('KGHPF'),
    'Ferrexpo plc': Symbol('FXPO.L'),
}

it_companies = {
    'amazon': Symbol('amzn', 'amazon'),
    'apple': Symbol('aapl', 'apple'),
    'google': Symbol('goog', 'google'),
    'microsoft': Symbol('msft', 'microsoft'),
    'facebook': Symbol('ft', 'facebook'),
    'adobe': Symbol('adbe', 'adobe'),
    # 'accenture': Symbol('acn'),
    'akamai': Symbol('akam', 'akamai'),
    'activision': Symbol('atvi', 'activision'),
    'autodesk': Symbol('adsk', 'autodesk'),
    'nvidia': Symbol('nvda', 'nvidia'),
    'intel': Symbol('intc', 'intel'),
    # 'at&t': Symbol('t'),
    # 'tmobile': Symbol('tmus')
}