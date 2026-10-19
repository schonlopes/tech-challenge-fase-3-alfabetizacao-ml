from scripts.extract_gcp import decode_cli


def test_decodes_windows_cli_without_corrupting_municipality_names():
    payload = '{"municipio": "São João"}'
    assert decode_cli(payload.encode('utf-8')) == payload
    assert decode_cli(payload.encode('cp1252')) == payload
